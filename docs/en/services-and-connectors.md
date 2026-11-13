# Services (apps) & connectors (MCP)

## Services / apps (`agent-services.api.tiiny`)

The box can run self-hosted apps as Docker services. (Endpoints below are from analysis of the
open-source `tiiny-web` project plus on-device checks — verify on your own unit.)

| Method + path | Purpose |
|---|---|
| `GET /api/services/cloud/apps` | installable apps `{app_id, installed}` |
| `GET /api/services` | installed services `{id, status, ports}` |
| `POST /api/services/download/stream` | install `{app_id}` (SSE, from cloud) |
| `POST /api/services/{id}/start` \| `/stop` | start / stop |
| `DELETE /api/services/{id}` | remove |

Catalog includes: KiloCode, n8n (wa-n8n), Dify, Open WebUI, OpenHands, AutoGPT, SillyTavern,
HermesAgent, OpenClaw, Odysseus, Tiiny Music, Tiiny Meeting, opencode.

> **🔒 Security.** Apps are served on the LAN over port 80 at `<app>.agent.tiiny.local` **without
> authentication**. Firewall the box off from untrusted networks.

## Connectors / MCP (`connector.api.tiiny`)

Connectors expose external integrations (and MCP servers) to the on-device agents. Requests carry the
header `x-user-id: <serial>`.

| Call | Purpose |
|---|---|
| `GET /v1/status` | connector status (telegram / discord / x / whatsapp / email) |
| `GET /v1/whatsapp/bridge/status` | WhatsApp bridge status |
| `GET /v1/mcp/servers` | list MCP servers |
| `POST /v1/mcp/servers` | add an MCP server |
| `DELETE /v1/mcp/servers/{id}` | remove an MCP server |

### Adding an MCP connector (no SSH required)

You can register an external **MCP server** with `POST /v1/mcp/servers` — this does **not** require
shell/root on the box. A connector pointing at, say, a Home Assistant MCP endpoint works this way.

A practical pattern for a connector that needs a long-lived bridge (e.g. WhatsApp): run the MCP bridge
on a separate always-on host, expose it as **Streamable HTTP + bearer token**, then register that URL
as a connector. Running such a bridge on the box itself would instead need container/root access.

> **⚠️ WhatsApp note.** WhatsApp has been banning automation since 2025. If you connect it, prefer
> read-only and/or a secondary number.
