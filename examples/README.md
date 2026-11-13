# Examples / Příklady

Small, self-contained scripts we used to test a Tiiny box. Stdlib-only Python (no `pip`), plus a
couple of `curl` snippets. The speech self-tests use macOS `say` to synthesize known text, so you can
measure accuracy without providing your own recordings.

> Malé samostatné skripty, kterými jsme testovali Tiiny. Python jen ze stdlib (žádný `pip`) + pár
> `curl` ukázek. Řečové self-testy používají macOS `say` k nasyntetizování známého textu, takže změříš
> přesnost i bez vlastních nahrávek.

## Setup

```bash
export TIINY_HOST=http://192.168.3.50    # your box IP — OpenAI base URL, no /v1
export TIINY_TOKEN=xxxxxxxx              # TiinyOS app -> Settings -> API access
```

The model you call must be **running** on the box (launch it in the app, or via
`POST /api/v1/models/<id>/launch`). See [../docs/en/api.md](../docs/en/api.md).

## Scripts

| File | What it does |
|---|---|
| [`whisper_test.py`](whisper_test.py) | Transcribe one file, or a `say`-generated Czech sentence, and compute **WER**. `-m` picks the ASR model. |
| [`asr_compare.py`](asr_compare.py) | Run several ASR models (Whisper / Qwen3-ASR / Parakeet) over a fixed set of CS/EN clips and print a WER + speed **summary table**. |
| [`song_demo.py`](song_demo.py) | Generate a song / background music with `SongGeneration-v2-large` (`song` / `bgm` / `vocal` / `separate` modes). |
| [`curl_examples.sh`](curl_examples.sh) | One-liners: chat with reasoning off (`think:false`), OpenAI-compatible chat, text→image, transcription. |

```bash
python3 whisper_test.py                 # self-test (cs) -> transcript -> WER
python3 asr_compare.py                  # compare all running ASR models
python3 song_demo.py -d 30              # 30 s sample song
bash   curl_examples.sh                 # quick API tour
```

## Notes from our runs / Poznámky z našich běhů

- ASR models must be launched first; `asr_compare.py` lists which ones are running and skips the rest.
- Speech-to-text ran comfortably faster than realtime on short clips; exact WER/speed depends on the
  model and audio, so the scripts print their own numbers rather than us hard-coding results here.
- `SongGeneration` is **not** in `openapi.json`; the endpoint (`/v1/music/generate`) was found by
  inspection and is documented in `song_demo.py`'s header. ~30 s of audio takes ~2 min to generate.
- These scripts contain **no token and no private addresses** — everything comes from the two env vars.
