"""LAN friend visits.

A tiny opt-in UDP broadcast beacon so multiple Kaka instances on the same
LAN can wave at each other. When a Kaka discovers a friend on the local
network, the pet is nudged toward the nearest screen edge and displays a
"👋" bubble.

Runs in a background thread; safe to disable — if the socket setup fails
(e.g. sandboxed OS), we just log & no-op.
"""
from __future__ import annotations

import json
import os
import socket
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


BEACON_PORT = 45871
BEACON_MAGIC = "KAKA_v1"
BROADCAST_INTERVAL_S = 5.0
FRIEND_EXPIRY_S = 30.0


@dataclass
class Friend:
    node_id: str
    name: str
    addr: str
    last_seen: float


@dataclass
class LANFriends:
    my_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    my_name: str = field(default_factory=lambda: os.environ.get("USER", "Kaka"))
    friends: Dict[str, Friend] = field(default_factory=dict)
    on_friend_seen: Optional[Callable[[Friend], None]] = None
    _running: bool = False
    _threads: List[threading.Thread] = field(default_factory=list)
    _rx: Optional[socket.socket] = None
    _tx: Optional[socket.socket] = None

    # ------------------------------------------------------------------ API
    def start(self) -> None:
        try:
            self._rx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._rx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                self._rx.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            except (AttributeError, OSError):
                pass
            self._rx.bind(("", BEACON_PORT))
            self._rx.settimeout(1.0)

            self._tx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._tx.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        except Exception as e:
            print(f"[Kaka] LAN friends disabled: {e}")
            self._rx = self._tx = None
            return

        self._running = True
        t1 = threading.Thread(target=self._broadcast_loop, daemon=True)
        t2 = threading.Thread(target=self._listen_loop, daemon=True)
        t1.start(); t2.start()
        self._threads = [t1, t2]

    def stop(self) -> None:
        self._running = False
        for s in (self._rx, self._tx):
            try:
                if s: s.close()
            except Exception:
                pass

    def active_friends(self) -> List[Friend]:
        now = time.time()
        return [f for f in self.friends.values() if now - f.last_seen < FRIEND_EXPIRY_S]

    # ------------------------------------------------------------------ Internals
    def _broadcast_loop(self) -> None:
        payload = json.dumps({
            "magic": BEACON_MAGIC,
            "id": self.my_id,
            "name": self.my_name,
        }).encode()
        while self._running:
            try:
                self._tx.sendto(payload, ("<broadcast>", BEACON_PORT))
            except Exception:
                pass
            time.sleep(BROADCAST_INTERVAL_S)

    def _listen_loop(self) -> None:
        while self._running:
            try:
                data, addr = self._rx.recvfrom(1024)
            except socket.timeout:
                continue
            except OSError:
                break
            try:
                msg = json.loads(data.decode("utf-8", errors="replace"))
            except Exception:
                continue
            if msg.get("magic") != BEACON_MAGIC or msg.get("id") == self.my_id:
                continue
            fid = msg.get("id", "")
            friend = self.friends.get(fid) or Friend(
                node_id=fid, name=msg.get("name", "?"),
                addr=addr[0], last_seen=time.time(),
            )
            friend.name = msg.get("name", friend.name)
            friend.addr = addr[0]
            new = fid not in self.friends
            friend.last_seen = time.time()
            self.friends[fid] = friend
            if new and self.on_friend_seen:
                try:
                    self.on_friend_seen(friend)
                except Exception:
                    pass
