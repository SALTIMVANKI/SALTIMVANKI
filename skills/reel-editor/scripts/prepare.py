#!/usr/bin/env python3
"""Prepara un proyecto de reel a partir de un vídeo vertical hablado a cámara.

Uso: python3 prepare.py VIDEO PROYECTO [--style dorado-editorial] [--language es]

Genera en PROYECTO/:
  assets/base.mp4    vídeo 1080x1920 30 fps con la gradación del estilo, sin audio
  assets/voice.wav   voz limpia y normalizada a -16 LUFS
  assets/endbg.jpg   último fotograma desenfocado (fondo de la tarjeta de cierre)
  fonts/             tipografías del estilo en local
  gsap.min.js        GSAP local (el CDN puede estar bloqueado)
  faces.json         posición de la cara cada 0,5 s y la zona segura calculada
  project.json       borrador: subtítulos con tiempos por palabra y secciones vacías
"""
import argparse, json, os, re, shutil, subprocess, sys, tarfile, tempfile, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
MODEL = os.path.expanduser("~/.cache/hyperframes/whisper/models/ggml-small.bin")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"


def run(*cmd):
    subprocess.run(cmd, check=True)


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return round(float(out), 2)


def prepare_media(video, proj, style):
    a = os.path.join(proj, "assets")
    os.makedirs(a, exist_ok=True)
    vf = f"scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,{style['grade']}"
    run("ffmpeg", "-v", "error", "-y", "-i", video, "-vf", vf, "-an", "-r", "30", "-c:v", "libx264",
        "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", f"{a}/base.mp4")
    run("ffmpeg", "-v", "error", "-y", "-i", video, "-vn", "-af",
        "highpass=f=80,afftdn=nf=-30,acompressor=threshold=-20dB:ratio=3:attack=10:release=150,"
        "loudnorm=I=-16:TP=-1.5:LRA=9", "-ar", "48000", "-ac", "2", f"{a}/voice.wav")
    run("ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", f"{a}/base.mp4", "-frames:v", "1",
        "-vf", "gblur=sigma=28,eq=brightness=-0.12:saturation=0.9", "-q:v", "3", f"{a}/endbg.jpg")


def fetch_fonts(proj, style):
    d = os.path.join(proj, "fonts")
    os.makedirs(d, exist_ok=True)
    req = urllib.request.Request(style["fonts"]["google_css"], headers={"User-Agent": UA})
    css = urllib.request.urlopen(req, timeout=30).read().decode()
    keep = []
    for sub, block in re.findall(r"/\* ([\w-]+) \*/\s*(@font-face\s*{[^}]+})", css):
        if sub not in ("latin", "latin-ext"):
            continue
        url = re.search(r"url\((https://[^)]+)\)", block).group(1)
        name = url.rsplit("/", 1)[1]
        if not os.path.exists(f"{d}/{name}"):
            urllib.request.urlretrieve(url, f"{d}/{name}")
        keep.append(block.replace(url, name))
    open(f"{d}/local.css", "w").write("\n".join(keep))


def fetch_gsap(proj):
    if os.path.exists(f"{proj}/gsap.min.js"):
        return
    with tempfile.TemporaryDirectory() as tmp:
        run("npm", "pack", "gsap@3.14.2", "--silent", "--pack-destination", tmp)
        tgz = next(f for f in os.listdir(tmp) if f.endswith(".tgz"))
        with tarfile.open(f"{tmp}/{tgz}") as t:
            src = t.extractfile("package/dist/gsap.min.js").read()
    open(f"{proj}/gsap.min.js", "wb").write(src)


def detect_faces(proj):
    import cv2  # opencv-python-headless<5 (la v5 quitó los Haar cascades)
    cap = cv2.VideoCapture(f"{proj}/assets/base.mp4")
    det = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    out, i = [], 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        if i % int(fps / 2) == 0:
            h, w = f.shape[:2]
            fs = det.detectMultiScale(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), 1.1, 6, minSize=(w // 5, w // 5))
            if len(fs):
                x, y, fw, fh = max(fs, key=lambda r: r[2] * r[3])
                out.append([round(i / fps, 1), round(x / w, 3), round(y / h, 3), round((x + fw) / w, 3), round((y + fh) / h, 3)])
        i += 1
    bottoms = sorted(o[4] for o in out)
    # percentil 90 del borde inferior de la cara (descarta falsos positivos) + margen
    p90 = bottoms[int(len(bottoms) * 0.9)] if bottoms else 0.6
    safe_top = int(min(max(p90 + 0.02, 0.5), 0.68) * 1920)
    json.dump({"samples": out, "safe_top_px": safe_top}, open(f"{proj}/faces.json", "w"))
    return safe_top


def transcribe(proj, language):
    if not os.path.exists(MODEL):
        sys.exit(f"Falta el modelo de Whisper ({MODEL}). Ejecuta scripts/setup-video-tools.sh con acceso a huggingface.co.")
    wav = f"{proj}/assets/voice16k.wav"
    run("ffmpeg", "-v", "error", "-y", "-i", f"{proj}/assets/voice.wav", "-ar", "16000", "-ac", "1", wav)
    run("whisper-cli", "-m", MODEL, "-l", language, "-ml", "1", "-sow", "-oj", "-of", f"{proj}/words",
        "-f", wav, "-t", str(os.cpu_count() or 4), "-np")
    words = [(s["offsets"]["from"] / 1000, s["text"].strip())
             for s in json.load(open(f"{proj}/words.json"))["transcription"] if s["text"].strip()]
    caps, cur, start, prev_t = [], [], 0.0, 0.0
    for t, w in words:
        gap = t - prev_t
        if cur and (len(cur) >= 3 or len(" ".join(cur + [w])) > 20 or cur[-1][-1] in ",.:;?!" or gap > 0.45):
            caps.append([round(start, 2), " ".join(cur)])
            cur = []
        if not cur:
            start = t
        cur.append(w)
        prev_t = t
    if cur:
        caps.append([round(start, 2), " ".join(cur)])
    return caps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("project")
    ap.add_argument("--style", default="dorado-editorial"); ap.add_argument("--language", default="es")
    a = ap.parse_args()
    style = json.load(open(f"{SKILL}/styles/{a.style}.json"))
    os.makedirs(a.project, exist_ok=True)
    prepare_media(a.video, a.project, style)
    fetch_fonts(a.project, style)
    fetch_gsap(a.project)
    safe_top = detect_faces(a.project)
    caps = transcribe(a.project, a.language)
    for name, data in (("hyperframes.json", {"paths": {"assets": "assets"}}),
                       ("meta.json", {"id": os.path.basename(os.path.abspath(a.project)), "name": "reel"})):
        json.dump(data, open(f"{a.project}/{name}", "w"), indent=2)
    pj = f"{a.project}/project.json"
    if os.path.exists(pj):
        print("project.json ya existe; no lo sobrescribo. Subtítulos nuevos en project.draft.json")
        pj = f"{a.project}/project.draft.json"
    draft = {
        "style": a.style, "video_end": duration(f"{a.project}/assets/base.mp4"), "end_card_duration": 2.5,
        "safe_top": safe_top, "captions": caps, "captions_left_from": None,
        "hook": None, "chapters": [], "card": None, "callout": None,
        "punches": [], "emphasis": [], "product_zoom": None, "end_card": None,
    }
    json.dump(draft, open(pj, "w"), ensure_ascii=False, indent=1)
    print(f"Listo. Zona segura desde y={safe_top}px. Revisa y completa {pj}")


if __name__ == "__main__":
    main()
