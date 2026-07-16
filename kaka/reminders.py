"""Break reminder — iOS-style notification card with snooze / dismiss.

Every ``POMODORO_INTERVAL_S`` Kaka pops a card top-right. The card has
two buttons: **Snooze 5 min** and **Dismiss**.
"""
from __future__ import annotations

import random

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from . import config


class BreakReminder:
    def __init__(self):
        self._timer = QTimer()
        self._timer.timeout.connect(self._pop)
        self._card = None

    def start(self) -> None:
        self._timer.start(config.POMODORO_INTERVAL_S * 1000)

    def stop(self) -> None:
        self._timer.stop()
        self._hide()

    def _pop(self) -> None:
        self._hide()
        text = random.choice(config.POMODORO_BREAK_TEXTS)
        card = QFrame()
        card.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
            | Qt.NoDropShadowWindowHint
        )
        card.setAttribute(Qt.WA_TranslucentBackground, False)
        card.setAttribute(Qt.WA_ShowWithoutActivating)
        card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 250);
                border-radius: 14px;
                border: 1px solid rgba(60,60,67,0.10);
            }
            QLabel#title { font-weight: 600; font-size: 14px; color: #111; }
            QLabel#msg   { font-size: 13px; color: #444; }
            QPushButton {
                background: #F2F2F7; color: #007AFF;
                border: 0; border-radius: 8px;
                padding: 6px 12px; font-size: 13px; font-weight: 600;
            }
            QPushButton:hover { background: #E5E5EA; }
            QPushButton#primary { background: #007AFF; color: #fff; }
            QPushButton#primary:hover { background: #0064D0; }
        """)

        lay = QVBoxLayout(card); lay.setContentsMargins(14, 12, 14, 12); lay.setSpacing(6)
        title = QLabel("🐾 Kaka 提醒"); title.setObjectName("title"); lay.addWidget(title)
        msg = QLabel(text); msg.setObjectName("msg"); msg.setWordWrap(True); lay.addWidget(msg)

        btns = QHBoxLayout(); btns.setSpacing(6)
        snooze = QPushButton("延后 5 分钟")
        dismiss = QPushButton("知道了"); dismiss.setObjectName("primary")
        snooze.clicked.connect(lambda: self._snooze(5))
        dismiss.clicked.connect(self._hide)
        btns.addStretch(1); btns.addWidget(snooze); btns.addWidget(dismiss)
        lay.addLayout(btns)

        card.setFixedWidth(320)
        card.adjustSize()

        screen = QGuiApplication.primaryScreen().availableGeometry()
        card.move(screen.right() - card.width() - 24, screen.top() + 24)
        card.show()
        self._card = card

        # auto-hide after 25s if the user ignores it
        QTimer.singleShot(25000, self._hide)

    def _snooze(self, minutes: int) -> None:
        self._hide()
        QTimer.singleShot(minutes * 60 * 1000, self._pop)

    def _hide(self) -> None:
        if self._card is not None:
            self._card.hide()
            self._card.deleteLater()
            self._card = None
