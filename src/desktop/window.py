"""Desktop window implementation using PyWebView.

Provides a native desktop window that displays the web interface
in a lightweight, always-on-top popup window.

Note: PyWebView must run on the main thread, so we spawn a separate
process to handle the window.
"""
from __future__ import annotations

import asyncio
import subprocess
import sys
from typing import TYPE_CHECKING

from ..infra import get_logger

if TYPE_CHECKING:
    from ..core.models import ProvideChoiceConfig, ProvideChoiceRequest, ProvideChoiceResponse

__all__ = ["run_desktop_choice", "is_desktop_available"]

_logger = get_logger(__name__)

# Check if pywebview is available
_WEBVIEW_AVAILABLE = False
try:
    import webview
    _WEBVIEW_AVAILABLE = True
except ImportError:
    _logger.warning("pywebview not installed, desktop mode unavailable")


def is_desktop_available() -> bool:
    """Check if desktop mode is available."""
    return _WEBVIEW_AVAILABLE


def _run_webview_window(url: str, title: str) -> None:
    """Run the webview window (must be called from main thread).
    
    This function is called in a subprocess to avoid main thread issues.
    """
    import webview
    
    window = webview.create_window(
        title=title or "Interactive Choice",
        url=url,
        width=1200,
        height=800,
        resizable=True,
        on_top=True,
        confirm_close=False,
        text_select=True,
    )
    webview.start()


async def run_desktop_choice(
    req: "ProvideChoiceRequest",
    *,
    defaults: "ProvideChoiceConfig",
    allow_terminal: bool,
) -> tuple["ProvideChoiceResponse", "ProvideChoiceConfig"]:
    """Run a choice session in a native desktop window.
    
    Creates a PyWebView window that loads the web interface URL.
    The window is always-on-top and sized appropriately for the content.
    
    Args:
        req: The choice request
        defaults: Default configuration
        allow_terminal: Whether to allow terminal fallback
        
    Returns:
        Tuple of (response, final_config)
    """
    if not _WEBVIEW_AVAILABLE:
        raise RuntimeError("pywebview not installed. Install with: pip install pywebview")
    
    from ..web.server import _get_server
    
    # First, ensure web server is running and create session
    server = await _get_server()
    session = await server.create_session(req, defaults, allow_terminal)
    url = session.url
    title = req.title or "Interactive Choice"
    
    _logger.info(f"Opening desktop window for session {session.choice_id[:8]}")
    
    # Spawn a subprocess to run the webview window
    # This avoids the main thread requirement
    script = f'''
import webview
window = webview.create_window(
    title="{title}",
    url="{url}",
    width=1200,
    height=800,
    resizable=True,
    on_top=True,
    confirm_close=False,
    text_select=True,
)
webview.start()
'''
    
    # Start subprocess
    process = subprocess.Popen(
        [sys.executable, "-c", script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    
    _logger.info(f"Desktop window subprocess started (PID: {process.pid})")
    
    # Wait for result from the session
    try:
        result = await session.wait_for_result()
    except asyncio.CancelledError:
        _logger.info(f"Desktop session {session.choice_id[:8]} cancelled")
        # Kill the subprocess
        process.terminate()
        raise
    finally:
        # Clean up subprocess if still running
        if process.poll() is None:
            process.terminate()
    
    final_config = session.config_used
    return result, final_config
