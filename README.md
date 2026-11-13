# Tiiny Pocket — community know-how

Unofficial, community-gathered notes on the **Tiiny Pocket** local AI box (model *Tiiny z01*):
hardware internals, the on-device HTTP API, networking, the official CLI, SSH, models, services
and connectors. Collected from hands-on testing plus other community projects.

> **Not affiliated** with Tiiny / dev.tiiny.ai. No warranty — commands here can change device state.
> Nothing here contains secrets; replace every `<TOKEN>` / `<ip>` placeholder with your own values.
> Verified against **TiinyOS firmware 0.1.39** (desktop app 1.0.3), November 2026.

🇨🇿 Česká verze níže / Czech version below.

---

## Contents

| Topic | Doc |
|---|---|
| Hardware internals | [docs/en/hardware.md](docs/en/hardware.md) |
| Networking & access (Wi-Fi, USB, USB-Ethernet, discovery, ports) | [docs/en/networking.md](docs/en/networking.md) |
| HTTP API (OpenAI-compatible + native) | [docs/en/api.md](docs/en/api.md) |
| Ollama & Anthropic compatible APIs | [docs/en/ollama-anthropic-api.md](docs/en/ollama-anthropic-api.md) |
| Models & custom model import | [docs/en/models.md](docs/en/models.md) |
| CLI & SSH | [docs/en/cli-and-ssh.md](docs/en/cli-and-ssh.md) |
| Services (apps) & connectors (MCP) | [docs/en/services-and-connectors.md](docs/en/services-and-connectors.md) |
| Troubleshooting | [docs/en/troubleshooting.md](docs/en/troubleshooting.md) |
| Related community projects | [docs/en/community-projects.md](docs/en/community-projects.md) |

## In one minute

- The box runs an **nginx :80 + FastAPI** server. **Everything is HTTP on port 80**; the service is
  selected by the `Host` header (`api.tiiny`, `ollama.api.tiiny`, `anthropic.api.tiiny`, …).
- Every request carries `Authorization: Bearer <TOKEN>` (the API key from the TiinyOS app →
  *Settings → API access*).
- Reach it over **Wi-Fi**, over **USB-C** (gadget to a host), or by plugging a **USB-C Ethernet
  adapter into the second USB-C port** so the box joins your LAN directly.
- There is **no web admin UI and no official shell**. An SSH server listens on **port 3588** (key-only);
  community tooling can enroll your own key.
- Models load on demand; the box does roughly **one inference at a time**.

---
---

# 🇨🇿 Tiiny Pocket — komunitní know-how

Neoficiální, komunitně sesbírané poznámky k lokálnímu AI boxu **Tiiny Pocket** (model *Tiiny z01*):
hardware uvnitř, HTTP API zařízení, síť, oficiální CLI, SSH, modely, služby a konektory.
Sesbíráno z vlastního testování a z dalších komunitních projektů.

> **Bez vazby** na Tiiny / dev.tiiny.ai. Bez záruky — příkazy zde mohou měnit stav zařízení.
> Nic zde neobsahuje tajemství; každý zástupný `<TOKEN>` / `<ip>` nahraď vlastními hodnotami.
> Ověřeno proti **TiinyOS firmware 0.1.39** (desktop app 1.0.3), listopad 2026.

## Obsah

| Téma | Dokument |
|---|---|
| Hardware uvnitř | [docs/cs/hardware.md](docs/cs/hardware.md) |
| Síť a přístup (Wi-Fi, USB, USB-Ethernet, discovery, porty) | [docs/cs/networking.md](docs/cs/networking.md) |
| HTTP API (OpenAI-kompatibilní + nativní) | [docs/cs/api.md](docs/cs/api.md) |
| Ollama a Anthropic kompatibilní API | [docs/cs/ollama-anthropic-api.md](docs/cs/ollama-anthropic-api.md) |
| Modely a import vlastních modelů | [docs/cs/models.md](docs/cs/models.md) |
| CLI a SSH | [docs/cs/cli-and-ssh.md](docs/cs/cli-and-ssh.md) |
| Služby (aplikace) a konektory (MCP) | [docs/cs/services-and-connectors.md](docs/cs/services-and-connectors.md) |
| Řešení potíží | [docs/cs/troubleshooting.md](docs/cs/troubleshooting.md) |
| Související komunitní projekty | [docs/cs/community-projects.md](docs/cs/community-projects.md) |

## V jedné minutě

- Box provozuje server **nginx :80 + FastAPI**. **Vše běží přes HTTP na portu 80**; služba se vybírá
  hlavičkou `Host` (`api.tiiny`, `ollama.api.tiiny`, `anthropic.api.tiiny`, …).
- Každý požadavek nese `Authorization: Bearer <TOKEN>` (API klíč z aplikace TiinyOS →
  *Settings → API access*).
- Dostaneš se tam přes **Wi-Fi**, přes **USB-C** (gadget do hostitele) nebo zapojením
  **USB-C Ethernet adaptéru do druhého USB-C portu**, čímž se box připojí přímo do tvé LAN.
- **Není webové admin rozhraní ani oficiální shell**. SSH server poslouchá na **portu 3588** (jen klíč);
  komunitní nástroje umí přidat vlastní klíč.
- Modely se načítají na vyžádání; box zvládá zhruba **jednu inferenci naráz**.
