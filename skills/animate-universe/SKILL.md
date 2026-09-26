---
name: animate-universe
description: Dirigir una animación o vídeo corto a partir de una imagen de referencia, preservando su identidad visual y diseñando acciones, planos, cámara y ritmo. Usar cuando el usuario adjunte una imagen y pida animarla, darle vida, convertirla en vídeo, entrar en su universo, crear un prompt image-to-video o diga /animate-universe con modos auto, poetic, playful, energetic o cinematic. No activar por una imagen adjunta sin intención de animación.
---

# Animate Universe

Tratar la imagen como el primer plano de una secuencia. La imagen define el mundo; dirigir cómo se mueve y cómo lo descubre la cámara. Priorizar la intención concreta del usuario sobre cualquier modo predeterminado.

## Entrada y modos

Aceptar `/animate-universe [modo] [duración]` o una petición natural equivalente. Modo por defecto: `auto`. Si falta duración, elegir una duración breve adecuada a la herramienta y explicitarla. Interpretar también instrucciones de formato, intensidad, plataforma, sonido y desenlace.

- `auto`: inferir acciones, cámara y ritmo de la imagen.
- `poetic`: profundidad, escala, transiciones fluidas y revelaciones.
- `playful`: descubrimientos, POV, cambios de altura y sorpresas.
- `energetic`: cortes rítmicos, tracking rápido, whip pans o crash zooms selectivos.
- `cinematic`: progresión narrativa, continuidad espacial, tensión y cierre.

Los modos modifican la dirección, no sustituyen las características de la imagen. Una petición de movimiento suave prevalece sobre `energetic` implícito. No introducir todos los movimientos de cámara en cada vídeo.

## Procedimiento

1. Inspeccionar la imagen real. Identificar técnica, pincelada o material, textura, paleta, proporciones, personajes, composición, profundidad, ambiente y posibles movimientos. Distinguir lo visible de lo que el modelo tendría que inventar fuera de cuadro.
2. Elegir acciones naturales y una lógica de cámara propia de ese universo. Leer [patrones.md](references/patrones.md) cuando ayude a decidir la dirección; adaptar el principio, nunca copiar personajes o acciones de otro ejemplo.
3. Diseñar una secuencia realizable para la duración: apertura fiel a la imagen, dos o tres descubrimientos o acciones legibles y cierre. Para 10 segundos, preferir 3 a 5 momentos claros; evitar exigir ocho escenas complejas si perjudica continuidad y fidelidad.
4. Redactar un prompt listo para la herramienta elegida, normalmente en inglés cuando el modelo de vídeo lo admita. Incluir referencia visual, invariantes de estilo, acciones, secuencia de planos, cámara, ritmo y cierre. Precisar qué puede expandirse y qué debe conservarse. Evitar negaciones genéricas que contradigan una foto o render deliberadamente realista.
5. Si el usuario pide generar el vídeo, usar una herramienta image-to-video disponible y compatible con la referencia. Consultar la skill específica de esa herramienta y respetar sus límites. No afirmar que se generó si solo se preparó un prompt. Si no hay herramienta suficiente, entregar prompt y guía breve de uso.

## Fidelidad y control

- Preservar técnica, textura, paleta, diseño y proporciones de sujetos reconocibles a lo largo de todos los planos. En ilustración, evitar realismo, 3D y limpieza digital ajenos a la referencia; en fotografía, preservar su lenguaje fotográfico.
- Mantener continuidad de orientación, número de sujetos y elementos principales. Tratar vistas no presentes como extensiones plausibles, no como detalles verificables de la imagen.
- En secuencias complejas, separar planos en generaciones o imágenes clave cuando un único clip pierda consistencia; proponer esa ruta sin prometer que una sola imagen controla todos los ángulos.
- No asumir que subir una imagen autoriza generar vídeo, gastar créditos o publicar. Una petición explícita de animarla sí autoriza la generación solicitada.

## Salida

Si piden dirección o prompt: indicar modo, duración y relación de aspecto asumidos; dar una secuencia breve de planos y el prompt completo copiable. Si piden ejecución: entregar el resultado real y señalar cualquier límite visible. Adaptar la cantidad de detalle a la petición. No presentar las heurísticas visuales como clasificación infalible.
