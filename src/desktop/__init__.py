"""Desktop window module using PyWebView.

Provides native desktop window support for interactive choice sessions.
"""
from __future__ import annotations

from .window import run_desktop_choice, is_desktop_available

__all__ = ["run_desktop_choice", "is_desktop_available"]
