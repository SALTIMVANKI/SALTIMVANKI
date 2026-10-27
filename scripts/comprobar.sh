#!/usr/bin/env bash
# Comprueba que todas las herramientas del kit de vídeo están listas.
set -uo pipefail
source "$(dirname "$0")/comun.sh"

ok=0
revisar() { local nombre=$1; shift; if "$@" >/dev/null 2>&1; then echo "OK    $nombre"; else echo "FALTA $nombre"; ok=1; fi; }

revisar ffmpeg ffmpeg -version
revisar yt-dlp yt-dlp --version
revisar hyperframes npx --no-install hyperframes --version
revisar whisper "$WHISPER_BIN" --help
if [[ -f "$WHISPER_MODEL" ]]; then echo "OK    modelo ($WHISPER_MODEL)"; else echo "FALTA modelo ($WHISPER_MODEL)"; ok=1; fi

exit $ok
