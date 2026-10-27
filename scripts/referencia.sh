#!/usr/bin/env bash
# Descarga un reel de referencia (TikTok, Instagram, YouTube) con yt-dlp.
# Uso: bash scripts/referencia.sh URL
set -euo pipefail
mkdir -p referencias
yt-dlp -f "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b" --merge-output-format mp4 \
  -o "referencias/%(uploader)s_%(id)s.%(ext)s" "$1"
