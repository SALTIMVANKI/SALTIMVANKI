#!/usr/bin/env bash
# Transcribe un vídeo en español con whisper.cpp y quema los subtítulos.
# Deja también el .srt junto al vídeo final para poder corregirlo.
# Uso: bash scripts/subtitular.sh entrada.mp4 [salida.mp4]
set -euo pipefail
source "$(dirname "$0")/comun.sh"
entrada="$1"
nombre="$(basename "${entrada%.*}")"
salida="${2:-salida/${nombre}_subtitulado.mp4}"
mkdir -p "$(dirname "$salida")"

ffmpeg -y -i "$entrada" -vn -ar 16000 -ac 1 -c:a pcm_s16le "$TRABAJO/$nombre.wav"
"$WHISPER_BIN" -m "$WHISPER_MODEL" -l es -ml 42 -osrt -of "$TRABAJO/$nombre" -f "$TRABAJO/$nombre.wav"
cp "$TRABAJO/$nombre.srt" "${salida%.*}.srt"

estilo="FontName=Arial,FontSize=14,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,Alignment=2,MarginV=60"
ffmpeg -y -i "$entrada" -vf "subtitles=$TRABAJO/$nombre.srt:force_style='$estilo'" \
  -c:v libx264 -preset medium -crf 20 -c:a copy -movflags +faststart "$salida"
echo "$salida"
