# Mobvoi TicWatch / Fossil (Gen 5, Gen 6)

Status: unverified template — no real-device run logged yet.

## Connection notes
- Both brands run closer-to-stock Wear OS than Samsung, but each layers its own companion suite
  on top (Mobvoi TicHealth/TicExercise, Fossil's Wellness app). Developer options location matches
  the generic Wear OS path (About → tap build number).
- Fossil's older Gen 5 watches (Wear OS, Qualcomm 3100) are slower to respond to adb over Wi-Fi —
  give commands extra time before assuming a hang.

## Commonly reported as safe to disable (verify first)
- Mobvoi's duplicate fitness/health apps if you're using Google Fit or a third-party tracker
  instead of TicHealth.
- Any preloaded partner watch-face apps (common on both brands at launch, e.g. Facer-branded
  bundles) if you don't use their faces.

## Keep enabled
- The core TicWear / Fossil companion sync service that bridges to the phone app — same caution
  as every other brand here: this is the one package category that breaks pairing entirely if
  disabled.

## Open questions for the next real run
- Mobvoi has shipped both Wear OS and its own older proprietary OS on different models (early
  TicWatch GTs) — confirm `getprop ro.build.version.release` shows a real Wear OS/Android version
  before running the debloat steps at all.
