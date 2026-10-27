# Saltimvanki — editor de reels

Este repositorio contiene la web de Saltimvanki (`index.html`) y el kit para
editar reels en local con la app de Codex. Responde siempre en español.

## Herramientas

| Herramienta | Para qué | Comprobar |
|---|---|---|
| FFmpeg | Cortar, mezclar, convertir, quemar subtítulos | `ffmpeg -version` |
| yt-dlp | Descargar reels de referencia | `yt-dlp --version` |
| HyperFrames (npm) | Títulos y animaciones en HTML renderizadas a vídeo | `npx hyperframes --help` |
| whisper.cpp | Transcribir voz en español a `.srt` | `whisper-cli --help` |

Modelo de Whisper: `~/.saltimvanki/modelos/ggml-small.bin` (multilingüe).

**Antes de la primera tarea de vídeo**, ejecuta `bash scripts/comprobar.sh`
(Mac/Linux). Si falta algo:
- Mac / Linux: `bash scripts/instalar.sh`
- Windows (PowerShell): `powershell -ExecutionPolicy Bypass -File scripts\instalar.ps1`

Pide permiso al usuario antes de instalar nada.

## Carpetas (ignoradas por git: nunca subas vídeos)

- `entrada/` — vídeos en bruto del usuario
- `referencias/` — reels descargados como referencia
- `trabajo/` — temporales (audio .wav, .srt, renders intermedios)
- `salida/` — reels terminados

## Scripts

- `scripts/vertical.sh entrada.mp4` → reel 1080x1920 con fondo desenfocado
- `scripts/subtitular.sh entrada.mp4` → transcribe y quema subtítulos (deja el `.srt` al lado para corregir)
- `scripts/referencia.sh URL` → descarga un reel a `referencias/`

## Formato de salida

MP4, H.264 + AAC, 1080x1920, 30 fps, `-movflags +faststart`. Subtítulos
blancos en negrita con borde negro, en el tercio inferior, máx. ~42
caracteres por línea.

## Flujo habitual de un reel

1. Si hay referencia, descárgala y analiza ritmo, duración de planos y estilo de textos.
2. Corta los clips de `entrada/` con FFmpeg y únelos en el orden pedido.
3. Pasa a vertical con `scripts/vertical.sh`.
4. Subtitula con `scripts/subtitular.sh`. Revisa el `.srt` (nombres propios
   como "Saltimvanki" suelen salir mal) y vuelve a quemarlo si lo corriges.
5. Títulos/animaciones: crea la composición con HyperFrames (consulta
   `npx hyperframes --help` para los comandos) y superponla con FFmpeg.
6. Deja el resultado en `salida/` y di al usuario la ruta y los comandos usados.

## Reglas

- No sobrescribas nunca los archivos de `entrada/`.
- Los scripts nuevos y reutilizables van en `scripts/` y se documentan aquí.
- Para descargar vídeos de TikTok/Instagram sin yt-dlp, el usuario también
  tiene la skill `skills/video-content-extractor` (TOKSCRIPT).
