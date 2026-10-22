# Pixel Watch (1, 2, 3)

Status: unverified template — no real-device run logged yet.

## Connection notes
- Closest to stock Wear OS of any device this project targets; Developer options and Wireless
  debugging behave the same as a Pixel phone.
- No data-capable charging puck — Wireless debugging is the only path in.

## What's actually there to remove
Pixel Watch ships closer to AOSP Wear OS than any other brand here, so the debloat win is smaller.
Realistic candidates, confirm with `dumpsys package` first:
- Fitbit app/services, if you don't use Fitbit for fitness tracking (Pixel Watch's fitness stack
  overlaps with it since the Fitbit acquisition).
- Any preloaded sample/demo tiles left over from setup.

## Keep enabled
- Everything under `com.google.android.wearable.*` — this is Wear OS itself, not OEM bloat.
- Google Assistant, if you use voice actions on the watch — ask before disabling.

## Open questions for the next real run
- Whether there's anything meaningful left to debloat beyond Fitbit integration — this device may
  mostly be a "battery and display tuning" candidate rather than a debloat one.
