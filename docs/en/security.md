# Security — observations & open concerns

> **Read this first.** This page collects a box owner's **security concerns**, written as
> **possible, speculative conclusions** drawn from normal use and from public community projects — **not**
> a security audit, **not** confirmed vulnerabilities, and **not** responsibly-disclosed findings. Some
> of it may be wrong, out of date, or based on misunderstanding how the device works. Nothing here is an
> accusation against Tiiny AI. Treat every "concern" below as a hypothesis to verify yourself, not as
> fact. Verified against firmware 0.1.39.

The pattern below is deliberate: **Observation** = something actually seen on the device or in public
code; **Speculative concern** = the worry it *might* imply, which has not been confirmed.

## 1. The device token looks root-equivalent

- **Observation.** Community tooling (`mjpcomp/tiiny-owner-ssh`) uses the documented services/connector
  APIs to spin up a temporary Docker container that mounts the host filesystem (`/:/host`) as root.
  Creating that container only requires the normal device **API token**.
- **Speculative concern.** If that primitive is generally available, then **holding the API token may be
  equivalent to having root on the box** — regardless of there being "no shell." A leaked token would
  then not be just an API-abuse problem but a full-device-compromise problem. See
  [cli-and-ssh.md](cli-and-ssh.md).
- **If true, mitigation.** Treat the token like a root password: never in repos/logs/shared configs,
  rotate if exposed, and keep the box off untrusted networks.

## 2. LAN services may be unauthenticated

- **Observation.** Per community analysis (`tiiny-web`) and on-device checks, installed apps are served
  on the LAN over port 80 at `<app>.agent.tiiny.local` with no obvious authentication in front of them.
- **Speculative concern.** Anyone who can reach the box on the LAN **might** be able to use those apps —
  and, depending on the app, whatever data or actions they expose — without credentials.
- **If true, mitigation.** Put the box on an isolated VLAN/segment; firewall it off from guest and IoT
  networks; don't port-forward it.

## 3. Discovery is unauthenticated

- **Observation.** `http://<ip>:39218/device.json` returns the device name, **serial number**, and all
  interface addresses with no authentication.
- **Speculative concern.** On a shared network this leaks identifying/inventory information and makes the
  box trivial to locate and fingerprint. Low severity, but worth knowing.

## 4. Cloud dependency and phone-home

- **Observation.** Activation, the model store, and OS (OTA) updates are **coordinated with the Tiiny
  cloud**; the desktop app talks to vendor services.
- **Speculative concern.** A device marketed as "private/offline" still **appears to depend on the
  vendor cloud** for setup, model fetches and updates, which implies some telemetry/connectivity and a
  trust and availability dependency on the vendor. The *inference* runs locally; the *lifecycle* may not
  be fully offline. What exactly is sent has not been inspected here.
- **If it matters to you.** Watch the box's outbound traffic yourself (e.g. at the router) before
  trusting "fully offline" claims, and consider network-level egress controls.

## 5. Encrypted storage, but auto-unlocked at boot

- **Observation.** `/data` is LUKS-encrypted but is unlocked automatically at boot (no owner passphrase
  prompt).
- **Speculative concern.** That protects a **stolen drive / powered-off device**, but likely **not a
  running or booted box**, since the unlock key must be available to the device itself. Where that key
  lives and how it's protected has not been examined here.

## 6. Closed firmware is hard to verify

- **Observation.** There is no official shell and the firmware is closed; you drive everything through
  the API.
- **Speculative concern.** That makes it **hard to independently verify** what runs on the device, what
  it sends, or whether a given update changed security-relevant behavior. This is a transparency
  limitation, not a specific flaw.

## 7. Non-standard SSH port is not protection

- **Observation.** SSH listens on port **3588**, key-only.
- **Speculative concern.** The non-standard port is **security by obscurity**; key-only auth is the real
  control. Don't rely on the port number.

## 8. Ecosystem hygiene

- **Observation.** At least one public community repo was seen to contain an **accidentally-committed API
  token**.
- **Speculative concern.** Combined with concern #1 (token ≈ root), careless token handling across the
  community could expose individual boxes. Never reuse a token found in someone else's repo; never commit
  your own.

---

## Bottom line (speculative)

If concerns #1 and #2 hold, the practical security model is roughly: **anyone with network reach to the
box, or a copy of its token, may be able to fully control it.** That is manageable on a trusted, isolated
home network and risky on a shared/exposed one. **None of this is confirmed** — verify on your own device
before relying on any of it, and report real issues to the vendor rather than treating this page as one.
