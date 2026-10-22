# Reels Saltimvanki · instrucciones para el agente

Este proyecto monta reels verticales (Instagram/TikTok) a partir de vídeos hablados a cámara.

- Cuando te pidan editar, montar o subtitular un reel, o adaptar el estilo de otro reel,
  sigue **`skills/reel-editor/SKILL.md`** paso a paso y usa la guía `skills/reel-editor/GUIA-DE-ESTILO.md`.
- Herramientas: `bash scripts/setup-video-tools.sh` (FFmpeg, HyperFrames, yt-dlp, whisper.cpp
  + modelo de Whisper, OpenCV). Si algo falta, ejecútalo de nuevo.
- Adaptaciones para este ordenador (sustituyen lo que diga SKILL.md sobre "artifact" o "SendUserFile"):
  - **Guion visual**: escríbelo como un archivo HTML local (`PROYECTO/guion.html`) con un
    fotograma real por escena y el diseño encima, ábrelo en el navegador y espera la aprobación.
  - **Entrega**: indica la ruta de `PROYECTO/render/final.mp4` y ábrelo con el reproductor del sistema.
  - **Reels de Instagram**: si `yt-dlp` falla por inicio de sesión, usa
    `yt-dlp --cookies-from-browser chrome URL` (o el navegador que use) o pide que suba el archivo.
- Guarda cada proyecto en `proyectos/NOMBRE/` y no subas vídeos al repositorio.
- No renderices nunca sin que el guion visual esté aprobado.
