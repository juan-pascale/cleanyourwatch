# Troubleshooting

## Wireless debugging won't stay connected
Wear OS suspends radios aggressively to save battery. If `adb` starts timing out mid-session:
- Confirm the watch screen hasn't gone to sleep — tap it or keep it on the charger with
  "stay awake while charging" enabled in Developer options.
- Check the watch hasn't dropped Wi-Fi in favor of its Bluetooth link to the phone:
  `adb shell dumpsys wifi | grep -i "mNetworkInfo"` or just check the Wi-Fi icon on the watch face.
- Some watches turn Wi-Fi fully off a minute or two after the phone reconnects over Bluetooth, by
  design. You may need to repeat the pairing flow more than once per session.

## `pm disable-user` succeeds but nothing changes
Confirm state directly instead of trusting the exit code:
```
adb shell pm list packages -d
```
If the package isn't listed as disabled despite a "Success" response, something (often an OEM
device-admin component) is re-enabling it. Check `dumpsys package <name>` for a device-admin or
device-owner flag before assuming the command itself failed.

## Screenshot comes back empty
A handful of secure/system surfaces (lock screen, some OEM always-on-display renderers) return a
blank or zero-byte capture from `screencap`, the same way DRM-protected video does on a phone.
That's the surface, not a broken debloat. Confirm what's actually in focus instead:
```
adb shell dumpsys activity activities | grep topResumedActivity
```

## Watch won't rejoin the phone / Bluetooth sync breaks after a disable
If you disabled anything under the companion-app bridge package (the Wear OS app's on-watch
service, or Galaxy Wearable's equivalent), re-enable it immediately:
```
adb shell pm enable --user 0 <package>
```
then unpair/re-pair from the phone's companion app if the link doesn't recover on its own.

## macOS says "No route to host" even though the watch answers a ping
This is macOS's Local Network privacy permission blocking the system `adb` binary, not a real
network issue. Either grant Local Network access to your terminal app in System Settings →
Privacy & Security, or use the Python `adb-shell` package instead of the stock adb client.

## No Wireless debugging / Debug over Wi-Fi option at all
A few OEM skins hide it behind a region or carrier variant, or require Google account sign-in on
the watch first (first-time setup must be complete). If it's genuinely absent after full setup,
the watch likely doesn't support ADB over the air and this tool can't reach it without a USB data
connection, which most Wear OS watches don't expose.
