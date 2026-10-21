# Guía de estilo visual · Reels Saltimvanki

Catálogo vivo de **formatos** (cómo se estructura el vídeo) y **estilos** (cómo se ve y suena).
Un reel = un formato + un estilo. Cada vez que montemos un vídeo nuevo que funcione,
se añade aquí como plantilla.

| Para pedir… | Di algo como |
|---|---|
| Un reel con una plantilla existente | "Monta este vídeo con *Explicativo con producto* en *Dorado Editorial*" |
| Adaptar el estilo de otro reel | "Analiza este reel y adáptalo a mi vídeo" (se añade a la guía como formato o estilo nuevo) |
| Cambiar solo los colores | "Igual que Dorado Editorial pero con los colores de la marca X" |

---

## Formatos

### F1 · Explicativo a cámara con producto ✅ probado
*Ejemplo: Virgen del Carmen · Orobriz Carmen (`templates/virgen-del-carmen.json`).*

Una persona cuenta algo cercano (tradición, consejo, historia) y lo conecta con un producto
de la tienda. Funciona con un solo plano de móvil de 30–60 s.

| Tramo | Duración | Elementos |
|---|---|---|
| Gancho | 0–4 s | Título dorado + subtítulo espaciado, pegatina amarilla con la idea en una línea, empuje lento |
| Contexto | 4–7 s | Solo subtítulos; una palabra **grande**; salto de zoom |
| Capítulo 1 | 7–13 s | Barrido dorado + título de capítulo con chispas |
| Dato para guardar | 13–23 s | Tarjeta crema "GUÁRDALO" abajo, columnas que aparecen al nombrarlas, resaltado amarillo del dato clave |
| Emoción | 23–28 s | Palabra **grande** ("precioso"), empuje de cámara |
| Producto + invitación | 28–35 s | Barrido + capítulo "Regala el…", etiqueta con flecha al producto, zoom al producto, subtítulos a la izquierda |
| Cierre de marca | +2,5 s | Fondo desenfocado, frase dorada, tarjeta con la marca |

### F2 · Tutorial por pasos ⚪ disponible, sin probar aún
*Estructura del reel de referencia ("My Claude Edits System, 5 Steps").*

Gancho con promesa ("5 pasos → sin curso"), cada paso como capítulo
(`"a": "Paso 1:"`, `"b": "Nombre"`) con barrido, y una tarjeta "GUÁRDALO" con las
herramientas o materiales. Se monta con el mismo motor: solo cambia el `project.json`.
El reel original además intercalaba grabaciones de pantalla a pantalla completa; eso aún no
está en el motor.

---

## Estilos

### E1 · Dorado Editorial ✅ (`styles/dorado-editorial.json`)
Cálido, elegante y artesanal: encaja con joyería, moda, gastronomía y tradiciones.

- **Color:** dorado `#F5D27F` (palabras clave), dorado profundo `#C99A3B`, crema `#FFF8EC`
  (tarjetas), tinta `#1D2433`, azul marino `#1E3557` (numerales), amarillo pegatina `#F6D04D`.
- **Tipografía:** *Playfair Display Italic* para palabras clave y títulos; **Figtree** 700–800
  para subtítulos y textos.
- **Imagen:** gradación cálida suave (+contraste, +saturación, piel y oro realzados), viñeta ligera.
- **Movimiento:** empujes lentos (+3 %), saltos de zoom al 108 % en frases clave, alejamiento
  cuando entra una tarjeta, zoom al producto al 112 %, barrido dorado diagonal de 0,5 s.
- **Sonido:** guitarra en arpegios sobre cadencia andaluza (La m–Sol–Fa–Mi) a 76 bpm,
  13 dB bajo la voz y bajando sola cuando se habla; efectos whoosh / pop / shimmer / tick.

---

## Reglas comunes a todos los estilos

1. **Nada duradero tapa la cara.** La zona segura se calcula sola (`faces.json`); los textos
   van debajo. Solo las transiciones (≤0,5 s) pasan por encima.
2. **Respeta la interfaz de Instagram:** nada importante por debajo de y≈1600 px ni en la
   columna de iconos de la derecha.
3. **Subtítulos cortos** (2–4 palabras), una palabra clave dorada por frase como mucho y
   una o dos palabras grandes por vídeo.
4. **Cada elemento que entra suena.** Sin música por encima de la voz.
5. **Guion visual aprobado antes de renderizar.**

## Cómo añadir un formato o estilo nuevo

- **Estilo:** copia `styles/dorado-editorial.json`, cambia colores, fuentes (URL de Google Fonts),
  gradación, intensidad de cámara y acordes/bpm de la música. Añade una ficha en "Estilos".
- **Formato:** guarda el `project.json` del vídeo en `templates/` y describe su estructura por
  tramos en "Formatos".
