# OTA upgrade — the field guide

The official quick start makes updating sound like one button. In practice an OS (firmware) upgrade is
a **multi-stage, cloud-coordinated** process that can stall in several ways. This page is what the
quick start leaves out, based on walking a box from an older firmware up to **0.1.39**.

## How it actually works

- OS upgrades are large **`.raucb` images** (tens of minutes to download and apply), driven by the
  **desktop app in coordination with the Tiiny cloud**. There is **no public API or CLI** for the OS
  update, and the box has **no shell** — you drive it from the desktop app.
- It climbs in **steps**, not one jump: e.g. `0.1.33 → 0.1.35 → … → 0.1.39`. Each step downloads,
  applies, and reboots; expect several reboots.
- After each OS step the box often re-downloads **new model versions**, which adds more time.

## Where the state lives (host, macOS paths)

| What | Path |
|---|---|
| Update state machine | `~/Library/Application Support/tiiny-ai/update-state.json` |
| Desktop app logs | `~/Library/Application Support/TiinyOS/logs` |
| PC Server request log | `/etc/pcsvr/logs/requests.jsonl` |

`update-state.json` holds the current `phase` and `upgrade_process.os_download_progress`. When things
go wrong you'll see values like `paused`, `cancelInProgress`, or `Cancellation failed` here.

## Driving the OS update via the PC Server API

While the desktop app ("PC Server") is running, the OS-upgrade coordinator is reachable on the host at
`http://hardware-upgrade.api.tiiny` (routed through the PC Server, **not** over the plain LAN IP):

```
GET  /api/upgrade/status
POST /api/upgrade/resume_prepare
POST /api/upgrade/pause_prepare
```

Use these to inspect and nudge a run that the UI has gotten confused about.

## Failure modes we actually hit (and the fix)

**"PC Server package signature could not be verified" (app 1.0.3)**
The newer desktop app threw this and then update/feedback calls failed. A manual `codesign -R` check
actually passes, so it looks like an app bug. **Workaround:** downgrade the desktop app to a known-good
version (0.9.6 in our case; the installer pkg sits on the mounted Tiiny volume), do the upgrade, then go
back. The signature warning can persist cosmetically on 1.0.3 even when things work.

**`hardware-upgrade` service hangs (timeouts / 502)**
The on-box upgrade service stalled and returned 502s. **Fix:** reboot the box with the **power button**.

**Stuck image pull ("获取镜像 manifest…")**
The box hangs while pulling a container image during prepare. **Fix:** reboot the box with the power
button. Note the OTA frequently **self-pauses after a pause** — re-issue `resume_prepare` or restart the
step.

**Internet sharing breaks detection**
If the Mac is sharing its internet over the USB bridge (`bridge100`), the PC Server stops seeing the box
(`current_device_missing_from_pc_service_snapshot`) and the update can't proceed. **Fix:** turn off
internet sharing on that interface.

**Update wedged in `paused` / `cancelInProgress` / "Cancellation failed"**
The cleanest reset: **Cmd+Q the TiinyOS app**, then — with the app closed — back up and **delete
`update-state.json`**, and start fresh. The OS update is optional; you can also just leave the box on the
firmware it's on.

## Practical tips

- Give it time and power: the first boot after a step is slow, and a 502 right after a reboot usually
  just means the inner service hasn't come up yet — wait before touching anything.
- Keep the box on the **same Wi-Fi** throughout, on its own power (not only USB-tethered).
- After the whole thing settles, a model may **not auto-launch** — start it again via the app or
  `POST /api/v1/models/<id>/launch`.
