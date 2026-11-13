# CLI & SSH

## Official CLI (`tiiny`)

The vendor ships an official CLI SDK (v0.0.7 at time of writing, from dev.tiiny.ai). It is a wrapper
over the same HTTP API — it does **not** give you a shell on the box.

Install (macOS example):

```bash
curl -fsSL http://tiiny-cli.tiiny.cloud/install-darwin.sh | bash
```

Binary at `~/.local/tiiny/bin/tiiny`, config at `~/.local/tiiny/config.json` (holds `account.authKey`
— your token).

Command groups:

```
auth / login / logout / status      scan / connect / wifi / upgrade
ls / info / top / load / unload     run / bench / interrupt
import / download / rm              connector
backup / restore / restart / shutdown / tasks      vault
```

Typical flow: `tiiny scan` → `tiiny connect <ip>` → `tiiny login` → `tiiny ls` / `tiiny run`.

## SSH

There is **no official shell**, but an SSH server listens on **port 3588** (port 22 is closed),
**key-only** (no password). Out of the box you have no authorized key, so you cannot log in.

### Enrolling your own key

Community project **`mjpcomp/tiiny-owner-ssh`** enrolls an owner key. How it works (worth understanding
before you run it):

1. It uses the connector API (`connector.api.tiiny` → `/v1/mcp/servers`) to create a temporary MCP
   connector, then the services API (`agent-services.api.tiiny` → `/api/services`) to run a **temporary
   Docker container** that mounts the host filesystem (`/:/host`) as **root**.
2. Inside that container it writes three files and SIGHUPs sshd:
   - `/etc/ssh/owner_authorized_keys/` (dir, `700`)
   - `/etc/ssh/owner_authorized_keys/root` (your public key, `600`)
   - `/etc/ssh/sshd_config.d/00-owner-access.conf`
     (`PermitRootLogin prohibit-password` + an `AuthorizedKeysFile` pointing at the dir above)
3. The container removes itself after ~180 s. The tool also takes a baseline backup, verifies, and
   can auto-roll-back.

The repo's Windows-only parts are just the launcher and token-reading; the core is platform-independent
Python.

> **🔒 Security implication.** The mechanism above means **anyone who holds the device token effectively
> has root on the box**, via the container primitive — regardless of SSH. Treat the token accordingly:
> keep it out of repos, logs, and shared configs, and firewall the box off from untrusted networks.

### Practical blocker (0.1.39)

Running `tiiny-owner-ssh`'s container needs a **plain `python3` Docker image present on the box**. On
firmware 0.1.39 the self-contained image discovery (internal port 5555, `/api/web/compose/current`)
returns empty, and the only preinstalled images are the n8n stack (node, not python). Installing a
service that caches a python image (e.g. **Odysseus**, which bundles SearXNG) provides one, after which
the "compatibility path" that posts the service from a host over `agent-services.api.tiiny` works.
