"""Application entry point — wires together the pet, world, menu, and
the boss key + break reminder subsystems.
"""
from __future__ import annotations

import signal
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication

from . import menu as menu_mod
from .config import BOSS_KEY_COMBO
from .hotkeys import BossKey
from .pet import Pet
from .reminders import BreakReminder
from .stats import Stats
from .world import World


def main() -> int:
    # Allow Ctrl+C in the terminal to kill the app
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    stats = Stats.load()
    pet = Pet(stats)
    world = World(pet, stats)

    # -------------------------------------------------- right-click menu
    def on_menu(pos):
        menu_mod.build_and_show(pet, world, stats, pos, on_quit=app.quit)

    pet.request_context_menu.connect(on_menu)

    # -------------------------------------------------- boss key
    def toggle_visible():
        pet.setVisible(not pet.isVisible())

    boss = BossKey(BOSS_KEY_COMBO, toggle_visible)
    boss.start()

    # -------------------------------------------------- pomodoro reminder
    reminder = BreakReminder()
    reminder.start()

    # -------------------------------------------------- graceful shutdown
    def _cleanup():
        try:
            stats.save()
        finally:
            reminder.stop()
            boss.stop()
            world.teardown()

    app.aboutToQuit.connect(_cleanup)

    pet.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
