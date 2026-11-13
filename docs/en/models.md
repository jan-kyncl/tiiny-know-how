# Models

Models load **on demand**. A `not loaded` response means the model exists on the box but is not
running — launch it via `POST /api/v1/models/<id>/launch`. The box runs roughly **one inference at a
time**; concurrent requests to a busy model return an error (code `150004`).

## Example installed models

| ID | Type |
|---|---|
| `Qwen/Qwen3.6-35B-A3B` | chat (vision + video + tool use, thinking) |
| `openai/gpt-oss-120b` | chat (large MoE) |
| `vllm-sr/d3-mini` | decision / routing (`/v1/systemone`) |
| `Qwen/Qwen3-ASR-1.7B` | speech-to-text |
| `openai/Whisper-large-v3-turbo` | speech-to-text |
| `nvidia/Parakeet-TDT-0.6B-V3` | speech-to-text |
| `OpenMOSS-Team/MOSS-Transcribe-Diarize` | transcription + speaker diarization |
| `Qwen/Qwen3-Embedding-0.6B` | embeddings |
| `Tongyi-MAI/Z-Image-Turbo` | text → image |
| `tencent/SongGeneration-v2-large` | music / song generation |

The full installable catalog (≈90+ models) is at `GET /api/v1/models/online_models`.

## Measured throughput (TiinyOS 0.1.39, via the HTTP API)

| Model | Decode | Prefill | TTFT |
|---|---|---|---|
| `Qwen/Qwen3.6-35B-A3B` | ~26–27 tok/s | ~750 tok/s | ~1 s |
| `openai/gpt-oss-120b` | ~16–17 tok/s | ~550 tok/s | ~1 s |

`gpt-oss-120b` needs the whole 48 GB NPU pool, so other large models must be stopped while it runs.
Model-store download speed from the Tiiny cloud is modest (~0.3–1.5 MB/s), so a 60–70 GB model can
take many hours.

## Importing custom models from Hugging Face

The TiinyOS app has an **Import model** step: paste a Hugging Face repo URL, the box downloads and
converts it. The API is only reachable from the host app's PC Server (`http://api.tiiny`):

| Call | Purpose |
|---|---|
| `GET /api/v1/models/import/toolkits` | supported base models (toolkits) |
| `POST /api/v1/models/import/inspect` `{"hf_url":"https://huggingface.co/<repo>"}` | dry-run check: `supported`/`unsupported`, size, type |
| `POST /api/v1/models/import` `{"hf_url": …}` | start the import |

Constraints:
- **Only fine-tunes of supported bases, in `.safetensors`.**
  - text bases: `Qwen/Qwen3.6-35B-A3B`, `Qwen/Qwen3.5-9B`, `Qwen/Qwen3-4B-Instruct-2507`
  - image bases: `Tongyi-MAI/Z-Image-Turbo`, `black-forest-labs/FLUX.2-klein-4B`, `baidu/ERNIE-Image-Turbo`
- **Not supported:** ASR/TTS models, GGUF, or other architectures. (`openai/whisper-large-v3` → `unsupported`.)

For arbitrary GGUF models, community project `trentsuzuki/tiiny-custom-models` runs `llama.cpp` in a
container instead — see [community-projects.md](community-projects.md).
