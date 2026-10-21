#!/usr/bin/env bash
# Instala y verifica las 3 herramientas de edición de vídeo:
#   FFmpeg      -> cortar y mezclar vídeo/audio
#   HyperFrames -> subtítulos y gráficos (HTML + GSAP renderizado a MP4)
#   yt-dlp      -> descargar Reels/TikToks/YouTube
# Uso: bash scripts/setup-video-tools.sh
set -euo pipefail

HYPERFRAMES_VERSION="0.8.185"

if ! command -v ffmpeg >/dev/null; then
  if command -v apt-get >/dev/null; then
    apt-get update -qq && apt-get install -y -qq ffmpeg
  elif command -v brew >/dev/null; then
    brew install ffmpeg
  else
    echo "Instala FFmpeg manualmente: https://ffmpeg.org/download.html" >&2
    exit 1
  fi
fi

python3 -m pip install -q -U yt-dlp 2>/dev/null \
  || python3 -m pip install -q -U --break-system-packages yt-dlp

npm install -g "hyperframes@${HYPERFRAMES_VERSION}"
# Chrome headless que HyperFrames necesita para renderizar
hyperframes browser ensure

echo
echo "FFmpeg:      $(ffmpeg -version | head -1)"
echo "yt-dlp:      $(yt-dlp --version)"
echo "HyperFrames: $(hyperframes --version)"
