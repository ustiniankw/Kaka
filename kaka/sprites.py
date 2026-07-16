"""Procedurally drawn pixel-art sprites.

The palette can be overridden globally with :func:`set_palette` — that's
what the skin system uses.
"""
from __future__ import annotations

from typing import Dict, Optional

from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QColor, QPainter, QPixmap, QFont, QTransform

from .config import PET_SIZE, WASTE_SIZE

# Default palette
_DEFAULTS: Dict[str, QColor] = {
    "body":  QColor("#F5C542"),
    "dark":  QColor("#C08A18"),
    "cheek": QColor("#F58A8A"),
    "eye":   QColor("#222222"),
    "white": QColor("#FFFFFF"),
}
_CURRENT: Dict[str, QColor] = dict(_DEFAULTS)

# Optional PNG frame lookup (mood -> QPixmap)
_FRAME_OVERRIDES: Dict[str, QPixmap] = {}


def set_palette(colors: Dict[str, QColor]) -> None:
    global _CURRENT
    merged = dict(_DEFAULTS)
    merged.update(colors)
    _CURRENT = merged


def set_frame_overrides(frames: Dict[str, QPixmap]) -> None:
    global _FRAME_OVERRIDES
    _FRAME_OVERRIDES = dict(frames)


def _new_pixmap(size: int) -> QPixmap:
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    return pm


def pet_pixmap(mood: str = "happy", flip: bool = False,
               rotation: float = 0.0) -> QPixmap:
    # If a PNG frame is provided for this mood, use it wholesale
    if mood in _FRAME_OVERRIDES:
        pm = _FRAME_OVERRIDES[mood]
    else:
        pm = _draw_procedural(mood)

    if flip or abs(rotation) > 0.01:
        t = QTransform()
        if flip:
            t.scale(-1, 1)
        if abs(rotation) > 0.01:
            t.rotate(rotation)
        pm = pm.transformed(t, mode=Qt.SmoothTransformation)
    return pm


def _draw_procedural(mood: str) -> QPixmap:
    size = PET_SIZE
    pm = _new_pixmap(size)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, False)
    grid = 16
    cell = size / grid

    def R(x, y, w=1, h=1, colour: QColor = None):
        p.fillRect(QRect(int(x*cell), int(y*cell), int(w*cell), int(h*cell)), colour)

    B = _CURRENT["body"]; D = _CURRENT["dark"]; C = _CURRENT["cheek"]
    E = _CURRENT["eye"];  W = _CURRENT["white"]

    R(4,3,8,1,B); R(3,4,10,1,B); R(2,5,12,6,B)
    R(3,11,10,1,B); R(4,12,8,1,B)
    R(4,13,3,1,B); R(9,13,3,1,B)
    R(3,10,10,1,D); R(4,11,8,1,D)

    if mood == "sleepy":
        R(5,7,2,1,E); R(9,7,2,1,E)
    elif mood == "wink":
        R(5,6,2,2,W); R(6,7,1,1,E); R(9,7,2,1,E)
    elif mood == "angry":
        R(4,5,2,1,E); R(10,5,2,1,E); R(5,7,2,1,E); R(9,7,2,1,E)
    else:
        R(5,6,2,2,W); R(9,6,2,2,W)
        R(6,7,1,1,E); R(10,7,1,1,E)

    R(4,9,1,1,C); R(11,9,1,1,C)

    if mood == "sad":
        R(7,10,2,1,E); R(6,9,1,1,E); R(9,9,1,1,E)
    elif mood == "hungry":
        R(7,9,2,2,E)
    elif mood == "working":
        R(7,10,2,1,E); R(6,9,1,1,W); R(9,9,1,1,W)
    else:
        R(7,10,2,1,E)

    p.end()
    return pm


def poop_pixmap() -> QPixmap:  return _emoji("💩", WASTE_SIZE)
def pee_pixmap()  -> QPixmap:  return _emoji("💦", WASTE_SIZE)
def food_pixmap(g: str) -> QPixmap:  return _emoji(g, WASTE_SIZE)
def work_status_pixmap(g: str) -> QPixmap: return _emoji(g, int(WASTE_SIZE * 0.9))


def _emoji(glyph: str, size: int) -> QPixmap:
    pm = _new_pixmap(size)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setFont(QFont("Segoe UI Emoji", int(size * 0.7)))
    p.drawText(pm.rect(), Qt.AlignCenter, glyph)
    p.end()
    return pm
