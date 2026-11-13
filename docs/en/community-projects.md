# Related community projects & credits

These notes stand on the shoulders of the wider Tiiny community. The repos below are what we cite or
drew inspiration from — thanks to their authors. Names and links are as published on GitHub; verify
anything before running it against your own device.

## API & reference
- [thezolon/tiiny-api-notes](https://github.com/thezolon/tiiny-api-notes) — the most complete community
  API reference; also documented the USB-C Ethernet adapter working in the second port.
- [US4LKW/tiiny-ai-model-atlas](https://github.com/US4LKW/tiiny-ai-model-atlas) — model catalog with a
  language filter.
- [CooperativePenguinToby/tiiny-web](https://github.com/CooperativePenguinToby/tiiny-web) — open-source
  web client; source of several `/api/services` and connector endpoints.

## Access & internals
- [mjpcomp/tiiny-owner-ssh](https://github.com/mjpcomp/tiiny-owner-ssh) — enrolls an owner SSH key (SSH
  is on port 3588). See [cli-and-ssh.md](cli-and-ssh.md) and its security note.
- [maci0/tiinyos-linux](https://github.com/maci0/tiinyos-linux) — notes on running TiinyOS on Linux.
- [webdevtodayjason/tiiny-unlock](https://github.com/webdevtodayjason/tiiny-unlock) — unlock `/data`
  after a reboot via a single API call when the box returns 502.
- [teaguesterling/TTt](https://github.com/teaguesterling/TTt) — `ttt` helper (`ttt doctor`, etc.).

## Models & inference
- [SJTU-IPADS/PowerInfer](https://github.com/SJTU-IPADS/PowerInfer) — the inference engine the box is
  built on (Tiiny ships a fork).
- [trentsuzuki/tiiny-custom-models](https://github.com/trentsuzuki/tiiny-custom-models) — run custom
  GGUF models via `llama.cpp` in a container.
- [Titanium-Devops/tiiny-bench](https://github.com/Titanium-Devops/tiiny-bench) — benchmarking.
- [webdevtodayjason/turnstile](https://github.com/webdevtodayjason/turnstile) — request queue (the box
  does one inference at a time; concurrent → error `150004`).

## Control panels & integrations
- [0xStian/tiiny-control-panel](https://github.com/0xStian/tiiny-control-panel) — web control panel.
- [TheS1ngularity/TiinyControlPanel-HA](https://github.com/TheS1ngularity/TiinyControlPanel-HA) — Home
  Assistant add-on.
- [thezolon/tiiny-studio](https://github.com/thezolon/tiiny-studio) — a studio UI.

---

> Listed for reference and credit, not as endorsements. At least one community repo has been observed to
> contain an accidentally-committed API key — never reuse a token you find in someone else's repo, and
> don't commit your own.
