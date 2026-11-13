# HTTP API

Všechna volání API jdou na **port 80** s `Authorization: Bearer <TOKEN>`. Hlavička `Host` vybírá, která
služba odpoví; výchozí/nativní API používá `Host: api.tiiny` (nebo prostě IP). OpenAPI spec je na
`http://<ip>/openapi.json`.

## OpenAI-kompatibilní API

```
Base URL:  http://<ip>/v1
API key:   <TOKEN>
```

```bash
curl http://<ip>/v1/chat/completions \
  -H "Authorization: Bearer <TOKEN>" -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen3.6-35B-A3B",
       "messages":[{"role":"user","content":"Ahoj"}],
       "max_tokens":2000}'
```

Endpointy: `/v1/chat/completions`, `/v1/audio/transcriptions`, `/v1/embeddings`,
`/v1/images/generations`, `/v1/models`.

> **⚠️ Thinking tokeny.** Chat modely přemýšlejí před odpovědí (často ~550 tokenů i na triviální dotaz).
> Nastav `max_tokens` ≥ 2000, jinak se budget spotřebuje na skryté uvažování a vrátí se prázdná odpověď.
> Úplně vypnout reasoning jde přes Ollama endpoint s `"think": false`
> (viz [ollama-anthropic-api.md](ollama-anthropic-api.md)).

### Generování obrázků
`POST /v1/images/generations`, model `Tongyi-MAI/Z-Image-Turbo`. Výsledek = base64 v
`data[0].b64_json`, ~1024×1024. První volání je pomalejší (model se načítá).

### Přepis řeči
`POST /v1/audio/transcriptions` (multipart: `model`, `file`, `language`). Modely
`Qwen/Qwen3-ASR-1.7B` nebo `openai/Whisper-large-v3-turbo` (musí běžet).

## Nativní API zařízení a modelů

| Metoda + cesta | Účel |
|---|---|
| `GET /api/v1/models/` | seznam modelů (`?including_downloading=true` i rozpracované) |
| `GET /api/v1/models/online_models` | katalog Model Store (instalovatelné modely) |
| `POST /api/v1/models/<id>/launch` | načíst/spustit model |
| `POST /api/v1/models/<id>/stop` | zastavit model |
| `POST /api/v1/models/<id>/download/stream` | stáhnout model (SSE; pokračuje i po zavření streamu) |
| `GET /api/v1/sys/device_info` | info o zařízení (jméno modelu, sériové číslo) |
| `GET /api/v1/sys/status` | zátěž CPU / RAM / NPU / disk |
| `GET /api/v1/sys/storage` | využití úložiště |
| `GET /api/v1/sys/performance` | statistiky requestů |
| `POST /api/v1/sys/reboot/` | restart |
| `POST /api/v1/sys/shutdown/` | vypnutí (bez těla) |
| `POST /api/v1/sys/ac_power/` | auto zapnutí po připojení napájení, `{"switch":1}` |
| `GET /api/v1/sys/wifi/wifi_list` | sken Wi-Fi sítí |
| `POST /api/v1/sys/wifi/wifi_connect` | připojit Wi-Fi |

Poznámky:
- Po vyp/zap může `/v1/models` vrátit **0 modelů** — za chvíli se donačtou, nebo některý spustíš
  explicitně endpointem `launch`.
- Některé endpointy (zejm. *import* vlastních modelů) jsou dostupné jen z hostitelského počítače s
  „PC Serverem“ aplikace, přes `http://api.tiiny` — ne přes běžnou LAN IP.

## Rozhodovací / routovací modely

Rozhodovací modely stylu Jev (např. `vllm-sr/d3-mini`) vystavují:

```
POST /v1/systemone
{ "model": "...", "state": "...",
  "questions": { "k": { "type": "choice|noul|score", "instructions": "...", "criteria": "..." } } }
```

Vrací `answers.k.{choice, probabilities, confidence}` (pro `noul` pravděpodobnost „ano“). Rychlé
(~0,9 s na volání), užitečné pro routing/klasifikaci.
