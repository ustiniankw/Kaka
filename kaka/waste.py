"""Floor entities: poop, pee, food. All are small transparent windows
that live on the desktop and can be clicked to be cleaned / eaten.
"""
from __future__ import annotations

from typing import Callable, Optional

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent, QPixmap
from PySide6.QtWidgets import QLabel, QWidget

from . import sprites
from .config import WASTE_SIZE


class FloorEntity(QLabel):
    """A tiny floating window sitting on the desktop.

    Base class for :class:`Poop`, :class:`Pee`, :class:`Food`.
    """

    KIND: str = "entity"

    def __init__(self, pos: QPoint, pixmap: QPixmap,
                 on_click: Callable[["FloorEntity"], None]):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setFixedSize(WASTE_SIZE, WASTE_SIZE)
        self.setPixmap(pixmap)
        self.setScaledContents(True)
        self._on_click = on_click
        self.move(pos)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._on_click(self)
        super().mousePressEvent(event)


class Poop(FloorEntity):
    KIND = "poop"

    def __init__(self, pos: QPoint, on_click):
        super().__init__(pos, sprites.poop_pixmap(), on_click)


class Pee(FloorEntity):
    KIND = "pee"

    def __init__(self, pos: QPoint, on_click):
        super().__init__(pos, sprites.pee_pixmap(), on_click)


class Food(FloorEntity):
    KIND = "food"

    def __init__(self, pos: QPoint, glyph: str, on_click):
        super().__init__(pos, sprites.food_pixmap(glyph), on_click)
        self.glyph = glyph
