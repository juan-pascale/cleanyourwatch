# The prompt

Paste this into Claude Code (or another coding assistant with shell access) on a computer that is
on the same Wi-Fi as the watch. Targets Wear OS watches: Samsung Galaxy Watch (4 and newer, One UI
Watch), Pixel Watch, Mobvoi TicWatch, Fossil Gen 5/6, OnePlus Watch 2/2R/3. It will not work on the
1st-gen OnePlus Watch, Galaxy Watch Active/3 or older (Tizen, not Wear OS), Garmin, Amazfit/Zepp OS,
or Apple Watch.

Before you start, on the watch: Settings → System → About → tap "Versions" or the build number
repeatedly (7 times) → back out → Developer options → turn on ADB debugging. Most watches have no
USB data port, so you'll pair over Wi-Fi: if you see "Wireless debugging," open it, choose "Pair new
device" and keep the code and IP:port on screen. If you only see "Debug over Wi-Fi," turn it on and
note the IP it shows. Keep the watch on its charger and the screen awake for the whole session —
Wear OS sleeps aggressively and will drop Wi-Fi debugging the moment the screen times out or Wi-Fi
is turned off to save battery while connected to the phone over Bluetooth. If the watch's Wi-Fi
radio is set to "only when disconnected from phone," switch it to always-on for this session and
remember to revert it after.

---

I want to debloat my Wear OS watch and claw back battery life. My watch model is:
<MODEL NAME HERE>. Work on the real device, step by step, and verify everything you do with
screenshots pulled from the watch. Ask me before anything that depends on my preferences.

Connect
- If Developer options shows "Wireless debugging": ask me for the pairing code and the pairing
  IP:port, run `adb pair <ip:port> <code>`, then ask for the connect IP:port (sometimes different
  from the pairing one) and run `adb connect <ip:port>`.
- If it only shows "Debug over Wi-Fi" with a single IP, connect on port 5555: `adb connect <ip>:5555`.
- If neither network option is visible, the watch may need its one-time first pairing over USB
  (rare — some Samsung models ship a USB-C charging puck with data lines). Ask me before assuming a
  watch has no way to enable it.
- If `adb` fails with "No route to host" on macOS even though the watch answers a ping, that's
  macOS Local Network privacy blocking adb, not a real network problem. Don't debug the network:
  use the Python `adb-shell` package in a venv as the client instead.
- If your own commands can't reach the watch at all while it answers from an ordinary terminal (a
  sandbox that blocks the local network), ask me to run `tools/relay.py <watch ip> <port>` in a
  terminal and leave it running, then use `WATCH_HOST=127.0.0.1 WATCH_PORT=<relay port>`.
- Tell me when the watch will show a pairing confirmation or fingerprint prompt so I can accept it
  — on a round display with a tiny keyboard, it's easy to miss.
- Wireless debugging silently drops whenever Wi-Fi drops, the watch goes into ambient/sleep for too
  long, or the companion phone app decides to put the Bluetooth link first. If a command suddenly
  times out mid-session, re-pair before assuming anything else broke.

Back up first
- Save the full package list, disabled-package list, `getprop` output, and current battery/display
  settings to a backup folder before changing anything, and write a restore script that re-enables
  everything you disable.
- Ask me whether this watch has cellular (LTE) service, since some connectivity and eSIM-management
  packages that look disposable on a Bluetooth-only watch are load-bearing on a cellular one.
- When you finish for the session, turn ADB debugging back off on the watch and revoke
  authorizations, unless I say I want it to stay on for more changes later.

Debloat
- List installed packages and sort them into: OEM account/sync services (Samsung Account, Samsung
  Cloud, Fossil HQ sync, TicWear/TicHealth companion duplicates), OEM app stores and "Galaxy
  Store"-style add-on managers, preloaded first-party apps I don't use (Bixby, Samsung Pay, Samsung
  Internet, Facer or other preloaded watch-face apps, games), and background telemetry/analytics.
- Disable with `pm disable-user --user 0`, never uninstall system packages.
- Never disable what the watch needs to work: Wear OS system services (`com.google.android.wearable.*`),
  Google Play Services and Play Store, the companion-app bridge (Wear OS app / Galaxy Wearable sync
  service), Bluetooth and Wi-Fi stack services, fall detection and emergency SOS if the watch has
  it, the watch face picker/complication host, and — on a cellular model — the telephony and eSIM
  services. Package names rarely say what they do: check `dumpsys package <name>` for its declared
  activities/services before disabling, and ask me if it's still unclear.
- Samsung watches specifically: Samsung Health itself is usually worth keeping (it owns fitness
  tracking and sensor permissions other apps rely on), but its duplicate sync/upload services,
  Samsung Pay, Bixby, Good Lock plugins, and Samsung's own app store are common no-loss removals.
  Confirm with me which Samsung services you're about to touch before disabling in that family —
  it's the most interconnected OEM layer of the ones this targets.
- Before touching the voice assistant, Google Pay/wallet, Find My Device, or firmware update
  services, ask me which ones I use with a checklist question and disable only what I don't tick.
- Run `pm` commands one per shell call; chained commands can silently stop after the first.
- If `pm disable-user` is refused for every package you try, stop and tell me rather than retrying:
  some OEM builds lock package state down further than Android TV firmware does, and there may be
  nothing left to debloat without root.
- Disable in small batches and screenshot (or check `dumpsys activity activities`) between them —
  Wear OS has far fewer visible UI surfaces than a TV, so a broken batch is easy to miss until the
  watch face or tile carousel stops responding.
- After the last batch, reboot once and diff `pm list packages -d` against what you disabled —
  some OEM firmware re-enables specific packages on every boot.

Battery and display
- This is the bigger win on a watch than on a TV: check `dumpsys batterystats` before you start and
  again at the end so I can see the difference.
- Ask me about always-on display: it's usually the single biggest battery cost. Offer to disable it
  outright, or to switch the watch's AOD style to a low-pixel-count face if the watch supports that
  as an alternative.
- Ask me which sensors I actually use (continuous heart rate, SpO2, skin temperature) — background
  sampling for ones I don't use is pure battery drain with no user-visible feature behind it.
- Check for OEM sync services polling location or the network on a schedule (`dumpsys
  jobscheduler` / `dumpsys alarm` filtered to disabled-adjacent packages) and flag any that are
  still running jobs after being disabled.
- There is no supported way to replace the system launcher or app-drawer on stock Wear OS the way
  there is on Android TV — don't attempt it, and don't install a third-party "launcher" APK that
  claims to do this without root. Offer the achievable version instead: set a minimal first-party
  watch face, disable OEM complications/widgets I don't use, and tidy the tile carousel.

Verify
- After each change, take a screenshot: `adb exec-out screencap -p > shot.png` and look at it. Fix
  what you see before moving on.
- Some screens report success without changing anything — confirm state (`pm list packages -d`,
  `dumpsys batterystats`) rather than trusting a command's exit code alone.
- When done, give me a restore script, and a README noting what was disabled, what battery delta
  you measured, and how to re-enable anything.

---

Expect to answer a handful of checklist questions (which OEM services you actually use, which
sensors to keep always-on, whether to touch always-on display). Everything is reversible via
`pm enable`.
