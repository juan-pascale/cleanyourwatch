# CleanYourWatch

Debloat your Wear OS watch and get battery life back, over ADB, no root. Inspired by
[cleanyourtv](https://cleanyour.tv) (same idea, applied to Android TV).

## What this is
A prompt you paste into Claude Code (or another coding assistant with shell access) along with
your watch model. It connects to your watch over Wi-Fi via ADB wireless debugging, lists what's
installed, asks which OEM services you actually use, and disables the rest with
`pm disable-user` — reversible, no root, no uninstalling system packages.

Unlike Android TV, Wear OS doesn't support swapping the system launcher without root, so this
project doesn't attempt a cosmetic home-screen rebuild the way cleanyourtv does. The real win on a
watch is different anyway: OEM account/sync bloat, preloaded apps you didn't ask for, and —
usually the biggest one — background services and always-on-display settings quietly draining the
battery.

## Targets
- Samsung Galaxy Watch, Watch4 and newer (One UI Watch / Wear OS)
- Pixel Watch (1, 2, 3)
- Mobvoi TicWatch (Wear OS models)
- Fossil Gen 5 / Gen 6
- OnePlus Watch 2, 2R, 3 (**not** the 1st-gen OnePlus Watch — see [examples/oneplus-watch.md](examples/oneplus-watch.md))

Won't work on Tizen-based Galaxy Watches (Active/3 and earlier), Garmin, Amazfit/Zepp OS, or Apple
Watch — none of those run Wear OS.

## Status
Early/unverified. The connection flow and `pm` mechanics in [PROMPT.md](PROMPT.md) are standard
Android behavior and should hold across devices. The per-brand package lists in `examples/` are
seed templates from general knowledge, not yet confirmed against real hardware — they need actual
runs logged before they can be trusted the way cleanyourtv's device-specific notes are. If you run
this against a real watch, please contribute back what you found (see below).

## Use it
1. Read the setup block at the top of [PROMPT.md](PROMPT.md) and enable ADB/Wireless debugging on
   your watch.
2. Paste the prompt into Claude Code, filling in your watch model.
3. Answer its checklist questions (which OEM services you use, whether to touch always-on
   display and which sensors to keep sampling).
4. Everything it disables is reversible with `adb shell pm enable --user 0 <package>` — the
   assistant will also hand you a restore script.

## Repo layout
- `PROMPT.md` — the actual prompt to paste.
- `tools/watch.py` — adb convenience wrapper (pair/connect/shell/screenshot).
- `tools/relay.py` — local TCP relay for sandboxed environments that block LAN access.
- `docs/TROUBLESHOOTING.md` — known gotchas (wireless debugging dropping, empty screenshots, etc).
- `examples/` — per-brand notes; currently seed templates, growing as real runs get logged.

## Contributing
If you run this on a real watch, open a PR updating the matching file in `examples/` with what you
actually found — confirmed package names, anything that broke, anything the prompt got wrong for
your model. That's how cleanyourtv's device list grew to 227 TVs; this one starts at zero.

## License
MIT — see [LICENSE](LICENSE).
