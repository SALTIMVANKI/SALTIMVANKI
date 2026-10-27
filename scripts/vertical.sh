#!/usr/bin/env bash
# Convierte cualquier vídeo a reel vertical 1080x1920, 30 fps, H.264 + AAC.
# Rellena con fondo desenfocado si el original no es vertical.
# Uso: bash scripts/vertical.sh entrada.mp4 [salida.mp4]
set -euo pipefail
entrada="$1"
salida="${2:-salida/$(basename "${entrada%.*}")_vertical.mp4}"
mkdir -p "$(dirname "$salida")"

ffmpeg -y -i "$entrada" -filter_complex \
  "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:2[fondo];
   [0:v]scale=1080:1920:force_original_aspect_ratio=decrease[frente];
   [fondo][frente]overlay=(W-w)/2:(H-h)/2,fps=30,format=yuv420p[v]" \
  -map "[v]" -map "0:a?" -c:v libx264 -preset medium -crf 20 -c:a aac -b:a 160k \
  -movflags +faststart "$salida"
echo "$salida"
