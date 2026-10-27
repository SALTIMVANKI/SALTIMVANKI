# Variables compartidas por los scripts (se carga con `source`).
WHISPER_MODEL="${WHISPER_MODEL:-$HOME/.saltimvanki/modelos/ggml-${WHISPER_MODELO:-small}.bin}"
if command -v whisper-cli >/dev/null; then
  WHISPER_BIN=whisper-cli
else
  WHISPER_BIN=whisper-cpp   # nombre antiguo en Homebrew
fi
TRABAJO="${TRABAJO:-trabajo}"
mkdir -p "$TRABAJO"
