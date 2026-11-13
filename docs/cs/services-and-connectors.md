# Služby (aplikace) a konektory (MCP)

## Služby / aplikace (`agent-services.api.tiiny`)

Box umí provozovat self-hosted aplikace jako Docker služby. (Níže uvedené endpointy pocházejí z analýzy
open-source projektu `tiiny-web` a z kontrol na zařízení — ověř na vlastním kusu.)

| Metoda + cesta | Účel |
|---|---|
| `GET /api/services/cloud/apps` | instalovatelné aplikace `{app_id, installed}` |
| `GET /api/services` | nainstalované služby `{id, status, ports}` |
| `POST /api/services/download/stream` | instalace `{app_id}` (SSE, z cloudu) |
| `POST /api/services/{id}/start` \| `/stop` | spustit / zastavit |
| `DELETE /api/services/{id}` | odebrat |

Katalog obsahuje: KiloCode, n8n (wa-n8n), Dify, Open WebUI, OpenHands, AutoGPT, SillyTavern,
HermesAgent, OpenClaw, Odysseus, Tiiny Music, Tiiny Meeting, opencode.

> **🔒 Bezpečnost.** Aplikace se na LAN servírují přes port 80 na `<app>.agent.tiiny.local`
> **bez autentizace**. Box zafirewalluj od nedůvěryhodných sítí.

## Konektory / MCP (`connector.api.tiiny`)

Konektory vystavují externí integrace (a MCP servery) agentům v zařízení. Požadavky nesou hlavičku
`x-user-id: <serial>`.

| Volání | Účel |
|---|---|
| `GET /v1/status` | stav konektorů (telegram / discord / x / whatsapp / email) |
| `GET /v1/whatsapp/bridge/status` | stav WhatsApp bridge |
| `GET /v1/mcp/servers` | seznam MCP serverů |
| `POST /v1/mcp/servers` | přidat MCP server |
| `DELETE /v1/mcp/servers/{id}` | odebrat MCP server |

### Přidání MCP konektoru (bez SSH)

Externí **MCP server** zaregistruješ přes `POST /v1/mcp/servers` — **nevyžaduje** to shell/root na
boxu. Konektor mířící např. na Home Assistant MCP endpoint funguje takto.

Praktický vzor pro konektor, který potřebuje dlouho běžící bridge (např. WhatsApp): spusť MCP bridge na
samostatném stále zapnutém hostiteli, vystav ho jako **Streamable HTTP + bearer token** a tu URL pak
zaregistruj jako konektor. Provoz takového bridge přímo na boxu by naopak vyžadoval přístup ke
kontejnerům/rootu.

> **⚠️ Poznámka k WhatsAppu.** WhatsApp od 2025 banuje automatizaci. Pokud ho připojíš, preferuj
> read-only a/nebo vedlejší číslo.
