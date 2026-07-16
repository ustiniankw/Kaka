"""Procedurally drawn pixel-art sprites.

Kaka has no external image assets — everything is painted with QPainter so
the repo stays lean and cross-platform. Feel free to replace these with
real PNGs in ``assets/`` and swap the loader in :mod:`kaka.pet`.
"""
from __future__ import annotations

from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QColor, QPainter, QPixmap, QBrush, QPen, QFont

from .config import PET_SIZE, WASTE_SIZE

# Colour palette
BODY = QColor("#F5C542")
BODY_DARK = QColor("#C08A18")
CHEEK = QColor("#F58A8A")
EYE = QColor("#222222")
WHITE = QColor("#FFFFFF")


def _new_pixmap(size: int) -> QPixmap:
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    return pm


def pet_pixmap(mood: str = "happy", flip: bool = False) -> QPixmap:
    """Return a pixmap of Kaka in a certain mood.

    Parameters
    ----------
    mood: "happy" | "sad" | "sleepy" | "hungry" | "wink"
    flip: mirror horizontally (used when walking left).
    """
    size = PET_SIZE
    pm = _new_pixmap(size)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, False)

    # scale: work on a 16x16 grid and blit to size
    grid = 16
    cell = size / grid

    def rect(x: int, y: int, w: int = 1, h: int = 1, colour: QColor = BODY):
        p.fillRect(QRect(int(x * cell), int(y * cell),
                         int(w * cell), int(h * cell)), colour)

    # body (rounded blob)
    body_cells = [
        (4, 3, 8, 1), (3, 4, 10, 1),
        (2, 5, 12, 6),
        (3, 11, 10, 1), (4, 12, 8, 1),
        # feet
        (4, 13, 3, 1), (9, 13, 3, 1),
    ]
    for (x, y, w, h) in body_cells:
        rect(x, y, w, h, BODY)

    # body shadow (bottom half)
    shadow_cells = [
        (3, 10, 10, 1), (4, 11, 8, 1),
    ]
    for (x, y, w, h) in shadow_cells:
        rect(x, y, w, h, BODY_DARK)

    # eyes
    if mood == "sleepy":
        rect(5, 7, 2, 1, EYE)
        rect(9, 7, 2, 1, EYE)
    elif mood == "wink":
        # left eye normal, right eye closed
        rect(5, 6, 2, 2, WHITE)
        rect(6, 7, 1, 1, EYE)
        rect(9, 7, 2, 1, EYE)
    else:
        rect(5, 6, 2, 2, WHITE)
        rect(9, 6, 2, 2, WHITE)
        rect(6, 7, 1, 1, EYE)
        rect(10, 7, 1, 1, EYE)

    # cheeks
    rect(4, 9, 1, 1, CHEEK)
    rect(11, 9, 1, 1, CHEEK)

    # mouth
    if mood == "sad":
        rect(7, 10, 2, 1, EYE)
        rect(6, 9, 1, 1, EYE)
        rect(9, 9, 1, 1, EYE)
    elif mood == "hungry":
        rect(7, 9, 2, 2, EYE)
    else:
        rect(7, 10, 2, 1, EYE)

    p.end()

    if flip:
        return pm.transformed(_flip_transform())
    return pm


def _flip_transform():
    from PySide6.QtGui import QTransform
    t = QTransform()
    t.scale(-1, 1)
    return t


def poop_pixmap() -> QPixmap:
    size = WASTE_SIZE
    pm = _new_pixmap(size)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setFont(QFont("Segoe UI Emoji", int(size * 0.7)))
    p.drawText(pm.rect(), Qt.AlignCenter, "💩")
    p.end()
    return pm


def pee_pixmap() -> QPixmap:
    size = WASTE_SIZE
    pm = _new_pixmap(size)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setFont(QFont("Segoe UI Emoji", int(size * 0.7)))
    p.drawText(pm.rect(), Qt.AlignCenter, "💦")
    p.end()
    return pm


def food_pixmap(glyph: str) -> QPixmap:
    size = WASTE_SIZE
    pm = _new_pixmap(size)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    p.setFont(QFont("Segoe UI Emoji", int(size * 0.7)))
    p.drawText(pm.rect(), Qt.AlignCenter, glyph)
    p.end()
    return pm
