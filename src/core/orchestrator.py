"""Orchestrator for interactive choice sessions.

The ChoiceOrchestrator is the central coordinator for user interaction:
- Validates incoming requests
- Determines the best available interface (Terminal vs Web)
- Executes the interaction on the chosen interface
- Supports terminal hand-off for non-blocking MCP invocations
"""
from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Dict, List, Optional

from ..infra import get_logger, get_language_from_env, ConfigStore
from .models import (
    LANG_EN,
    ProvideChoiceConfig,
    ProvideChoiceRequest,
    ProvideChoiceResponse,
    ValidationError,
    TRANSPORT_TERMINAL,
    TRANSPORT_WEB,
    TRANSPORT_DESKTOP,
)
from .validation import parse_request
from .response import cancelled_response, timeout_response
from ..web import run_web_choice, create_terminal_handoff_session, poll_terminal_session_result

__all__ = ["ChoiceOrchestrator", "safe_handle"]

_logger = get_logger(__name__)


# Section: Orchestrator Logic
class ChoiceOrchestrator:
    """
    Central coordinator for user interaction.

    This class is responsible for:
    1. Validating the incoming request.
    2. Determining the best available interface (Terminal vs Web).
    3. Executing the interaction on the chosen interface.
    4. Supporting terminal hand-off for non-blocking MCP invocations.
    """
    def __init__(self, *, config_path: Optional[Path] = None) -> None:
        self._store = ConfigStore(path=config_path)
        self._last_config: Optional[ProvideChoiceConfig] = self._store.load()

    async def handle(
        self,
        *,
        title: str,
        prompt: str,
        selection_mode: str,
        options: List[Dict[str, object]],
        timeout_seconds: Optional[int] = None,
        # Extended schema fields
        single_submit_mode: Optional[bool] = None,
        use_default_option: Optional[bool] = None,
        timeout_action: Optional[str] = None,
        # Terminal hand-off support
        session_id: Optional[str] = None,
    ) -> ProvideChoiceResponse:
        """
        Process a choice request from start to finish.
        
        Validates inputs, selects interface, and awaits user action.
        
        When `session_id` is provided, polls for the result of an existing
        terminal hand-off session instead of creating a new interaction.
        """
        _logger.info(f"Handling choice request: title='{title}', mode={selection_mode}, options={len(options)}")

        # Section: Session Polling
        # If session_id is provided, poll for result of existing terminal session.
        # The poll function blocks for up to 30s waiting for the result,
        # reducing the need for frequent polling by the AI agent.
        if session_id is not None:
            result = await poll_terminal_session_result(session_id, wait_seconds=30)
            if result is not None:
                return result
            # Session not found (expired or invalid)
            from .models import ProvideChoiceSelection
            return ProvideChoiceResponse(
                action_status="cancelled",
                selection=ProvideChoiceSelection(
                    selected_indices=[],
                    interface=TRANSPORT_TERMINAL,
                    summary=f"Session {session_id} not found or expired. Please create a new session.",
                ),
            )

        # Section: Request Validation
        # Step 1: Validate and parse the request payload.
        req: ProvideChoiceRequest = parse_request(
            title=title,
            prompt=prompt,
            selection_mode=selection_mode,
            options=options,
            timeout_seconds=timeout_seconds,
            single_submit_mode=single_submit_mode,
            use_default_option=use_default_option,
            timeout_action=timeout_action,
        )
        _logger.debug(f"Request parsed successfully")

        config_defaults = self._build_default_config(req)

        # Section: Transport Selection
        # If terminal interface is configured, create a terminal hand-off session.
        # The AI agent will execute the terminal command to start the interaction.
        if config_defaults.interface == TRANSPORT_TERMINAL:
            _logger.debug("Using terminal interface (handoff)")
            # Update cached config for future calls
            self._last_config = config_defaults
            return await create_terminal_handoff_session(req, config_defaults)

        # If desktop interface is configured, use native window
        if config_defaults.interface == TRANSPORT_DESKTOP:
            _logger.debug("Using desktop interface (pywebview)")
            from ..desktop import run_desktop_choice, is_desktop_available
            if is_desktop_available():
                response, final_config = await run_desktop_choice(req, defaults=config_defaults, allow_terminal=True)
                self._last_config = final_config
                _logger.info(f"Choice completed via desktop: action={response.action_status}")
                return response
            else:
                _logger.warning("Desktop mode unavailable, falling back to web")
                # Fall through to web mode

        # Otherwise, use web interface (default)
        _logger.debug("Using web interface")
        response, final_config = await run_web_choice(req, defaults=config_defaults, allow_terminal=True)
        # Update cached config with final config used
        self._last_config = final_config
        _logger.info(f"Choice completed via web: action={response.action_status}")
        return response

    def _build_default_config(self, req: ProvideChoiceRequest) -> ProvideChoiceConfig:
        # Always reload config to get latest settings from Web UI
        saved = self._store.load()
        # Transport preference: use saved config or default to web
        transport_pref = saved.interface if saved else TRANSPORT_WEB
        timeout_pref = saved.timeout_seconds if saved else req.timeout_seconds

        # Extended settings: inherit from saved config or request defaults
        single_submit_pref = saved.single_submit_mode if saved else req.single_submit_mode
        use_default_option_pref = saved.use_default_option if saved else req.use_default_option
        timeout_action_pref = saved.timeout_action if saved else req.timeout_action

        # Language: env > saved > default (en)
        env_lang = get_language_from_env()
        if env_lang is not None:
            language_pref = env_lang
        elif saved is not None:
            language_pref = saved.language
        else:
            language_pref = LANG_EN

        return ProvideChoiceConfig(
            interface=transport_pref,
            timeout_seconds=timeout_pref,
            single_submit_mode=single_submit_pref,
            use_default_option=use_default_option_pref,
            timeout_action=timeout_action_pref,
            language=language_pref,
        )



# Section: Safety Wrapper
async def safe_handle(orchestrator: ChoiceOrchestrator, **kwargs) -> ProvideChoiceResponse:
    """
    Wrapper to catch unexpected errors during orchestration.
    
    Ensures that the MCP tool always returns a valid JSON response,
    even if validation fails or an unhandled exception occurs.
    Includes retry logic for transient connection errors.
    """
    max_retries = 2
    last_error = None
    
    for attempt in range(max_retries + 1):
        try:
            return await orchestrator.handle(**kwargs)
        except ValidationError as exc:
            # Validation errors should not be retried
            _logger.warning(f"Validation error: {exc}")
            return cancelled_response(
                interface=kwargs.get("interface") or TRANSPORT_TERMINAL,
                url=None,
                summary=f"validation_error: {exc}",
            )
        except asyncio.CancelledError:
            _logger.debug("Request cancelled")
            raise
        except ConnectionError as exc:
            # Connection errors may be transient, retry
            last_error = exc
            if attempt < max_retries:
                _logger.warning(f"Connection error (attempt {attempt + 1}/{max_retries + 1}): {exc}, retrying...")
                await asyncio.sleep(0.5 * (attempt + 1))  # Exponential backoff
                continue
            _logger.exception(f"Connection error after {max_retries + 1} attempts: {exc}")
        except OSError as exc:
            # OS errors (like port binding) may be transient
            last_error = exc
            if attempt < max_retries:
                _logger.warning(f"OS error (attempt {attempt + 1}/{max_retries + 1}): {exc}, retrying...")
                await asyncio.sleep(0.5 * (attempt + 1))
                continue
            _logger.exception(f"OS error after {max_retries + 1} attempts: {exc}")
        except Exception as exc:
            # Other errors - log and return error response
            last_error = exc
            _logger.exception(f"Unexpected error during orchestration: {exc}")
            break
    
    # All retries exhausted or non-retryable error
    try:
        # Filter out session_id as it's not part of parse_request
        parse_kwargs = {k: v for k, v in kwargs.items() if k != "session_id"}
        req = parse_request(**parse_kwargs)
        return timeout_response(req=req, interface=kwargs.get("interface") or TRANSPORT_TERMINAL, url=None)
    except Exception:
        # If even parsing fails, return cancelled response with error details
        error_msg = str(last_error) if last_error else "Unknown error"
        return cancelled_response(
            interface=kwargs.get("interface") or TRANSPORT_TERMINAL, 
            url=None,
            summary=f"orchestration_error: {error_msg}",
        )
