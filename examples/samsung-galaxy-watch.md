# Samsung Galaxy Watch (One UI Watch, Watch4 and newer)

Status: one short real-device run is documented below for SM-L715U on Android 17.
The general candidate list remains an unverified template for other models and firmware:
check `dumpsys package <name>` before disabling anything.

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

## Real-device report: SM-L715U / Android 17

One device tested on 2026-11-17 using the workflow at commit
`caa2fafe4bb136b4a094c7cf08a08422cd860079`.

- Device-reported model: `SM-L715U`.
- Firmware: `CP2A.260330.023.L715USQS1AZH4`; Android release property: `17`;
  security patch: `2026-08-05`.
- LTE was not in use; telephony and eSIM packages were left enabled.
- Preferences: no contactless payments or voice assistants; retain Samsung Health, stock
  watch faces, always-on display, existing sensor settings, Find My Device and updates.
- This is a short functional check on one firmware, not a universal safe-disable profile.

### Packages disabled and verified after reboot

Each package was inspected with `dumpsys package`, then disabled with its own
`pm disable-user --user 0 <package>` shell invocation. All five were initially enabled
in the default state (`enabled=0`).

| Package | Observed role |
| --- | --- |
| `com.samsung.android.bixby.agent` | Bixby assistant app |
| `com.samsung.android.bixby.wakeup` | Bixby wake-word / invocation component |
| `com.google.android.wearable.assistant` | Google Assistant app declaring a voice-interaction service |
| `com.samsung.android.samsungpay.gear` | Samsung Wallet app and payment/card-emulation services |
| `com.samsung.android.spay` | Samsung Wallet-specific data-sync/session bridge |

The Google Assistant entry above identifies the individually inspected assistant app;
it must not be used as a reason to disable other `com.google.android.wearable.*`
packages. The `spay` bridge above is Wallet-specific, not the watch's general phone bridge.

After one reboot, the disabled-package diff exactly matched these five packages. The
two packages already disabled before the session remained unchanged. No system package
was uninstalled and no app data was cleared.

The watch face, app drawer, tile carousel and Samsung Health home screen were checked
visually and remained usable. No process names matched the five disabled packages in
the final `ps -A` snapshot. Job-scheduler references to them were only in its cached
UID-to-package map; the final alarm dump had no matching package references. This does
not rule out all work performed through shared UIDs or other services.

Samsung account/cloud, Galaxy Store, diagnostics, health/sensor services, stock faces,
companion connectivity, NFC, emergency/safety, Find My Device, updates and telephony/eSIM
were left unchanged. The unverified candidates elsewhere in this file were not all tested.

### Connection and assistant-selection observations

- Wireless debugging dropped repeatedly. Reopening its screen with the watch awake
  allowed reconnection. After reboot the connection port changed; `adb mdns services`
  found the new port for the already paired device. Check device identity before using
  a discovered address, especially when multiple Android devices are advertised.
- Disabling assistants caused Android to clear the `secure assistant` and
  `secure voice_interaction_service` settings. It also changed
  `secure raise_trigger_default_assistant` and `global setting_home_key_long_press`
  to Bixby components even though Bixby was disabled.
- Back up those four settings before changing assistants. Re-enabling packages may
  need to be followed by restoring the original assistant selection and shortcuts, or
  selecting the desired actions in the watch UI. Actual physical-button behavior was
  not tested in this run.
- A local restore script was prepared using `pm enable --user 0`, followed by
  `pm default-state --user 0` for these originally-default packages, and restoration
  of the four assistant settings. The restore path was not exercised on the device.

### Resource snapshots and limits

The final snapshot was taken approximately 223 seconds after boot, after UI checks.

| Metric | Before | After reboot and UI checks |
| --- | ---: | ---: |
| Installed packages | 282 | 282 |
| Disabled packages | 2 | 7 |
| Available RAM (`/proc/meminfo MemAvailable`, MiB) | 231.3 | 361.2 |
| Free RAM (`MemFree`, MiB) | 70.8 | 70.1 |
| Free data storage (`df -k /data`, MiB) | 45,847.3 | 45,920.1 |
| Processes, including kernel threads (`ps -A`) | 587 | 696 |
| CPU utilization (`dumpsys cpuinfo` sampling window) | 19% | 26% |
| Battery level | 83% | 81% |

These are uncontrolled snapshots. Reboot, cache eviction, startup work, foreground UI
checks and wireless debugging affect the results. The RAM increase and storage change
cannot be attributed solely to disabling these apps; APKs and app data were retained.
CPU activity and process count were higher in the final snapshot. Battery-level change
during maintenance is not a battery-life benchmark. Full `batterystats` snapshots were
captured locally, but no comparable full-cycle drain test was performed.

Long-term stability, battery life, restoration, physical shortcuts, and end-to-end
phone sync, notifications, calls, LTE and safety functions remain untested. Retaining
their packages is not a claim that those functions were comprehensively verified.

Only this summarized report is contributed. Backups, raw settings/properties,
diagnostic dumps, network/device identifiers, pairing details, and screenshots are
excluded.
