"""Fake work mode.

Kaka goes to a virtual "keyboard spot", sits down, and pretends to be
hard at work: micro key-tap movement + a rotating status glyph.

This is purely animation; nothing is really typed. It's a mood booster
and joke feature — perfect for camera-on meetings when you look away.
"""
from __future__ import annotations

import random
import time
from dataclasses import dataclass


@dataclass
class WorkModeState:
    active: bool = False
    started_at: float = 0.0
    duration_s: float = 0.0
    typing_offset: float = 0.0
    status_frame: int = 0
    keyboard_x: int = 0
    keyboard_y: int = 0

    STATUS_FRAMES = ("⌨️", "💻", "📊", "📝", "☕️")

    def start(self, kb_x: int, kb_y: int, duration_s: float = 120.0) -> None:
        self.active = True
        self.started_at = time.time()
        self.duration_s = duration_s
        self.typing_offset = 0.0
        self.status_frame = 0
        self.keyboard_x = kb_x
        self.keyboard_y = kb_y

    def stop(self) -> None:
        self.active = False

    def tick(self, tick_ms: int) -> None:
        if not self.active:
            return
        self.typing_offset = random.uniform(-1.5, 1.5)
        if int((time.time() - self.started_at) * 1.5) != self.status_frame:
            self.status_frame = int((time.time() - self.started_at) * 1.5) % len(
                self.STATUS_FRAMES
            )
        if time.time() - self.started_at > self.duration_s:
            self.active = False

    def current_glyph(self) -> str:
        return self.STATUS_FRAMES[self.status_frame % len(self.STATUS_FRAMES)]
