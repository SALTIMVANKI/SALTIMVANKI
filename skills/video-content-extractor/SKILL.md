---
name: video-content-extractor
description: Extrae transcripciones, metadatos y contenido de vídeos de TikTok, Instagram y YouTube (uno o varios enlaces a la vez). Úsalo cuando el usuario pida transcribir, analizar, resumir o descargar vídeos de estas plataformas a partir de una URL, o cuando pida investigar/comparar varios vídeos o el contenido de un creador.
---

# Video Content Extractor

Esta skill guía el uso de las herramientas del servidor MCP `TOKSCRIPT` para
extraer transcripciones y metadatos de vídeos de TikTok, Instagram y YouTube.

## Flujo de decisión

1. **Un único enlace** → usa la herramienta específica de la plataforma:
   - YouTube: `mcp__TOKSCRIPT__get_youtube_transcript`
   - TikTok: `mcp__TOKSCRIPT__get_tiktok_transcript`
   - Instagram: `mcp__TOKSCRIPT__get_instagram_transcript`

   Estas herramientas devuelven título, autor, duración, vistas, métricas de
   engagement (likes, comentarios, shares), miniatura y segmentos de
   transcripción con timestamps.

2. **Dos o más enlaces (mismo o distinto tipo de plataforma)** → NUNCA llames
   la herramienta de una sola URL varias veces. En su lugar:
   - `mcp__TOKSCRIPT__submit_transcript_job` para lanzar un trabajo asíncrono
     (devuelve `job_id` al momento) — preferible si el usuario no necesita el
     resultado en la misma respuesta, o si son muchos enlaces.
   - `mcp__TOKSCRIPT__get_bulk_transcripts` para obtener resúmenes por lotes
     de hasta 50 URLs en la misma llamada (sin esperar a un job).

3. **Colección/playlist de TikTok** (URL con `/collection/`) → usa
   `mcp__TOKSCRIPT__get_tiktok_collection`.

4. **Perfil de un creador** → usa `get_tiktok_user`, `get_tiktok_user_videos`,
   `get_instagram_user`, `get_instagram_user_posts`,
   `get_instagram_user_reels` o `get_youtube_user_shorts` según la
   plataforma, para listar contenido antes de extraer transcripciones.

5. **Seguimiento de un job asíncrono** → sondea con
   `mcp__TOKSCRIPT__get_job_status` usando el `job_id` devuelto por
   `submit_transcript_job`. No hagas polling agresivo: espera unos segundos
   entre consultas.

6. **Leer el texto completo de un ítem dentro de un resultado bulk** → usa
   `mcp__TOKSCRIPT__get_stored_video` con `bulk_transcript_id` y
   `bulk_item_index`.

7. **Exportar todo el resultado** (transcripciones + metadatos) a un archivo
   descargable → `mcp__TOKSCRIPT__export_results` (JSON o CSV, expira en 7
   días).

8. **Descargar el vídeo en sí** (no la transcripción) → `download_video`
   (TikTok/Instagram, uno a uno) o `download_videos_bulk` (varios). YouTube
   no soporta descarga directa.

9. **Descargar solo la miniatura/portada** → `download_cover_image` o
   `download_cover_images_bulk`.

## Reintentos

Los ítems que fallan con "Transcript unavailable" o "Processing failed" en
resultados bulk suelen ser fallos transitorios del scraper, no un problema
real del vídeo. Vuelve a enviar solo esas URLs fallidas al menos una vez
antes de decirle al usuario que el vídeo no está disponible. No reintentes
ítems marcados explícitamente como posts de foto/carrusel (esos nunca tienen
transcripción).

## Límites conocidos

- Usuarios free: 5 extracciones individuales por día.
- `submit_transcript_job` y trabajos bulk grandes requieren plan Pro/Premium.
- Instagram no expone shares/reposts vía API pública (siempre `null`).
- `get_bulk_transcripts` admite hasta 50 URLs por llamada y devuelve
  resúmenes (título, autor, word_count, duración), no el texto completo —
  para el texto completo usa `get_stored_video` o `export_results`.

## Formato de salida al usuario

Cuando proceses varias URLs, informa siempre el desglose exacto (p. ej.
"10 URLs: 7 vídeos con transcripción, 3 fotos sin transcripción, 0
fallidos") en vez de omitir URLs silenciosamente.
