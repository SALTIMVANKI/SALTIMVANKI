# Reel Virgen del Carmen — Orobriz Carmen

Fuentes para regenerar el reel (estilo adaptado del reel de referencia).
Los vídeos y audios no se versionan; se generan con estos scripts.

1. `faces.py VIDEO salida.json` — posición de la cara en el tiempo (zona segura: 0–62 % de alto).
2. `gen_audio.py assets/` — música suave (cadencia andaluza) y efectos (whoosh, pop, shimmer, tick).
3. `build_comp.py DIR` — composición HyperFrames (`index.html`) y lista de efectos (`sfx.json`).
4. `hyperframes render -o render/visual.mp4` y después `bash mix.sh` (voz + música con ducking + efectos).

Necesita `assets/base.mp4`, `assets/endbg.jpg`, `assets/voice.wav`, `fonts/`, `gsap.min.js`
(ver `scripts/setup-video-tools.sh` para las herramientas).
