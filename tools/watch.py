#!/usr/bin/env python3
"""
Small adb convenience wrapper for a Wear OS watch, mirroring what the prompt
in PROMPT.md expects to call.

Usage:
    tools/watch.py pair <ip:port> <code>
    tools/watch.py connect <ip:port>
    tools/watch.py shell <command...>
    tools/watch.py --screenshot shots/out.png [key ...]
    tools/watch.py props          # dump getprop, useful for the backup step

Respects WATCH_HOST / WATCH_PORT env vars as an override (e.g. when going
through tools/relay.py from a sandboxed environment):
    WATCH_HOST=127.0.0.1 WATCH_PORT=15555 tools/watch.py shell pm list packages
"""
import os
import subprocess
import sys


def adb(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["adb", *args], capture_output=True, text=True)


def target() -> str | None:
    host = os.environ.get("WATCH_HOST")
    port = os.environ.get("WATCH_PORT")
    if host and port:
        return f"{host}:{port}"
    return None


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    dev = target()
    dev_args = ["-s", dev] if dev else []

    if cmd == "pair":
        if len(sys.argv) != 4:
            print("usage: watch.py pair <ip:port> <code>")
            sys.exit(1)
        result = adb("pair", sys.argv[2], sys.argv[3])
        print(result.stdout + result.stderr)

    elif cmd == "connect":
        if len(sys.argv) != 3:
            print("usage: watch.py connect <ip:port>")
            sys.exit(1)
        result = adb("connect", sys.argv[2])
        print(result.stdout + result.stderr)

    elif cmd == "shell":
        result = adb(*dev_args, "shell", *sys.argv[2:])
        print(result.stdout + result.stderr)
        sys.exit(result.returncode)

    elif cmd == "props":
        result = adb(*dev_args, "shell", "getprop")
        print(result.stdout + result.stderr)

    elif cmd == "--screenshot":
        if len(sys.argv) < 3:
            print("usage: watch.py --screenshot <out.png> [key ...]")
            sys.exit(1)
        out_path = sys.argv[2]
        for key in sys.argv[3:]:
            adb(*dev_args, "shell", "input", "keyevent", key)
        shot = subprocess.run(
            ["adb", *dev_args, "exec-out", "screencap", "-p"],
            capture_output=True,
        )
        if not shot.stdout:
            print("empty screenshot — this screen may not be capturable, see docs/TROUBLESHOOTING.md")
            sys.exit(1)
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(shot.stdout)
        print(f"saved {out_path} ({len(shot.stdout)} bytes)")

    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
