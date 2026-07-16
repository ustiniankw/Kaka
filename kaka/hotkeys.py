"""Global boss-key hotkey listener.

Runs in a background thread so it doesn't block the Qt event loop.
"""
from __future__ import annotations

from typing import Callable, Optional

try:
    from pynput import keyboard
    _PYNPUT_OK = True
except Exception:  # pragma: no cover - optional at runtime
    _PYNPUT_OK = False


class BossKey:
    def __init__(self, combo: str, callback: Callable[[], None]):
        self._callback = callback
        self._combo = combo
        self._listener: Optional["keyboard.GlobalHotKeys"] = None

    def start(self) -> None:
        if not _PYNPUT_OK:
            print("[Kaka] pynput not available; boss key disabled.")
            return
        try:
            self._listener = keyboard.GlobalHotKeys({self._combo: self._callback})
            self._listener.daemon = True
            self._listener.start()
        except Exception as e:
            print(f"[Kaka] Failed to register boss key: {e}")

    def stop(self) -> None:
        if self._listener is not None:
            try:
                self._listener.stop()
            except Exception:
                pass
            self._listener = None
