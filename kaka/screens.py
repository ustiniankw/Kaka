"""Multi-screen roaming helper.

Kaka can walk across every connected display. We treat the union of all
screen geometries as one virtual "desktop" the pet can roam.
"""
from __future__ import annotations

from typing import List, Tuple

from PySide6.QtCore import QRect
from PySide6.QtGui import QGuiApplication


def all_screen_rects() -> List[QRect]:
    return [s.availableGeometry() for s in QGuiApplication.screens()]


def union_rect() -> QRect:
    rects = all_screen_rects()
    if not rects:
        return QRect(0, 0, 1920, 1080)
    left   = min(r.left()   for r in rects)
    top    = min(r.top()    for r in rects)
    right  = max(r.right()  for r in rects)
    bottom = max(r.bottom() for r in rects)
    return QRect(left, top, right - left + 1, bottom - top + 1)


def in_any_screen(x: int, y: int) -> bool:
    for r in all_screen_rects():
        if r.contains(x, y):
            return True
    return False


def clamp_to_union(x: int, y: int, w: int, h: int) -> Tuple[int, int]:
    u = union_rect()
    x = max(u.left(),   min(u.right()  - w, x))
    y = max(u.top(),    min(u.bottom() - h, y))
    return x, y


def floor_y_for(x: int, w: int, h: int) -> int:
    """Return the local floor y (bottom of the screen that contains x)."""
    for r in all_screen_rects():
        if r.left() <= x <= r.right():
            return r.bottom() - h
    return union_rect().bottom() - h
