#!/usr/bin/env python3
"""Speech-to-text test on Tiiny (openai/Whisper-large-v3-turbo). Stdlib only.
Přepis řeči na Tiiny — vlastní test (macOS `say`) nebo libovolný soubor, s výpočtem WER.

Examples:
  export TIINY_HOST=http://192.168.3.50   # your box, OpenAI-compatible base (no /v1)
  export TIINY_TOKEN=xxxxxxxx
  python3 whisper_test.py                      # self-test: macOS `say` (cs) -> transcribe -> WER
  python3 whisper_test.py recording.m4a        # transcribe any file
  python3 whisper_test.py speech.wav -m Qwen/Qwen3-ASR-1.7B   # another ASR model (must be running)

Endpoint: POST $TIINY_HOST/v1/audio/transcriptions (multipart, OpenAI-compatible):
  file, model, language (cs), response_format (json|text — box supports only these), prompt, temperature
"""
import argparse, json, os, re, subprocess, sys, tempfile, time, unicodedata, urllib.error, urllib.request, uuid

HOST = os.environ.get("TIINY_HOST", "").rstrip("/")
TOKEN = os.environ.get("TIINY_TOKEN", "")
if not HOST or not TOKEN:
    sys.exit("Set TIINY_HOST (e.g. http://192.168.3.50) and TIINY_TOKEN environment variables.")

SAMPLE = ("Dobrý den, tady je test rozpoznávání řeči na zařízení Tiiny. "
          "Dnes je středa a venku je osm stupňů. Prosím zapni světlo v obýváku "
          "a nastav topení na dvacet jedna stupňů.")


def transcribe(path, model, language, fmt, prompt=None):
    b = uuid.uuid4().hex
    fields = {"model": model, "response_format": fmt}
    if language:
        fields["language"] = language
    if prompt:
        fields["prompt"] = prompt
    body = b"".join(f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode() for k, v in fields.items())
    body += (f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{os.path.basename(path)}\"\r\n"
             f"Content-Type: application/octet-stream\r\n\r\n").encode() + open(path, "rb").read() + f"\r\n--{b}--\r\n".encode()
    req = urllib.request.Request(f"{HOST}/v1/audio/transcriptions", body,
                                 {"Authorization": f"Bearer {TOKEN}", "Content-Type": f"multipart/form-data; boundary={b}"})
    raw = urllib.request.urlopen(req, timeout=600).read().decode()
    try:
        return json.loads(raw)
    except ValueError:
        return {"text": raw}


def words(t):
    t = unicodedata.normalize("NFC", t.lower())
    return re.findall(r"\w+", t)


def wer(ref, hyp):
    r, h = words(ref), words(hyp)
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
    return d[len(h)] / max(len(r), 1)


def duration(path):
    try:
        out = subprocess.run(["afinfo", path], capture_output=True, text=True).stdout
        return float(re.search(r"estimated duration: ([\d.]+)", out).group(1))
    except Exception:
        return None


def main():
    p = argparse.ArgumentParser(description="Whisper test on Tiiny")
    p.add_argument("file", nargs="?", help="audio file (omit for a self-test via macOS `say`)")
    p.add_argument("-m", "--model", default="openai/Whisper-large-v3-turbo")
    p.add_argument("-l", "--language", default="cs", help="language code, empty = autodetect")
    p.add_argument("-f", "--format", default="json", help="json|text (box supports only these)")
    p.add_argument("-r", "--ref", help="reference text for WER")
    a = p.parse_args()

    running = [m["id"] for m in json.load(urllib.request.urlopen(urllib.request.Request(
        f"{HOST}/v1/models", headers={"Authorization": f"Bearer {TOKEN}"}), timeout=30))["data"]]
    if a.model not in running:
        sys.exit(f"Model {a.model} is not running (running: {', '.join(running)}). Launch it via "
                 f"POST http://api.tiiny/api/v1/models/{a.model.replace('/', '%2F')}/launch")

    path, ref = a.file, a.ref
    if not path:
        path = os.path.join(tempfile.mkdtemp(), "say_cs.wav")
        subprocess.run(["say", "-v", "Zuzana", "-o", path, "--data-format=LEI16@16000", SAMPLE], check=True)
        ref = SAMPLE
        print(f"Generated with `say -v Zuzana`: {path}")

    dur = duration(path)
    print(f"Transcribing {os.path.basename(path)}" + (f" ({dur:.1f} s)" if dur else "") + f", model {a.model}")
    t0 = time.time()
    try:
        r = transcribe(path, a.model, a.language, a.format)
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode()[:500]}")
    el = time.time() - t0
    text = r.get("text", "")
    print(f"\nTRANSCRIPT ({el:.1f} s" + (f", {dur/el:.1f}x realtime" if dur else "") + "):\n" + text.strip())
    for s in r.get("segments") or []:
        print(f"  [{s.get('start', 0):6.1f}-{s.get('end', 0):6.1f}] {s.get('text', '').strip()}")
    if ref:
        print(f"\nREFERENCE:\n{ref}\nWER: {wer(ref, text)*100:.1f} %")


if __name__ == "__main__":
    main()
