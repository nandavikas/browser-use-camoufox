"""Optional shared Playwright Firefox browser for BiDi sessions.

Host apps that already hold a live ``playwright.firefox.connect()`` handle
(e.g. a Camoufox singleton across LangGraph nodes) can register it here.
``BrowserSession.connect()`` then reuses that browser instead of opening a
second WS connection — Playwright browser-server contexts are *per
connection*, so a second connect would see a blank page and lose form state.

The shared browser is never closed by ``BidiBrowserConnection.stop()``;
the host owns its lifecycle.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
	from playwright.async_api import Browser as PlaywrightBrowser
	from playwright.async_api import Playwright

_shared_playwright: Playwright | None = None
_shared_browser: PlaywrightBrowser | None = None


def set_shared_browser(playwright: Playwright, browser: PlaywrightBrowser) -> None:
	"""Register a live Playwright Firefox browser for BiDi sessions to reuse."""
	global _shared_playwright, _shared_browser
	_shared_playwright = playwright
	_shared_browser = browser


def clear_shared_browser() -> None:
	"""Forget the shared browser (does not close it)."""
	global _shared_playwright, _shared_browser
	_shared_playwright = None
	_shared_browser = None


def get_shared_browser() -> tuple[Playwright, PlaywrightBrowser] | None:
	"""Return ``(playwright, browser)`` if a live shared browser is registered."""
	if _shared_playwright is None or _shared_browser is None:
		return None
	try:
		if not _shared_browser.is_connected():
			return None
	except Exception:
		return None
	return (_shared_playwright, _shared_browser)
