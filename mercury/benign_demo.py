"""Benign network demo: local echo server/client for learning only.

This demo is intentionally local-only (binds to localhost). It demonstrates
basic socket flows and can be used in an isolated lab environment.
"""
import socket
import threading
import time
from typing import Optional


class EchoServer:
    """A controllable local-only echo server used for benign demos.

    Use `start()` to run the server in the background and `stop()` to stop it.
    """
    def __init__(self, host: str = "127.0.0.1", port: int = 9001):
        self.host = host
        self.port = port
        self._server = None
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

    def _handler(self, conn, addr):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)

    def _run(self):
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.host, self.port))
        self._server.listen(5)
        try:
            while not self._stop_event.is_set():
                try:
                    self._server.settimeout(1.0)
                    conn, addr = self._server.accept()
                    threading.Thread(target=self._handler, args=(conn, addr), daemon=True).start()
                except socket.timeout:
                    continue
        finally:
            try:
                self._server.close()
            except Exception:
                pass

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self, timeout: float = 2.0):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=timeout)


def echo_client_send(message: str, host: str = "127.0.0.1", port: int = 9001, timeout: float = 2.0) -> str:
    s = socket.create_connection((host, port), timeout=timeout)
    with s:
        s.sendall(message.encode())
        resp = s.recv(4096)
    return resp.decode()
