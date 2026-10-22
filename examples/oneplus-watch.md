# OnePlus Watch

## Important: generation matters
The **1st-gen OnePlus Watch (2021)** does **not** run Wear OS. It runs OnePlus's own
RTOS-based firmware (the same lineage as OPPO/Mobvoi hybrid designs of that era), has no standard
adb/package-manager surface, and this project cannot do anything with it.

Only the **OnePlus Watch 2, 2R, and 3** run real Wear OS (dual-chip design: a Snapdragon W5-class
chip running Wear OS 4/5 for smart features, paired with a low-power BES chip handling always-on
watch face and extended battery mode). Everything below applies to those models only — confirm
with `getprop ro.build.version.release` before proceeding; if it doesn't report an Android/Wear OS
version at all, stop, this is the 1st-gen unit.

Status: unverified template — no real-device run logged yet, for the Watch 2/2R/3.

## Connection notes
- Standard Wear OS Developer options path (About → tap build number repeatedly).
- The dual-chip architecture means some "always-on" behavior (the always-on watch face, basic
  step counting) is handled by the low-power BES chip and keeps running even if you disable things
  on the Wear OS side — don't mistake that for a disable not having worked.

## What's actually there to remove
OnePlus's Wear OS skin is relatively light; typical candidates (confirm with `dumpsys package`):
- Any OnePlus-branded preloaded watch-face or wellness-duplicate apps.
- Preloaded game or demo content, if present out of the box.

## Open questions for the next real run
- Full package inventory from a real Watch 2/2R/3 — this file needs a real pass before the
  "commonly reported" category in other examples applies here too.
