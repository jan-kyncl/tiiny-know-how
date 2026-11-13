#!/usr/bin/env python3
"""Demo: song generation on Tiiny (tencent/SongGeneration-v2-large). Stdlib only.
Generování písně na Tiiny.

Examples:
  export TIINY_HOST=http://192.168.3.50
  export TIINY_TOKEN=xxxxxxxx
  python3 song_demo.py                                   # default sample song, 30 s
  python3 song_demo.py -c "male, rock, energetic, drums, electric guitar, the bpm is 140" -d 60
  python3 song_demo.py -l text.txt -o song.wav           # lyrics from a file
  python3 song_demo.py -m bgm -c "lofi, chill, piano" -d 45   # background music, no vocals
  python3 song_demo.py -m separate                       # vocals and accompaniment separately

Endpoint (discovered, not in openapi.json):
  POST $TIINY_HOST/v1/music/generate
  {"model": "...", "mode": "song|bgm|vocal|separate",
   "config": {"lyrics": "...", "caption": "style", "duration": s, "seed": int,
              "temperature": f, "top_k": int, "top_p": f, "steps": int}}
  -> {"success", "audio_data": base64 WAV, "audio_outputs": {...}, "sample_rate", "duration", "metadata", "error"}

Lyrics format: sections [intro-short|intro-medium], [verse], [chorus], [bridge], [inst-short], [outro-short]
separated by " ; ", sentences inside a section by ".". Style (caption): comma-separated keywords
(voice gender, genre, mood, instruments, "the bpm is N").
Model must be running (launch via http://api.tiiny, ~28% NPU, ~20 s to start). Max length 270 s;
30 s of song takes ~2 min to generate.
"""
import argparse, base64, json, os, sys, time, urllib.error, urllib.request

MODEL = "tencent/SongGeneration-v2-large"
HOST = os.environ.get("TIINY_HOST", "").rstrip("/")
TOKEN = os.environ.get("TIINY_TOKEN", "")
if not HOST or not TOKEN:
    sys.exit("Set TIINY_HOST (e.g. http://192.168.3.50) and TIINY_TOKEN environment variables.")

DEFAULT_LYRICS = ("[intro-short] ; "
                  "[verse] Ranní slunce nad Prahou. Káva voní v kuchyni. Tramvaj zvoní pod oknem ; "
                  "[chorus] Je to krásný den. Je to krásný den. Zpívám si a jdu ven ; "
                  "[outro-short]")
DEFAULT_CAPTION = "female, pop, happy, piano, acoustic guitar, the bpm is 110"


def api(path, body=None, timeout=60):
    req = urllib.request.Request(HOST + path, json.dumps(body).encode() if body is not None else None,
                                 {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=timeout))


def main():
    p = argparse.ArgumentParser(description="Song generation on Tiiny")
    p.add_argument("-l", "--lyrics", help="lyrics text, or path to a lyrics file")
    p.add_argument("-c", "--caption", default=DEFAULT_CAPTION, help="style (keywords)")
    p.add_argument("-d", "--duration", type=float, default=30, help="length in s (max 270)")
    p.add_argument("-m", "--mode", default="song", choices=["song", "bgm", "vocal", "separate"])
    p.add_argument("-s", "--seed", type=int)
    p.add_argument("-o", "--out", default=f"song_{time.strftime('%Y%m%d_%H%M%S')}.wav")
    a = p.parse_args()

    lyrics = a.lyrics or DEFAULT_LYRICS
    if os.path.isfile(lyrics):
        lyrics = open(lyrics, encoding="utf-8").read().strip()

    if MODEL not in [m["id"] for m in api("/v1/models")["data"]]:
        sys.exit(f"Model {MODEL} is not running. Launch it (from a host with the PC Server):\n"
                 f"  curl -X POST -H 'Authorization: Bearer $TIINY_TOKEN' -d '{{}}' "
                 f"http://api.tiiny/api/v1/models/tencent%2FSongGeneration-v2-large/launch")

    cfg = {"caption": a.caption, "duration": a.duration}
    if a.mode != "bgm":
        cfg["lyrics"] = lyrics
    if a.seed is not None:
        cfg["seed"] = a.seed
    print(f"Generating {a.duration:.0f} s, mode {a.mode}, style: {a.caption}")
    t0 = time.time()
    try:
        r = api("/v1/music/generate", {"model": MODEL, "mode": a.mode, "config": cfg}, timeout=1800)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:500]}")
    if not r.get("success"):
        sys.exit(f"Error: {r.get('error')}")

    base, ext = os.path.splitext(a.out)
    files = []
    if r.get("audio_data"):
        open(a.out, "wb").write(base64.b64decode(r["audio_data"]))
        files.append(a.out)
    for name, data in (r.get("audio_outputs") or {}).items():
        if isinstance(data, dict):
            data = data.get("audio_data") or data.get("data")
        if isinstance(data, str) and data:
            f = f"{base}_{name}{ext or '.wav'}"
            open(f, "wb").write(base64.b64decode(data))
            files.append(f)
    md = r.get("metadata", {})
    print(f"Done in {time.time()-t0:.0f} s: {r.get('duration')} s, {r.get('sample_rate')} Hz, "
          f"{r.get('channels')} channels, seed {md.get('seed')}")
    for f in files:
        print("  ", os.path.abspath(f))
    if sys.platform == "darwin" and files:
        print("Play: afplay", files[0])


if __name__ == "__main__":
    main()
