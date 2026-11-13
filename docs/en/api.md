# HTTP API

All API calls go to **port 80** with `Authorization: Bearer <TOKEN>`. The `Host` header selects which
service answers; the default/native API uses `Host: api.tiiny` (or just the IP). An OpenAPI spec is
served at `http://<ip>/openapi.json`.

## OpenAI-compatible API

```
Base URL:  http://<ip>/v1
API key:   <TOKEN>
```

```bash
curl http://<ip>/v1/chat/completions \
  -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen3.6-35B-A3B",
       "messages":[{"role":"user","content":"Hello"}],
       "max_tokens":2000}'
```

Endpoints: `/v1/chat/completions`, `/v1/audio/transcriptions`, `/v1/embeddings`,
`/v1/images/generations`, `/v1/models`.

> **⚠️ Thinking tokens.** Chat models think before answering (often ~550 tokens even for a trivial
> prompt). Set `max_tokens` ≥ 2000, or the budget is spent on hidden reasoning and you get an empty
> reply. To disable reasoning entirely, use the Ollama endpoint with `"think": false`
> (see [ollama-anthropic-api.md](ollama-anthropic-api.md)).

### Image generation
`POST /v1/images/generations`, model `Tongyi-MAI/Z-Image-Turbo`. Result is base64 in
`data[0].b64_json`, ~1024×1024. The first call is slower while the model loads.

### Speech transcription
`POST /v1/audio/transcriptions` (multipart: `model`, `file`, `language`). Models
`Qwen/Qwen3-ASR-1.7B` or `openai/Whisper-large-v3-turbo` (must be running).

## Native device & model API

| Method + path | Purpose |
|---|---|
| `GET /api/v1/models/` | list models (`?including_downloading=true` to include in-progress) |
| `GET /api/v1/models/online_models` | the Model Store catalog (installable models) |
| `POST /api/v1/models/<id>/launch` | load/start a model |
| `POST /api/v1/models/<id>/stop` | unload/stop a model |
| `POST /api/v1/models/<id>/download/stream` | download a model (SSE; continues after the stream closes) |
| `GET /api/v1/sys/device_info` | device info (model name, serial) |
| `GET /api/v1/sys/status` | CPU / RAM / NPU / disk load |
| `GET /api/v1/sys/storage` | storage usage |
| `GET /api/v1/sys/performance` | request statistics |
| `POST /api/v1/sys/reboot/` | reboot |
| `POST /api/v1/sys/shutdown/` | shutdown (no body) |
| `POST /api/v1/sys/ac_power/` | auto power-on after power applied, `{"switch":1}` |
| `GET /api/v1/sys/wifi/wifi_list` | scan Wi-Fi networks |
| `POST /api/v1/sys/wifi/wifi_connect` | join a Wi-Fi network |

Notes:
- After a power cycle, `/v1/models` can return **0 models** — they reload shortly, or you launch one
  explicitly with the `launch` endpoint.
- Some endpoints (notably the custom-model *import* flow) are only reachable from the host computer
  running the desktop app's "PC Server", via `http://api.tiiny` — not over the plain LAN IP.

## Decision / routing models

Jev-style decision models (e.g. `vllm-sr/d3-mini`) expose:

```
POST /v1/systemone
{ "model": "...", "state": "...",
  "questions": { "k": { "type": "choice|noul|score", "instructions": "...", "criteria": "..." } } }
```

Returns `answers.k.{choice, probabilities, confidence}` (for `noul`, the probability of "yes"). Fast
(~0.9 s per call) and useful for routing/classification.
