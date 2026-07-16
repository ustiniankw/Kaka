"""Application entry point."""
from __future__ import annotations

import signal
import sys

from PySide6.QtWidgets import QApplication

from . import menu as menu_mod, skins as skins_mod, sprites
from .config import BOSS_KEY_COMBO
from .friends import LANFriends
from .hotkeys import BossKey
from .pet import Pet
from .reminders import BreakReminder
from .stats import Stats
from .world import World


def main() -> int:
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    stats = Stats.load()

    # ---- apply saved skin ----
    all_skins = skins_mod.all_skins()
    skin = all_skins.get(stats.skin_key, all_skins["default"])
    sprites.set_palette(skin.colors)
    frames = {}
    for mood in list(skin.frames.keys()):
        pm = skin.load_frame(mood)
        if pm is not None:
            frames[mood] = pm
    sprites.set_frame_overrides(frames)

    pet = Pet(stats)
    world = World(pet, stats)

    # ---- LAN friends ----
    friends = LANFriends()
    def on_friend(f):
        try:
            pet.setToolTip(f"👋 {f.name} ({f.addr})")
        except Exception:
            pass
    friends.on_friend_seen = on_friend
    friends.start()

    def on_menu(pos):
        menu_mod.build_and_show(pet, world, stats, pos,
                                on_quit=app.quit, friends=friends)
    pet.request_context_menu.connect(on_menu)

    def toggle_visible():
        pet.setVisible(not pet.isVisible())
    boss = BossKey(BOSS_KEY_COMBO, toggle_visible)
    boss.start()

    reminder = BreakReminder()
    reminder.start()

    def _cleanup():
        try:
            stats.save()
        finally:
            reminder.stop(); boss.stop()
            friends.stop()
            world.teardown()
    app.aboutToQuit.connect(_cleanup)

    pet.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
