#!/usr/bin/env python3
"""
Local TCP relay for environments that block LAN access (e.g. a sandboxed coding
assistant). Run this on a machine that *can* reach the watch, then point the
assistant's adb client at 127.0.0.1:<relay-port> instead of the watch's real
address.

Usage:
    tools/relay.py <watch-ip> <watch-port> [relay-port]

Example:
    tools/relay.py 192.168.1.42 5555 15555
    # then: adb connect 127.0.0.1:15555
"""
import socket
import sys
import threading


def pump(src: socket.socket, dst: socket.socket) -> None:
    try:
        while True:
            data = src.recv(4096)
            if not data:
                break
            dst.sendall(data)
    except OSError:
        pass
    finally:
        for sock in (src, dst):
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            sock.close()


def handle(client: socket.socket, target_host: str, target_port: int) -> None:
    try:
        upstream = socket.create_connection((target_host, target_port), timeout=10)
    except OSError as exc:
        print(f"[relay] could not reach {target_host}:{target_port}: {exc}")
        client.close()
        return
    threading.Thread(target=pump, args=(client, upstream), daemon=True).start()
    threading.Thread(target=pump, args=(upstream, client), daemon=True).start()


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    target_host = sys.argv[1]
    target_port = int(sys.argv[2])
    relay_port = int(sys.argv[3]) if len(sys.argv) > 3 else 15555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", relay_port))
    server.listen(5)
    print(f"[relay] listening on 127.0.0.1:{relay_port} -> {target_host}:{target_port}")
    print("[relay] leave this running; Ctrl+C to stop")

    try:
        while True:
            client, _ = server.accept()
            threading.Thread(
                target=handle, args=(client, target_host, target_port), daemon=True
            ).start()
    except KeyboardInterrupt:
        print("\n[relay] stopped")


if __name__ == "__main__":
    main()
