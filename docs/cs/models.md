# Modely

Modely se načítají **na vyžádání**. Odpověď `not loaded` znamená, že model na boxu existuje, ale neběží
— spusť ho přes `POST /api/v1/models/<id>/launch`. Box zvládá zhruba **jednu inferenci naráz**;
souběžné požadavky na zaneprázdněný model vrátí chybu (kód `150004`).

## Příklad nainstalovaných modelů

| ID | Typ |
|---|---|
| `Qwen/Qwen3.6-35B-A3B` | chat (vision + video + tool use, thinking) |
| `openai/gpt-oss-120b` | chat (velké MoE) |
| `vllm-sr/d3-mini` | rozhodování / routing (`/v1/systemone`) |
| `Qwen/Qwen3-ASR-1.7B` | přepis řeči |
| `openai/Whisper-large-v3-turbo` | přepis řeči |
| `nvidia/Parakeet-TDT-0.6B-V3` | přepis řeči |
| `OpenMOSS-Team/MOSS-Transcribe-Diarize` | přepis + rozlišení mluvčích |
| `Qwen/Qwen3-Embedding-0.6B` | embeddingy |
| `Tongyi-MAI/Z-Image-Turbo` | text → obrázek |
| `tencent/SongGeneration-v2-large` | generování hudby / písní |

Kompletní instalovatelný katalog (≈90+ modelů) je na `GET /api/v1/models/online_models`.

## Naměřená propustnost (TiinyOS 0.1.39, přes HTTP API)

| Model | Decode | Prefill | TTFT |
|---|---|---|---|
| `Qwen/Qwen3.6-35B-A3B` | ~26–27 tok/s | ~750 tok/s | ~1 s |
| `openai/gpt-oss-120b` | ~16–17 tok/s | ~550 tok/s | ~1 s |

`gpt-oss-120b` potřebuje celý 48GB NPU zdroj, takže během jeho běhu musí být ostatní velké modely
zastavené. Rychlost stahování z Tiiny cloudu je mírná (~0,3–1,5 MB/s), takže 60–70GB model se může
stahovat mnoho hodin.

## Import vlastních modelů z Hugging Face

Aplikace TiinyOS má krok **Import model**: vložíš URL Hugging Face repa, box ho stáhne a převede. API je
dostupné jen z PC Serveru hostitelské aplikace (`http://api.tiiny`):

| Volání | Účel |
|---|---|
| `GET /api/v1/models/import/toolkits` | podporované základy (toolkity) |
| `POST /api/v1/models/import/inspect` `{"hf_url":"https://huggingface.co/<repo>"}` | kontrola bez stahování: `supported`/`unsupported`, velikost, typ |
| `POST /api/v1/models/import` `{"hf_url": …}` | spustí import |

Omezení:
- **Jen fine-tuny podporovaných základů, formát `.safetensors`.**
  - textové základy: `Qwen/Qwen3.6-35B-A3B`, `Qwen/Qwen3.5-9B`, `Qwen/Qwen3-4B-Instruct-2507`
  - obrázkové základy: `Tongyi-MAI/Z-Image-Turbo`, `black-forest-labs/FLUX.2-klein-4B`, `baidu/ERNIE-Image-Turbo`
- **Nepodporováno:** ASR/TTS modely, GGUF ani jiné architektury. (`openai/whisper-large-v3` → `unsupported`.)

Pro libovolné GGUF modely komunitní projekt `trentsuzuki/tiiny-custom-models` místo toho spouští
`llama.cpp` v kontejneru — viz [community-projects.md](community-projects.md).
