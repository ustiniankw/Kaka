"""Anthropomorphic pomodoro reminder.

Every ``POMODORO_INTERVAL_S`` seconds Kaka pops a small toast bubble in
the corner suggesting the user takes a break.
"""
from __future__ import annotations

import random

from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QLabel

from . import config


class BreakReminder:
    def __init__(self):
        self._timer = QTimer()
        self._timer.timeout.connect(self._pop)
        self._label = None

    def start(self) -> None:
        self._timer.start(config.POMODORO_INTERVAL_S * 1000)

    def stop(self) -> None:
        self._timer.stop()
        self._hide()

    def _pop(self) -> None:
        text = random.choice(config.POMODORO_BREAK_TEXTS)
        self._hide()
        lbl = QLabel(f"🐾  {text}")
        lbl.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
            | Qt.NoDropShadowWindowHint
        )
        lbl.setAttribute(Qt.WA_TranslucentBackground)
        lbl.setAttribute(Qt.WA_ShowWithoutActivating)
        lbl.setStyleSheet(
            "QLabel {"
            " background-color: rgba(255, 240, 200, 235);"
            " color: #4a2f00;"
            " padding: 10px 16px;"
            " border-radius: 12px;"
            " font-size: 14px;"
            " font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;"
            "}"
        )
        lbl.adjustSize()
        screen = QGuiApplication.primaryScreen().availableGeometry()
        lbl.move(
            screen.right() - lbl.width() - 24,
            screen.top() + 24,
        )
        lbl.show()
        self._label = lbl
        QTimer.singleShot(6000, self._hide)

    def _hide(self) -> None:
        if self._label is not None:
            self._label.hide()
            self._label.deleteLater()
            self._label = None
