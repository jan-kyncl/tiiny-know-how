# Networking & access

The box runs **nginx on port 80** in front of a FastAPI backend. There is no HTTPS and no admin web
page — everything is the HTTP API. You can reach port 80 over any of three transports.

## 1. Wi-Fi (normal LAN client)

The box joins your home Wi-Fi and gets a DHCP address. This is the usual way to use it headless.

```
http://<ip>/...        Host header selects the service, Bearer token authenticates
```

Because it is DHCP, the address can change; set a DHCP reservation on your router (by the box's Wi-Fi
MAC) if you want it fixed.

## 2. USB-C gadget (to a host computer)

Plugging the box into a computer's USB-C port exposes an **RNDIS / USB-Ethernet gadget** (interface
`usb0`). The box takes a fixed small subnet (the exact `/30` differs per unit, e.g.
`172.20.204.136/30` with device `.137` and host `.138`). Lower latency than Wi-Fi, but only while
tethered, and the host desktop app ("PC Server") also uses this path.

## 3. USB-C Ethernet adapter (box joins LAN by cable) ✅

Plug a **USB-C → Ethernet adapter into the _second_ USB-C port** (the one that is *not* the
"to PC" gadget port). The box brings up an ordinary `eth0` with a **normal LAN DHCP address**, and the
full API is reachable over it exactly like Wi-Fi — just with a stable, faster wired link.

- A 2.5 GbE adapter works.
- Only the HTTP API (port 80) and SSH (3588) are exposed this way — the internal per-model ports are
  **not** opened on `eth0` either, so the adapter buys you stability and speed, not "more ports".
- An earlier community claim that "the adapter does nothing without an intermediary" was wrong.

## Discovery

Every interface answers a discovery endpoint:

```
http://<ip>:39218/device.json
```

It returns the device name, serial, and **all current interface addresses** (`eth0`, `wlan0`, `usb0`)
plus IPv6 link-local endpoints. This is the reliable way to learn the box's current addresses after a
DHCP change. (A matching UDP discovery listens on 39217.)

## Open ports (observed)

| Port | Service |
|---|---|
| 80 | HTTP API (nginx → FastAPI; `Host` header routes to services) |
| 3588 | SSH (key-only; see [cli-and-ssh.md](cli-and-ssh.md)) |
| 39217 / 39218 | discovery (UDP / HTTP `device.json`) |

Ports commonly expected but **closed** from the LAN: 22 (SSH is on 3588 instead), 443, 11434 (Ollama
is served on 80 via Host header, not its native port), and the internal services/model ports (e.g.
8880, 5555) — those are loopback-only on the device.

## Authentication

Every API request carries:

```
Authorization: Bearer <TOKEN>
```

`<TOKEN>` is the API key from the TiinyOS app → *Settings → API access* (stored locally in the app's
config, key `account.authKey`). Treat it as a root-equivalent credential — see
[cli-and-ssh.md](cli-and-ssh.md).
