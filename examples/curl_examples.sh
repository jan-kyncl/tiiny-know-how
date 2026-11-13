#!/usr/bin/env bash
# Minimal curl examples against a Tiiny box. Set these first:
#   export TIINY_HOST=http://192.168.3.50     # your box IP (OpenAI base, no /v1)
#   export TIINY_TOKEN=xxxxxxxx               # Settings -> API access
# The model you call must be running (launch it in the app or via the launch API).
set -euo pipefail
: "${TIINY_HOST:?set TIINY_HOST}" "${TIINY_TOKEN:?set TIINY_TOKEN}"
IP="${TIINY_HOST#http://}"; IP="${IP#https://}"   # bare host for Host-header calls

echo "== chat, reasoning OFF (Ollama endpoint, think:false) =="
curl -s -H "Host: ollama.api.tiiny" -H "Authorization: Bearer $TIINY_TOKEN" \
  "http://$IP/api/chat" \
  -d '{"model":"Qwen/Qwen3.6-35B-A3B","stream":false,"think":false,
       "messages":[{"role":"user","content":"Reply with one short sentence: what is a Tiiny Pocket?"}]}'
echo

echo "== chat, OpenAI-compatible (set max_tokens high; model thinks first) =="
curl -s -H "Authorization: Bearer $TIINY_TOKEN" -H "Content-Type: application/json" \
  "$TIINY_HOST/v1/chat/completions" \
  -d '{"model":"Qwen/Qwen3.6-35B-A3B","max_tokens":2000,
       "messages":[{"role":"user","content":"Say hello in Czech."}]}'
echo

echo "== text -> image (Z-Image), saves out.png =="
curl -s -H "Authorization: Bearer $TIINY_TOKEN" -H "Content-Type: application/json" \
  "$TIINY_HOST/v1/images/generations" \
  -d '{"model":"Tongyi-MAI/Z-Image-Turbo","prompt":"a small white AI box on a wooden desk, soft light"}' \
  | python3 -c 'import sys,json,base64;open("out.png","wb").write(base64.b64decode(json.load(sys.stdin)["data"][0]["b64_json"]));print("wrote out.png")'

echo "== transcribe a file (Whisper) =="
echo "   curl -s -H \"Authorization: Bearer \$TIINY_TOKEN\" \\"
echo "     -F model=openai/Whisper-large-v3-turbo -F language=cs -F file=@recording.wav \\"
echo "     \"\$TIINY_HOST/v1/audio/transcriptions\""
