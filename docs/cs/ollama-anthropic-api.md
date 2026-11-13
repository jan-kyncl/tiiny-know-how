# Ollama a Anthropic kompatibilní API

Kromě OpenAI-kompatibilního rozhraní box vystavuje i **Ollama-** a **Anthropic-kompatibilní**
endpointy. Oba běží na **portu 80**, vybírají se hlavičkou `Host` — nativní Ollama port (11434) je
zavřený. Ověřeno jen s textovými modely.

## Ollama-kompatibilní

```bash
# seznam modelů
curl -H "Host: ollama.api.tiiny" -H "Authorization: Bearer <TOKEN>" http://<ip>/api/tags

# chat — "think": false VYPNE reasoning (čisté, krátké odpovědi)
curl -H "Host: ollama.api.tiiny" -H "Authorization: Bearer <TOKEN>" http://<ip>/api/chat \
  -d '{"model":"Qwen/Qwen3.6-35B-A3B","stream":false,"think":false,
       "messages":[{"role":"user","content":"Ahoj"}]}'
```

`"think": false` je nejjednodušší způsob, jak modelu zabránit utrácet tokeny za skryté uvažování.

## Anthropic-kompatibilní

```bash
curl -H "Host: anthropic.api.tiiny" \
     -H "x-api-key: <TOKEN>" -H "anthropic-version: 2023-06-01" \
     http://<ip>/v1/messages \
  -d '{"model":"Qwen/Qwen3.6-35B-A3B","max_tokens":500,
       "messages":[{"role":"user","content":"Ahoj"}]}'
```

Anthropic endpoint vrací v odpovědi i bloky `thinking`.

## Další známé `Host` vhosty

Z dokumentace dev.tiiny.ai routují na portu 80 i tyto virtuální hosty:

```
api.tiiny                 openai.api.tiiny        ollama.api.tiiny
anthropic.api.tiiny       wifi.api.tiiny          upgrade.api.tiiny
connector.api.tiiny       agents.api.tiiny        agent-services.api.tiiny
p8800.api.tiiny           kb.tiiny.local          auth.api.tiiny.local
hardware-upgrade.api.tiiny
```

K `agent-services.api.tiiny` a `connector.api.tiiny` viz
[services-and-connectors.md](services-and-connectors.md).
