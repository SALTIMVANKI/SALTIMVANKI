#!/usr/bin/env python3
"""Música suave (arpegios de guitarra Karplus-Strong) + efectos, sin derechos de autor.

Uso: python3 audio.py CARPETA_SALIDA DURACION_S STYLE_JSON
El estilo define bpm y acordes (por defecto, cadencia andaluza Am-G-F-E).
"""
import json, sys, wave
import numpy as np

SR = 48000
OUT = sys.argv[1]
STYLE = json.load(open(sys.argv[3]))["music"]
rng = np.random.default_rng(7)


def write(name, x):
    x = np.clip(x, -1, 1)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    with wave.open(f"{OUT}/{name}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x); acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc; y[i] = acc
    return y


def pluck(freq, dur, bright=0.5):
    n = int(SR * dur); p = int(SR / freq)
    buf = lowpass(rng.uniform(-1, 1, p), 2000 + 4000 * bright)
    out = np.empty(n)
    for i in range(n):
        v = buf[i % p]; out[i] = v
        buf[i % p] = 0.996 * 0.5 * (v + buf[(i + 1) % p])
    return out * np.exp(-np.linspace(0, dur * 1.2, n))


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


# ---------- música ----------
DUR = float(sys.argv[2]) + 0.7; BPM = STYLE["bpm"]; beat = 60 / BPM; bar = beat * 4
chords = STYLE["chords"]  # notas MIDI; nota 0 = bajo
music = np.zeros((int(SR * (DUR + bar + 3)), 2))
pattern = [0, 2, 3, 4, 3, 2, 3, 4]  # índice de nota por corchea
t = 0.0; c = 0
while t < DUR:
    ch = chords[c % len(chords)]
    for k, idx in enumerate(pattern):
        st = t + k * beat / 2
        if st >= DUR: break
        note = pluck(midi(ch[idx]) * (1 + rng.normal(0, 0.0007)), 2.2, 0.35 if k else 0.5)
        if k == 0:
            note = pluck(midi(ch[idx]), 2.6, 0.5) + 0.9 * pluck(midi(ch[0]), 2.6, 0.2)  # bajo
        pan = 0.5 + 0.25 * np.sin(k)
        s = int(st * SR) + rng.integers(0, 120)
        gain = 0.30 if k == 0 else 0.20
        note = note[: len(music) - s]
        music[s:s + len(note), 0] += note * gain * (1 - pan) * 2
        music[s:s + len(note), 1] += note * gain * pan * 2
    # pad suave
    pn = int(bar * SR); tt = np.arange(pn) / SR
    env = np.minimum(1, tt / 1.2) * np.minimum(1, (bar - tt) / 1.0)
    pad = sum(np.sin(2 * np.pi * midi(m + 12) * tt + i) for i, m in enumerate(ch[1:4])) * env * 0.035
    s = int(t * SR); music[s:s + pn, 0] += pad; music[s:s + pn, 1] += pad
    t += bar; c += 1
music = music[: int(SR * DUR)]
# reverb sencilla: ecos difusos
rev = np.zeros_like(music)
for d, g in [(0.031, .35), (0.047, .3), (0.071, .25), (0.113, .2), (0.163, .15), (0.241, .1)]:
    k = int(d * SR); rev[k:] += music[:-k] * g
music = music + 0.6 * rev[:, ::-1]
fade = np.ones(len(music)); fi = int(1.5 * SR); fo = int(3 * SR)
fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
music *= fade[:, None]
music /= np.abs(music).max() * 1.4
write("music", music)

# ---------- efectos ----------
def whoosh(d=0.5):
    n = int(SR * d); tt = np.linspace(0, 1, n)
    noise = rng.normal(0, 1, n)
    out = np.empty(n); acc = 0.0
    cut = 300 + 5000 * np.sin(np.pi * tt) ** 2
    for i in range(n):
        a = np.exp(-2 * np.pi * cut[i] / SR); acc = (1 - a) * noise[i] + a * acc; out[i] = acc
    env = np.sin(np.pi * tt) ** 1.5
    x = out * env; x /= np.abs(x).max()
    pan = np.linspace(0.2, 0.8, n)
    return np.stack([x * (1 - pan) * 1.4, x * pan * 1.4], 1) * 0.55


def pop(f0=900, d=0.12):
    n = int(SR * d); tt = np.arange(n) / SR
    f = f0 * np.exp(-tt * 18) + 180
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 38)
    return x * 0.7


def shimmer(d=1.4):
    n = int(SR * d); tt = np.arange(n) / SR; x = np.zeros(n)
    for i, m in enumerate([88, 91, 95, 100, 103]):
        st = int(i * 0.045 * SR)
        seg = tt[: n - st]
        x[st:] += np.sin(2 * np.pi * midi(m) * seg) * np.exp(-seg * 4.5) * 0.22
    return x


def tick(d=0.06):
    n = int(SR * d); tt = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2400 * tt) * np.exp(-tt * 90) + rng.normal(0, .3, n) * np.exp(-tt * 200)) * 0.5


write("whoosh", whoosh())
write("pop", pop())
write("shimmer", shimmer())
write("tick", tick())
print("ok")
