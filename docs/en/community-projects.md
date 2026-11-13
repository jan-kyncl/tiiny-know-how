# Related community projects

Other repos and references that helped build these notes. Names are as published on GitHub; verify
anything before running it against your own device.

## API & reference
- **thezolon/tiiny-api-notes** — the most complete community API reference; also documented the
  USB-C Ethernet adapter working in the second port.
- **US4LKW/tiiny-ai-model-atlas** — model catalog with a language filter.
- **CooperativePenguinToby/tiiny-web** — open-source web client; source of several `/api/services`
  and connector endpoints.

## Access & internals
- **mjpcomp/tiiny-owner-ssh** — enrolls an owner SSH key (SSH is on port 3588). See
  [cli-and-ssh.md](cli-and-ssh.md) and its security note.
- **maci0/tiinyos-linux** — notes on running TiinyOS on Linux.
- **webdevtodayjason/tiiny-unlock** — unlock `/data` after a reboot via a single API call when the box
  returns 502.
- **teaguesterling/TTt** — `ttt` helper (`ttt doctor`, etc.).

## Models & inference
- **SJTU-IPADS / Tiiny-AI — PowerInfer** — the box's inference engine.
- **trentsuzuki/tiiny-custom-models** — run custom GGUF models via `llama.cpp` in a container.
- **Titanium-Devops/tiiny-bench** — benchmarking.
- **webdevtodayjason/turnstile** — request queue (the box does one inference at a time; concurrent →
  error `150004`).

## Control panels & integrations
- **0xStian/tiiny-control-panel** and **TheS1ngularity/TiinyControlPanel-HA** — web control panel and a
  Home Assistant add-on.
- **thezolon/tiiny-studio** — a studio UI.

> Listed for reference only; not endorsements. At least one community repo has been observed to contain
> an accidentally-committed API key — never reuse a token you find in someone else's repo, and don't
> commit your own.
