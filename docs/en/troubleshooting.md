# Troubleshooting

**nginx 502** — the web server is up but the inner Tiiny service hasn't started yet. Typical right
after power-on (first boot is slow) or during an update. Wait; if needed, launch the TiinyOS app,
which authorizes the backend.

**Agent store empty / `is_activated:false`** — incomplete activation or an update in progress. Finish
sign-in in the app, let the update finish, restart the app.

**0 models in `/v1/models`** — normal after a power cycle; models reload shortly, or launch one with
`POST /api/v1/models/<id>/launch`.

**Model not running after every power-on** — the box does not always auto-relaunch the last model.
Re-launch it (API or app) after each boot.

**Stuck OTA update** — OS updates are large `.raucb` images driven by the **desktop app in coordination
with the Tiiny cloud**; there is no public API or CLI for the OS update, and the box has no shell. A
stuck image pull is often cleared by a hardware reboot (power button); OTA frequently self-pauses after
a pause. The app keeps update state locally (desktop app support dir, `update-state.json`).

**"PC Server package signature could not be verified"** — seen on some desktop-app versions; often
harmless. Downgrading the desktop app can work around it.

**Internet sharing breaks detection** — sharing the host's internet over the USB bridge can stop the
desktop "PC Server" from detecting the box (`current_device_missing_from_pc_service_snapshot`). Disable
internet sharing on that interface.

**Shutdown from the app doesn't power off** — a stuck process can block it. Alternatives:
`POST /api/v1/sys/shutdown/`, or hold the power button ~10 s.

**Finding the box after a DHCP change** — query `http://<ip>:39218/device.json`, or scan the subnet
for port 80 and match `GET /api/v1/sys/device_info` (`device_model_name` starts with `Tiiny`).
