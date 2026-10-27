#!/usr/bin/env bash
# Instala el kit de vídeo de Saltimvanki en Mac (Homebrew) o Linux (apt).
# Uso: bash scripts/instalar.sh
set -euo pipefail

MODELOS="$HOME/.saltimvanki/modelos"
MODELO="${WHISPER_MODELO:-small}"   # small = buen equilibrio velocidad/calidad en español

if [[ "$(uname)" == "Darwin" ]]; then
  if ! command -v brew >/dev/null; then
    echo "Falta Homebrew. Instálalo desde https://brew.sh y vuelve a ejecutar este script."
    exit 1
  fi
  brew install ffmpeg yt-dlp whisper-cpp node
else
  sudo apt-get update
  sudo apt-get install -y ffmpeg python3-pip pipx cmake build-essential git curl nodejs npm
  pipx install yt-dlp || pipx upgrade yt-dlp
  if ! command -v whisper-cli >/dev/null; then
    git clone --depth 1 https://github.com/ggml-org/whisper.cpp "$HOME/.saltimvanki/whisper.cpp"
    cmake -S "$HOME/.saltimvanki/whisper.cpp" -B "$HOME/.saltimvanki/whisper.cpp/build" -DCMAKE_BUILD_TYPE=Release
    cmake --build "$HOME/.saltimvanki/whisper.cpp/build" -j
    sudo ln -sf "$HOME/.saltimvanki/whisper.cpp/build/bin/whisper-cli" /usr/local/bin/whisper-cli
  fi
fi

npm install -g hyperframes

mkdir -p "$MODELOS"
if [[ ! -f "$MODELOS/ggml-$MODELO.bin" ]]; then
  curl -L -o "$MODELOS/ggml-$MODELO.bin" \
    "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-$MODELO.bin"
fi

bash "$(dirname "$0")/comprobar.sh"
