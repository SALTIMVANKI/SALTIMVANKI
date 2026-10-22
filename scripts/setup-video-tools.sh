#!/usr/bin/env bash
# Instala y verifica las herramientas de edición de vídeo:
#   FFmpeg      -> cortar y mezclar vídeo/audio
#   HyperFrames -> subtítulos y gráficos (HTML + GSAP renderizado a MP4)
#   yt-dlp      -> descargar Reels/TikToks/YouTube
#   whisper.cpp -> transcripción para subtítulos automáticos
# Uso: bash scripts/setup-video-tools.sh   (Linux, macOS o Windows con WSL2/Ubuntu)
# Requiere Node.js >= 20 y Python >= 3.10.
set -euo pipefail

HYPERFRAMES_VERSION="0.8.185"
SUDO=""; [ "$(id -u)" -ne 0 ] && command -v sudo >/dev/null && SUDO="sudo"
CPUS="$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 4)"
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"; mkdir -p "$BIN_DIR"

# FFmpeg + herramientas para compilar whisper.cpp
if command -v apt-get >/dev/null; then
  $SUDO apt-get update -qq
  $SUDO apt-get install -y -qq ffmpeg git cmake build-essential curl python3-pip python3-venv
elif command -v brew >/dev/null; then
  brew list ffmpeg >/dev/null 2>&1 || brew install ffmpeg
  command -v cmake >/dev/null || brew install cmake
elif ! command -v ffmpeg >/dev/null; then
  echo "Instala FFmpeg y cmake manualmente: https://ffmpeg.org/download.html" >&2
  exit 1
fi
node -e 'process.exit(Number(process.versions.node.split(".")[0]) < 20 ? 1 : 0)' 2>/dev/null \
  || { echo "Necesitas Node.js 20 o superior: https://nodejs.org" >&2; exit 1; }

python3 -m pip install -q -U yt-dlp "opencv-python-headless<5" numpy 2>/dev/null \
  || python3 -m pip install -q -U --break-system-packages yt-dlp "opencv-python-headless<5" numpy

npm install -g "hyperframes@${HYPERFRAMES_VERSION}" || $SUDO npm install -g "hyperframes@${HYPERFRAMES_VERSION}"
# Chrome headless que HyperFrames necesita para renderizar
hyperframes browser ensure

# whisper.cpp -> subtítulos automáticos (hyperframes transcribe)
WHISPER_DIR="${WHISPER_DIR:-$HOME/.local/share/whisper.cpp}"
if ! command -v whisper-cli >/dev/null; then
  [ -d "$WHISPER_DIR" ] || git clone -q --depth 1 https://github.com/ggml-org/whisper.cpp.git "$WHISPER_DIR"
  cmake -S "$WHISPER_DIR" -B "$WHISPER_DIR/build" -DCMAKE_BUILD_TYPE=Release -DWHISPER_BUILD_TESTS=OFF >/dev/null
  cmake --build "$WHISPER_DIR/build" -j"$CPUS" --config Release >/dev/null
  ln -sf "$WHISPER_DIR/build/bin/whisper-cli" "$BIN_DIR/whisper-cli"
  case ":$PATH:" in *":$BIN_DIR:"*) ;; *) echo "AVISO: añade $BIN_DIR al PATH (export PATH=\"$BIN_DIR:\$PATH\")" >&2; export PATH="$BIN_DIR:$PATH";; esac
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
    && [ "$( (sha256sum "$MODEL.part" 2>/dev/null || shasum -a 256 "$MODEL.part") | cut -d' ' -f1)" = "$MODEL_SHA256" ]; then
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
