#!/usr/bin/env python3
"""Compare ASR models on Tiiny over a set of recordings (macOS `say`, known text). Stdlib only.
Srovnání ASR modelů na Tiiny na sadě nahrávek, s výpočtem WER.

  export TIINY_HOST=http://192.168.3.50
  export TIINY_TOKEN=xxxxxxxx
  python3 asr_compare.py                                  # all running ASR models
  python3 asr_compare.py -m openai/Whisper-large-v3-turbo nvidia/Parakeet-TDT-0.6B-V3
  python3 asr_compare.py -f recording.wav -r "reference text"   # add your own recording

WER is computed after normalization (lowercase, no punctuation, numbers 0-99 spelled out).
"""
import argparse, json, os, re, subprocess, sys, tempfile, time, unicodedata, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from whisper_test import HOST, TOKEN, transcribe, duration  # noqa: E402

SAMPLES = [
    ("cs-short", "Zuzana", "cs",
     "Dobrý den, tady je test rozpoznávání řeči na zařízení Tiiny. Dnes je středa a venku je osm stupňů. "
     "Prosím zapni světlo v obýváku a nastav topení na dvacet jedna stupňů."),
    ("cs-command", "Zuzana", "cs", "Vypni všechna světla v ložnici a stáhni žaluzie na terase."),
    ("cs-long", "Zuzana", "cs",
     "Praha je hlavní a zároveň největší město České republiky. Leží na řece Vltavě a žije v ní přibližně "
     "jeden a čtvrt milionu obyvatel. Historické centrum je zapsáno na seznamu světového dědictví UNESCO. "
     "Mezi nejznámější památky patří Pražský hrad, Karlův most a Staroměstské náměstí s orlojem. "
     "Ročně město navštíví miliony turistů z celého světa."),
    ("en", "Samantha", "en",
     "Good morning. Please turn off the kitchen lights and set the thermostat to twenty one degrees. "
     "The meeting with the engineering team starts at half past nine."),
]

ONES = "nula jedna dva tři čtyři pět šest sedm osm devět deset jedenáct dvanáct třináct čtrnáct patnáct šestnáct sedmnáct osmnáct devatenáct".split()
TENS = {2: "dvacet", 3: "třicet", 4: "čtyřicet", 5: "padesát", 6: "šedesát", 7: "sedmdesát", 8: "osmdesát", 9: "devadesát"}
EN_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
EN_TENS = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"}


def num2words(n, lang):
    ones, tens = (ONES, TENS) if lang == "cs" else (EN_ONES, EN_TENS)
    if n < 20:
        return ones[n]
    if n < 100:
        return tens[n // 10] + ("" if n % 10 == 0 else " " + ones[n % 10])
    return str(n)


def norm(t, lang):
    t = unicodedata.normalize("NFC", t.lower())
    t = re.sub(r"\d+", lambda m: " " + num2words(int(m.group()), lang) + " ", t)
    return re.findall(r"\w+", t)


def edit(r, h):
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
    return d[len(h)]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-m", "--models", nargs="*")
    p.add_argument("-f", "--file")
    p.add_argument("-r", "--ref")
    p.add_argument("-l", "--lang", default="cs")
    a = p.parse_args()

    info = json.load(urllib.request.urlopen(urllib.request.Request(
        f"{HOST}/v1/models", headers={"Authorization": f"Bearer {TOKEN}"}), timeout=30))["data"]
    asr = [m["id"] for m in info if m.get("type") == "ASR"]
    models = a.models or asr
    missing = [m for m in models if m not in asr]
    if missing:
        sys.exit(f"Not running: {', '.join(missing)} (running ASR: {', '.join(asr)})")

    tmp = tempfile.mkdtemp()
    items = []
    for name, voice, lang, text in SAMPLES:
        f = os.path.join(tmp, name + ".wav")
        subprocess.run(["say", "-v", voice, "-o", f, "--data-format=LEI16@16000", text], check=True)
        items.append((name, lang, f, text))
    if a.file:
        items.append((os.path.basename(a.file), a.lang, a.file, a.ref))

    res = {}
    for name, lang, f, ref in items:
        dur = duration(f) or 0
        print(f"\n=== {name} ({dur:.1f} s)\nREF: {ref or '-'}")
        for m in models:
            t0 = time.time()
            try:
                text = transcribe(f, m, lang, "json").get("text", "").strip()
            except Exception as e:
                print(f"{m.split('/')[-1]:>24} ERROR {e}")
                continue
            el = time.time() - t0
            w = edit(norm(ref, lang), norm(text, lang)) / max(len(norm(ref, lang)), 1) if ref else None
            res.setdefault(m, []).append((el, dur, w))
            print(f"{m.split('/')[-1]:>24} {el:5.1f} s  " + (f"WER {w*100:5.1f} %" if w is not None else "") + f"\n{'':>26}{text}")

    print("\n=== SUMMARY")
    print(f"{'model':>28} | {'sum t':>7} | {'x realtime':>10} | {'avg WER':>10}")
    for m, rows in res.items():
        el = sum(r[0] for r in rows); du = sum(r[1] for r in rows)
        ws = [r[2] for r in rows if r[2] is not None]
        print(f"{m:>28} | {el:6.1f}s | {du/el:9.1f}x | {sum(ws)/len(ws)*100:9.1f} %")


if __name__ == "__main__":
    main()
