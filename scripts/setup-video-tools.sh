#!/usr/bin/env bash
# Instala y verifica las herramientas de edición de vídeo:
#   FFmpeg      -> cortar y mezclar vídeo/audio
#   HyperFrames -> subtítulos y gráficos (HTML + GSAP renderizado a MP4)
#   yt-dlp      -> descargar Reels/TikToks/YouTube
#   whisper.cpp -> transcripción para subtítulos automáticos
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

python3 -m pip install -q -U yt-dlp "opencv-python-headless<5" numpy 2>/dev/null \
  || python3 -m pip install -q -U --break-system-packages yt-dlp "opencv-python-headless<5" numpy

npm install -g "hyperframes@${HYPERFRAMES_VERSION}"
# Chrome headless que HyperFrames necesita para renderizar
hyperframes browser ensure

# whisper.cpp -> subtítulos automáticos (hyperframes transcribe)
WHISPER_DIR="${WHISPER_DIR:-/opt/whisper.cpp}"
if ! command -v whisper-cli >/dev/null; then
  [ -d "$WHISPER_DIR" ] || git clone -q --depth 1 https://github.com/ggml-org/whisper.cpp.git "$WHISPER_DIR"
  cmake -S "$WHISPER_DIR" -B "$WHISPER_DIR/build" -DCMAKE_BUILD_TYPE=Release -DWHISPER_BUILD_TESTS=OFF >/dev/null
  cmake --build "$WHISPER_DIR/build" -j"$(nproc)" --config Release >/dev/null
  ln -sf "$WHISPER_DIR/build/bin/whisper-cli" /usr/local/bin/whisper-cli
fi

# Modelo multilingüe "small" (sirve para español), mismo pin que usa HyperFrames.
# Requiere acceso a huggingface.co; si no hay, HyperFrames lo reintentará al transcribir.
MODELS_DIR="$HOME/.cache/hyperframes/whisper/models"
MODEL="$MODELS_DIR/ggml-small.bin"
MODEL_SHA256="1be3a9b2063867b937e64e2ec7483364a79917e157fa98c5d94b5c1fffea987b"
if [ ! -f "$MODEL" ]; then
  mkdir -p "$MODELS_DIR"
  if curl -fsSL -o "$MODEL.part" \
      "https://huggingface.co/ggerganov/whisper.cpp/resolve/5359861c739e955e79d9a303bcbc70fb988958b1/ggml-small.bin" \
    && echo "$MODEL_SHA256  $MODEL.part" | sha256sum -c --quiet; then
    mv "$MODEL.part" "$MODEL"
  else
    rm -f "$MODEL.part"
    echo "AVISO: no se pudo descargar el modelo de Whisper (¿huggingface.co bloqueado?)" >&2
  fi
fi

echo
echo "FFmpeg:      $(ffmpeg -version | head -1)"
echo "yt-dlp:      $(yt-dlp --version)"
echo "HyperFrames: $(hyperframes --version)"
echo "whisper.cpp: $(command -v whisper-cli)"
echo "Modelo ES:   $( [ -f "$MODEL" ] && echo "$MODEL" || echo "no descargado")"
