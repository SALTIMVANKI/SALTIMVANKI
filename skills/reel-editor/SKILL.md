---
name: reel-editor
description: Monta reels verticales (Instagram/TikTok) a partir de un vídeo hablado a cámara, aplicando un estilo visual del catálogo (títulos, subtítulos con palabra clave, tarjetas, zooms, música y efectos). Úsalo cuando el usuario pida editar o montar un reel, adaptar el estilo de otro reel a su vídeo, añadir subtítulos animados o motion graphics, o reutilizar una plantilla de vídeo de Saltimvanki.
---

# Reel Editor

Convierte un vídeo vertical hablado a cámara en un reel montado con FFmpeg + HyperFrames
+ whisper.cpp. Todo se configura con un `project.json` y un estilo de `styles/`.
Los formatos y estilos disponibles están en `GUIA-DE-ESTILO.md`.

## Requisitos

`bash scripts/setup-video-tools.sh` (en la raíz del repo) instala FFmpeg, HyperFrames,
yt-dlp, whisper.cpp y el modelo de Whisper. Además: `pip install "opencv-python-headless<5"`.
Dominios necesarios en la red del entorno: `huggingface.co`, `*.hf.co`, `fonts.googleapis.com`,
`fonts.gstatic.com` y, para descargar reels de referencia, `*.instagram.com`, `*.cdninstagram.com`,
`*.fbcdn.net` (Instagram suele bloquear servidores; si falla, pide al usuario que suba el reel
o lo comparta por Google Drive con "cualquier persona con el enlace" y descárgalo de
`drive.usercontent.google.com/download?id=ID&export=download&confirm=t`).

## Flujo

1. **Referencia (si hay).** Saca una hoja de contactos (`ffmpeg -vf "fps=1,scale=180:-1,tile=8x8"`)
   y fotogramas clave recortados sin la interfaz de Instagram. Describe sus técnicas (gancho,
   subtítulos, capítulos, tarjetas, ritmo, transiciones, color) y relaciónalas con un formato
   y un estilo de la guía. Si no encaja ninguno, crea un estilo nuevo (ver la guía).
2. **Preparar.** `python3 scripts/prepare.py VIDEO PROYECTO --style dorado-editorial --language es`
   deja la base graduada a 1080×1920, la voz normalizada, las fuentes, GSAP, `faces.json`
   (zona segura bajo la cara) y un `project.json` con los subtítulos transcritos.
3. **Confirmar dudas.** Lee la transcripción y pregunta por nombres propios, marcas y frases
   que Whisper haya podido oír mal. Pide nombre del negocio, redes y logo para el cierre.
4. **Guion visual antes de renderizar.** Publica un guion (artifact) con una escena por bloque:
   fotograma real + diseño encima, tiempo, frase, lo que aparece y el movimiento de cámara.
   No renderices hasta que el usuario lo apruebe.
5. **Completar `project.json`** (esquema abajo) a partir del guion aprobado.
6. **Comprobar.** `python3 scripts/finish.py PROYECTO --snap 1,8,15,22,30` y revisa los
   fotogramas: nada duradero sobre la cara, flechas apuntando al producto, textos legibles.
7. **Renderizar y mezclar.** `python3 scripts/finish.py PROYECTO` → `PROYECTO/render/final.mp4`
   (≈2,5 min por 35 s). Mide: `ebur128` ≈ -15 LUFS y la música unos 13 dB bajo la voz.
   No puedes escuchar: dilo y pide al usuario que revise el audio con auriculares.
8. **Entregar** con SendUserFile y guarda el `project.json` en `templates/` si es reutilizable.

## Reglas de composición

- **La cara manda.** Nada que dure más de ~0,5 s se coloca sobre la cara. Todo lo duradero
  va desde `safe_top` (calculado en `faces.json`) hacia abajo. Los zooms se anclan en la
  barbilla (`50% 45%`) para no empujar la cara hacia los textos.
- **Zona de la interfaz de Instagram.** Evita textos por debajo de y≈1600 px y la columna
  derecha (x > 950) entre y=1000 y 1600, salvo etiquetas breves de producto.
- **Subtítulos.** De 2 a 4 palabras, palabra clave en `*dorado*`, una o dos por vídeo en
  `**grande**` (momentos emocionales). Corrige lo que Whisper oiga mal.
- **Producto.** Si señala una joya/producto, usa `callout` con flecha apuntando al objeto real
  (compruébalo con `--snap`) y pasa los subtítulos a la izquierda (`captions_left_from`).
- **Sonido.** Cada elemento que entra lleva su efecto (lo asigna `build.py`): `whoosh` en
  transiciones y tarjetas, `pop` en pegatinas/etiquetas/palabras grandes, `shimmer` en títulos
  dorados, `tick` en zooms bruscos.

## Esquema de `project.json`

```jsonc
{
  "style": "dorado-editorial",          // archivo de styles/
  "video_end": 34.77,                   // duración del vídeo base (s)
  "end_card_duration": 2.5,
  "safe_top": 1210,                     // px; de faces.json
  "captions": [[0.0, "Como sabéis,"], [0.5, "la *Virgen del Carmen*"], [5.03, "a la **mar**"]],
  // [inicio, texto] o [inicio, texto, fin] para que no se quede en pantalla bajo pegatinas/tarjeta
  "captions_left_from": 28.76,          // null = siempre centrados
  "stickers": {"clear": 16.1, "items": [{"text": "Maricruz de la Harley", "at": 6.12, "x": 235, "y": 1335, "rot": -4, "fs": 36}]},
                                         // pila de pegatinas (x,y = centro); en "clear" tiemblan y salen volando
  "hook": {"start": 0.1, "end": 3.8, "line1": "La *Virgen del Carmen*", "line2": "PATRONA DE LOS MARINEROS",
           "sticker": {"text": "Sin mar → Por el río", "start": 1.6, "end": 3.8}},
  "chapters": [{"start": 7.35, "end": 11.45, "a": "Sevilla:", "b": "Por el río", "transition": true}],
  "card": {"start": 13.4, "end": 23.3, "title": "Las *2* Vírgenes del río", "tag": "GUÁRDALO",
           "items": [{"n": "I", "name": "Carmen de|Calatrava", "sub": "Dama de Calatrava", "at": 16.0}],
           "highlight": {"item": 0, "at": 21.88}, "name_px": 30},   // "|" = salto de línea; name_px = tamaño de los nombres
  "callout": {"start": 30.9, "end": 34.77, "text": "Escapulario *del Carmen*", "right": 60, "top": 1585, "arrow_right": 232},
  "punches": [3.8, 12.22, 23.4],        // saltos de zoom (falsos jump cuts) al empezar frase
  "emphasis": [26.62],                  // empujes lentos en el momento emocional
  "product_zoom": {"start": 30.8, "end": 34.4, "origin": "78% 86%"},
  "end_card": {"kicker": "ESCAPULARIOS DE LA", "title": "Virgen del Carmen", "brand": "OROBRIZ CARMEN", "sub": "JOYERÍA · SEVILLA"}
}
```

Ejemplos completos: `templates/virgen-del-carmen.json` (Dorado Editorial) y `templates/la-gran-maricruz.json` (Pop Atrevido).

Pausas largas: recórtalas con FFmpeg (`trim`/`atrim` + `concat`) **antes** de `prepare.py` y pon un `punch` en el punto de corte.
Nunca uses `random()` en GSAP: el render usa varios procesos y cada uno sacaría valores distintos.
