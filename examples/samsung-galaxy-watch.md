# Samsung Galaxy Watch (One UI Watch, Watch4 and newer)

Status: unverified template — no real-device run logged yet. Treat every package name below as a
starting point to check with `dumpsys package <name>` before disabling, not a confirmed list.

## Connection notes
- Developer options is under Settings → About watch → Software → tap "Software version" 7 times.
- Shows as "Wireless debugging," same pairing-code flow as a Samsung phone.
- Samsung Account must be signed in during first setup for Wireless debugging to reliably persist
  across reboots on some firmware.

## Commonly reported as safe to disable (verify first)
These are frequently cited in community Wear OS debloat threads — confirm each with `dumpsys
package` on the actual unit before touching it, since One UI Watch versions vary by region and year:
- `com.samsung.android.bixby.agent`, `com.samsung.android.bixby.service` — Bixby
- `com.samsung.android.spay` — Samsung Pay / Samsung Wallet (skip if you use it)
- `com.sec.android.app.samsungapps` — Galaxy Store
- `com.samsung.android.app.watchmanager` plugins unrelated to core sync (Good Lock-style extras)

## Keep enabled
- `com.samsung.android.wear.shealth` and its core sync service — Samsung Health owns sensor
  permissions other features depend on, even if you don't use the app's UI.
- Anything under `com.samsung.android.wear.sapps` that's flagged as the Galaxy Wearable bridge —
  this is the phone-pairing link; disabling it breaks notifications and the sync app entirely.
- Fall detection / SOS services if the watch supports them.

## Open questions for the next real run
- Exact package set differs between a Watch4/5 (Wear OS 3) and Watch6/7/Ultra (Wear OS 4/5) —
  log both separately in SHOWCASE.md once tested.
- Confirm whether disabling Bixby breaks the physical side-button shortcut, or just the voice
  assistant.
