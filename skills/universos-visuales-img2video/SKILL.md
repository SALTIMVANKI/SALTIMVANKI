---
name: universos-visuales-img2video
description: Escribe prompts de image-to-video (Seedance, Kling, Veo, Higgsfield, Magnific…) a partir de UNA imagen de referencia ilustrada, protegiendo su estilo pictórico y convirtiéndola en una secuencia dinámica de varios planos. Úsala cuando el usuario quiera animar una ilustración, "dar vida" a un universo visual, pida un prompt para Seedance u otro modelo image-to-video, o mencione mantener el estilo, textura o pincelada de una imagen al animarla.
---

# Universos visuales: 1 imagen + 1 prompt

Workflow: **1 imagen de referencia + 1 prompt**. La imagen se genera o se
explora antes (p. ej. con Krea Agent) y después se lleva a un modelo
image-to-video (p. ej. Seedance 2.5) para animarla.

> **La imagen define el mundo. El prompt define cómo se mueve ese mundo.**

Una imagen con identidad visual potente ya contiene composición, paleta,
textura, pincelada, diseño de personajes, iluminación, atmósfera, nivel de
abstracción y lenguaje visual. Por eso el prompt **no vuelve a describir la
imagen**: se centra en el movimiento, la cámara y el montaje.

## El riesgo que hay que evitar

En image-to-video, al pedir cámara o acciones complejas, el modelo tiende a
convertir la ilustración en algo demasiado realista, demasiado 3D, demasiado
limpio, demasiado "cinematográfico" o alejado de la técnica original.

Regla fija en todos los prompts: **mantener el estilo pictórico original**.
Con el estilo blindado, se puede ser mucho más agresivo con la cámara.

## Proceso

Antes de escribir, mira la imagen y anota: técnica (acuarela, gouache,
lana/fieltro, grabado, collage…), paleta dominante, personajes/objetos,
elementos que podrían moverse de forma natural y tono (poético, infantil,
surrealista, editorial…).

Después construye el prompt en inglés con estos 6 bloques, en este orden:

1. **Imagen como base visual** — la referencia es la única fuente visual; no
   rediseñar el mundo.
   `Use the reference image as the only visual foundation.`
2. **Proteger el estilo** — nombra los rasgos concretos de ESTA imagen:
   brushwork, texture, color palette, proportions, simplified shapes,
   handmade quality, illustration style, composition, atmosphere. Añade
   siempre la negativa explícita:
   `Do not make the image photorealistic or alter its handmade illustration technique.`
3. **Dar vida a la escena** — elige solo acciones con sentido dentro de ese
   mundo: personajes, objetos, agua, nubes, vegetación, ropa, luces,
   criaturas, fondo. No hace falta que todo se mueva.
4. **Pensar en secuencia, no en "una imagen que se mueve"** — la referencia
   es el primer plano de una pequeña secuencia. Pide múltiples planos,
   encuadres distintos, primeros planos, planos generales, ángulos bajos,
   cenitales, POVs y cambios de perspectiva, para que el modelo imagine lo
   que existe *alrededor* de la imagen. Describe el recorrido plano a plano
   ("Start with…, rapidly push toward…, cut to…, then…, pull far back to
   reveal…").
5. **Lenguaje de cámara** — push-ins, pull-backs, tracking shots, whip pans,
   crash zooms, handheld, foreground wipes, parallax, camera orbit, fast
   reframing. No todo a la vez: selecciona según el universo.
6. **Montaje adaptado al estilo** (ver tabla) y **cierre reforzando el
   estilo**: `Preserve the original brush texture and handmade feeling in every frame.`

### Ritmo según el tipo de ilustración

| Universo visual | Ritmo / cámara recomendados |
|---|---|
| Surrealista | Cortes rapidísimos, crash zooms, cambios de escala bruscos |
| Infantil | Cámara juguetona, rebotes, órbitas, POVs de personajes |
| Editorial | Movimiento imperfecto, handheld, reencuadres rápidos |
| Poética | Escala, profundidad y cambios de perspectiva; pull-backs que revelan |

## Plantilla

```
Use the reference image as the only visual foundation. Create a [dynamic /
playful / contemplative] animated sequence with multiple shots, [camera
language elegida], while fully preserving the original [técnica], [textura],
[formas], [paleta concreta], composition, and [atmósfera]. Do not make the
image photorealistic or alter its handmade illustration technique.
Animate [elemento 1 + acción]. [Elemento 2 + acción]. [Elemento de fondo +
reacción sutil]. Start with the original wide shot, [plano 2], cut to
[plano 3], [transición], switch to [perspectiva nueva], then [revelación
final / pull-back]. Add [pases de cámara, capas de profundidad, foreground
elements crossing the frame]. Keep the scene [tono], but [visually
spectacular / constantly evolving]. Preserve the original [brush texture /
grain / stitches…] and handmade feeling in every frame.
```

## Checklist antes de entregar

- [ ] No re-describe la imagen entera; solo nombra rasgos de estilo a proteger.
- [ ] Incluye la negativa "not photorealistic / no alterar la técnica".
- [ ] Las acciones tienen sentido físico dentro de ese mundo.
- [ ] Hay una secuencia de planos concreta (inicio → desarrollo → revelación).
- [ ] La cámara y el ritmo encajan con el tipo de universo.
- [ ] Cierra reforzando el estilo "in every frame".

Entrega el prompt en inglés (bloque de cita o código) y, si es útil, una
breve explicación en español de las decisiones de cámara.

## Ejemplos

- [01 — Whale Island](ejemplos/01-whale-island.md) (universo poético, Seedance 2.5)
