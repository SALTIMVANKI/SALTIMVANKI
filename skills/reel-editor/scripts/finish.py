#!/usr/bin/env python3
"""Construye, renderiza y mezcla el reel. Uso: python3 finish.py PROYECTO [--snap 1,8.5,20]

  --snap   solo genera fotogramas de control (sin render) en PROYECTO/snaps/
Salida: PROYECTO/render/final.mp4 (1080x1920, voz + música con ducking + efectos, ~-15 LUFS)
"""
import argparse, json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)


def run(*cmd, cwd=None):
    subprocess.run(cmd, check=True, cwd=cwd)


ap = argparse.ArgumentParser()
ap.add_argument("project"); ap.add_argument("--snap")
a = ap.parse_args()
P = os.path.abspath(a.project)
run("python3", "-I", f"{HERE}/build.py", P)
if a.snap:
    run("hyperframes", "snapshot", "--at", a.snap, "--no-end", "-o", "snaps", cwd=P)
    raise SystemExit(f"Fotogramas en {P}/snaps/")

meta = json.load(open(f"{P}/sfx.json"))
style = json.load(open(f"{P}/project.json"))["style"]
run("python3", "-I", f"{HERE}/audio.py", f"{P}/assets", str(meta["duration"]), f"{SKILL}/styles/{style}.json")
os.makedirs(f"{P}/render", exist_ok=True)
run("hyperframes", "render", "-o", "render/visual.mp4", cwd=P)

D, sfx = meta["duration"], meta["sfx"]
ins = ["-i", "render/visual.mp4", "-i", "assets/voice.wav", "-i", "assets/music.wav"]
for _, n, _ in sfx:
    ins += ["-i", f"assets/{n}.wav"]
f = ["[1:a]asplit=2[v][sc]",
     f"[2:a]atrim=0:{D},volume={meta['music_volume']},afade=t=out:st={D - 1.5}:d=1.5[m0]",
     "[m0][sc]sidechaincompress=threshold=0.05:ratio=3:attack=40:release=450:makeup=1[m]"]
for i, (t, n, v) in enumerate(sfx):
    ms = int(t * 1000)
    f.append(f"[{i + 3}:a]volume={v * 0.6:.3f},adelay={ms}|{ms}[s{i}]")
labels = "".join(f"[s{i}]" for i in range(len(sfx)))
f.append(f"[v][m]{labels}amix=inputs={2 + len(sfx)}:normalize=0:duration=longest,atrim=0:{D},alimiter=limit=0.89[mix]")
run("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(f), "-map", "0:v", "-map", "[mix]",
    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", "render/final.mp4", cwd=P)
print(f"Listo: {P}/render/final.mp4")
