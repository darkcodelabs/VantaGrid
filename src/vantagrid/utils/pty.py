from __future__ import annotations

import asyncio
import fcntl
import os
import pty
import signal
import struct
import termios
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class PtyProcess:
    pid: int
    fd: int
    env: dict[str, str] = field(default_factory=dict)

    def write(self, data: bytes) -> None:
        os.write(self.fd, data)

    def read(self, size: int = 4096) -> bytes:
        return os.read(self.fd, size)

    def resize(self, rows: int, cols: int) -> None:
        winsize = struct.pack("HHHH", rows, cols, 0, 0)
        fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)

    def kill(self) -> None:
        try:
            os.kill(self.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

    def is_alive(self) -> bool:
        try:
            os.kill(self.pid, 0)
            return True
        except ProcessLookupError:
            return False


def spawn_claude(
    config_dir: Path,
    working_dir: Path,
    extra_env: dict[str, str] | None = None,
) -> PtyProcess:
    env = os.environ.copy()
    env["CLAUDE_CONFIG_DIR"] = str(config_dir)
    if extra_env:
        env.update(extra_env)

    pid, fd = pty.openpty()
    child_pid = os.fork()
    if child_pid == 0:
        os.setsid()
        os.dup2(fd, 0)
        os.dup2(fd, 1)
        os.dup2(fd, 2)
        os.chdir(str(working_dir))
        os.execvpe("claude", ["claude"], env)
    else:
        return PtyProcess(pid=child_pid, fd=pid, env=env)


async def read_pty_async(proc: PtyProcess, size: int = 4096) -> bytes:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, proc.read, size)
