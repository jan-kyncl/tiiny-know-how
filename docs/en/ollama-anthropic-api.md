# Ollama & Anthropic compatible APIs

Besides the OpenAI-compatible surface, the box exposes **Ollama-** and **Anthropic-compatible**
endpoints. Both are served on **port 80**, selected by the `Host` header — the native Ollama port
(11434) is closed. Verified with text models only.

## Ollama-compatible

```bash
# list models
curl -H "Host: ollama.api.tiiny" -H "Authorization: Bearer <TOKEN>" http://<ip>/api/tags

# chat — "think": false turns OFF reasoning (clean, short answers)
curl -H "Host: ollama.api.tiiny" -H "Authorization: Bearer <TOKEN>" http://<ip>/api/chat \
  -d '{"model":"Qwen/Qwen3.6-35B-A3B","stream":false,"think":false,
       "messages":[{"role":"user","content":"Hello"}]}'
```

`"think": false` is the simplest way to stop the model from spending tokens on hidden reasoning.

## Anthropic-compatible

```bash
curl -H "Host: anthropic.api.tiiny" \
     -H "x-api-key: <TOKEN>" -H "anthropic-version: 2023-06-01" \
     http://<ip>/v1/messages \
  -d '{"model":"Qwen/Qwen3.6-35B-A3B","max_tokens":500,
       "messages":[{"role":"user","content":"Hello"}]}'
```

The Anthropic endpoint returns `thinking` blocks in the response.

## Other known `Host` vhosts

From the dev.tiiny.ai docs, these virtual hosts also route on port 80:

```
api.tiiny                 openai.api.tiiny        ollama.api.tiiny
anthropic.api.tiiny       wifi.api.tiiny          upgrade.api.tiiny
connector.api.tiiny       agents.api.tiiny        agent-services.api.tiiny
p8800.api.tiiny           kb.tiiny.local          auth.api.tiiny.local
hardware-upgrade.api.tiiny
```

See [services-and-connectors.md](services-and-connectors.md) for `agent-services.api.tiiny` and
`connector.api.tiiny`.
