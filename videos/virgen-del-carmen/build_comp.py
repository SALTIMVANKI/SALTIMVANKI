"""Genera la composición HyperFrames (index.html) y la lista de efectos de sonido (sfx.json)."""
import json, re, sys

OUT = sys.argv[1]
VID = 34.77          # fin del vídeo original
DUR = 37.3           # con tarjeta de cierre

# Subtítulos: (inicio, texto). *x* = palabra clave dorada, **x** = palabra grande.
CAPS = [
    (0.00, "Como sabéis,"), (0.50, "la *Virgen del Carmen*"), (1.38, "es la patrona"),
    (1.92, "de los *marineros*"), (2.70, "en casi todos"), (3.36, "los pueblos costeros"),
    (4.38, "pues salen"), (5.03, "a la **mar**"), (5.60, "embarca"), (6.11, "y es súper bonito,"),
    (7.38, "pero en *Sevilla*"), (7.91, "tiene una"), (8.23, "*peculiaridad*"),
    (9.20, "que como no"), (9.85, "tenemos mar"), (10.58, "y lo que tenemos"),
    (11.52, "es el *río*,"), (12.22, "sale por el *río*."),
    (13.36, "Y hay *dos*"), (14.09, "Vírgenes del Carmen"), (15.09, "que salen por el río:"),
    (16.00, "la de la Dama"), (16.66, "de *Calatrava*"), (17.40, "y luego la de la"),
    (18.36, "Virgen del Carmen"), (19.56, "del *Puente de Triana*,"), (21.08, "que esa sale"),
    (21.88, "*mañana* por la tarde,"), (23.40, "así que si no"), (24.16, "la habéis visto"),
    (24.77, "nunca,"), (25.53, "la verdad es que es"), (26.67, "**precioso**"),
    (27.27, "y es algo"), (27.83, "*muy de aquí*."), (28.76, "Así que"), (29.16, "os *invito*"),
    (29.68, "a que vayáis a verla,"), (30.76, "y además"), (31.55, "que sepáis"),
    (32.20, "que si queréis"), (32.87, "regalarle a alguien"), (33.73, "un **escapulario**"),
]
LEFT_FROM = 28.76  # en el último bloque los subtítulos van a la izquierda (el medallón está a la derecha)


def fmt(t):
    t = re.sub(r"\*\*(.+?)\*\*", r'<span class="kw big">\1</span>', t)
    return re.sub(r"\*(.+?)\*", r'<span class="kw">\1</span>', t)


caps_html = []
for i, (s, txt) in enumerate(CAPS):
    e = CAPS[i + 1][0] if i + 1 < len(CAPS) else VID
    cls = "cap left" if s >= LEFT_FROM else "cap"
    caps_html.append(f'<div class="{cls}" data-start="{s}" data-duration="{round(e - s, 2)}"><span class="ln">{fmt(txt)}</span></div>')

# Efectos de sonido: (tiempo, archivo, volumen)
SFX = [
    (0.10, "shimmer", 0.55), (1.60, "pop", 0.7), (3.80, "tick", 0.5), (5.03, "pop", 0.6),
    (7.10, "whoosh", 0.8), (7.40, "shimmer", 0.5), (12.22, "tick", 0.5),
    (13.30, "whoosh", 0.6), (16.00, "pop", 0.6), (18.36, "pop", 0.6), (21.88, "tick", 0.6),
    (23.40, "tick", 0.45), (26.62, "shimmer", 0.6), (28.50, "whoosh", 0.8), (28.80, "shimmer", 0.45),
    (30.90, "pop", 0.65), (33.70, "shimmer", 0.55), (34.60, "whoosh", 0.7), (35.10, "shimmer", 0.5),
]
json.dump(SFX, open(f"{OUT}/sfx.json", "w"))

html = f"""<!doctype html>
<html lang="es" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="fonts/local.css" />
<script src="gsap.min.js"></script>
<style>
  :root {{
    --gold: #F5D27F; --gold-deep: #C99A3B; --cream: #FFF8EC; --ink: #1D2433;
    --navy: #1E3557; --sticker: #F6D04D;
    --display: 'Playfair Display', Georgia, serif;
    --sans: 'Figtree', 'Helvetica Neue', Arial, sans-serif;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
  #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: var(--sans); }}
  /* cámara: dos capas para combinar zoom general (ancla en la barbilla) y zoom al medallón */
  #cam {{ position: absolute; inset: 0; transform-origin: 50% 45%; will-change: transform; }}
  #cam2 {{ position: absolute; inset: 0; transform-origin: 78% 86%; will-change: transform; }}
  #base {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
  #vignette {{ position: absolute; inset: 0; pointer-events: none;
    background: radial-gradient(ellipse 85% 70% at 50% 42%, transparent 55%, rgba(20,12,4,.38) 100%),
                linear-gradient(to bottom, transparent 58%, rgba(0,0,0,.30) 100%); }}

  /* zona segura: la cara ocupa 0-62 % de la altura -> todo lo duradero va de 1210 px hacia abajo */
  .cap {{ position: absolute; left: 60px; right: 60px; bottom: 330px; text-align: center;
    font-weight: 800; font-size: 68px; line-height: 1.08; color: #fff; letter-spacing: -.5px;
    text-shadow: 0 4px 14px rgba(0,0,0,.65), 0 0 30px rgba(0,0,0,.35); }}
  .cap.left {{ right: 400px; text-align: left; }}
  .cap .ln {{ display: inline-block; }}
  .kw {{ font-family: var(--display); font-style: italic; font-weight: 700; color: var(--gold);
    font-size: 1.12em; -webkit-text-stroke: 2px rgba(60,40,10,.45); paint-order: stroke fill; }}
  .kw.big {{ display: block; font-size: 2.1em; line-height: .95; }}

  .title {{ position: absolute; left: 0; right: 0; top: 1215px; text-align: center; color: #fff;
    text-shadow: 0 4px 18px rgba(0,0,0,.55); }}
  .title .l1 {{ font-family: var(--display); font-style: italic; font-weight: 500; font-size: 94px; line-height: 1; }}
  .title .l1 b {{ color: var(--gold); font-weight: 700; }}
  .title .l2 {{ margin-top: 14px; font-weight: 700; font-size: 30px; letter-spacing: 13px; }}
  .sticker {{ position: absolute; left: 92px; top: 1392px; transform: rotate(-3deg);
    background: var(--sticker); color: var(--ink); font-weight: 800; font-size: 50px;
    padding: 10px 26px 12px; border-radius: 14px; box-shadow: 0 10px 26px rgba(0,0,0,.35); }}

  .chap {{ position: absolute; left: 0; right: 0; top: 1225px; text-align: center; color: #fff;
    text-shadow: 0 4px 18px rgba(0,0,0,.55); white-space: nowrap; }}
  .chap .a {{ font-weight: 700; font-size: 56px; vertical-align: 10px; margin-right: 14px; }}
  .chap .b {{ font-family: var(--display); font-style: italic; font-weight: 700; font-size: 116px; color: var(--gold); }}
  .spark {{ position: absolute; color: #FFF1C9; font-size: 40px; text-shadow: 0 0 14px rgba(255,220,140,.9); }}

  .card {{ position: absolute; left: 60px; right: 60px; top: 1198px; background: var(--cream);
    border-radius: 34px; padding: 22px 34px 26px; color: var(--ink); box-shadow: 0 16px 44px rgba(0,0,0,.38); }}
  .card .hd {{ display: flex; justify-content: space-between; align-items: baseline;
    border-bottom: 2px solid #E8DABD; padding-bottom: 12px; margin-bottom: 16px; }}
  .card .hd b {{ font-family: var(--display); font-style: italic; font-weight: 500; font-size: 52px; }}
  .card .hd b span {{ color: var(--gold-deep); font-weight: 700; }}
  .card .hd em {{ font-style: normal; font-weight: 700; font-size: 20px; letter-spacing: 5px; color: #B08B44; }}
  .card .cols {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; text-align: center; }}
  .card .n {{ font-family: var(--display); font-weight: 700; font-size: 46px; color: var(--navy); line-height: 1; }}
  .card .nm {{ font-weight: 800; font-size: 30px; line-height: 1.12; margin-top: 6px; }}
  .card .sub {{ display: inline-block; margin-top: 8px; font-size: 24px; font-weight: 600; color: #6B6252;
    padding: 2px 10px; border-radius: 8px; }}

  .pill {{ position: absolute; right: 60px; top: 1585px; background: var(--cream); color: var(--ink);
    font-weight: 800; font-size: 36px; padding: 14px 28px; border-radius: 60px;
    box-shadow: 0 10px 26px rgba(0,0,0,.35); }}
  .pill span {{ font-family: var(--display); font-style: italic; color: #9A7120; }}
  .arrow {{ position: absolute; right: 232px; top: 1668px; width: 6px; height: 62px; background: var(--gold);
    border-radius: 3px; transform-origin: top center; box-shadow: 0 0 10px rgba(0,0,0,.3); }}
  .arrow::after {{ content: ""; position: absolute; left: -13px; bottom: -6px; border: 16px solid transparent;
    border-top: 22px solid var(--gold); border-bottom: 0; }}

  .flash {{ position: absolute; inset: -200px; pointer-events: none;
    background: linear-gradient(115deg, transparent 0 35%, rgba(240,200,110,.95) 42% 58%, rgba(255,240,200,.9) 60%, transparent 68%); }}

  #endbg {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
  .end {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center;
    justify-content: center; gap: 38px; text-align: center; color: #fff; padding: 0 90px; }}
  .end .k1 {{ font-weight: 700; font-size: 44px; letter-spacing: 4px; }}
  .end .k2 {{ font-family: var(--display); font-style: italic; font-weight: 700; font-size: 120px; line-height: 1;
    color: var(--gold); text-shadow: 0 6px 24px rgba(0,0,0,.45); }}
  .end .brand {{ background: var(--cream); color: var(--ink); border-radius: 36px; padding: 34px 64px 30px;
    box-shadow: 0 18px 50px rgba(0,0,0,.4); }}
  .end .brand b {{ display: block; font-family: var(--display); font-weight: 700; font-size: 72px; letter-spacing: 6px; }}
  .end .brand small {{ display: block; margin-top: 8px; font-weight: 600; font-size: 30px; letter-spacing: 8px; color: #8A6A2A; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">

  <div id="cam"><div id="cam2">
    <video id="base" class="clip" src="assets/base.mp4" muted data-start="0" data-duration="{VID}"></video>
  </div></div>
  <div id="vignette"></div>

  <!-- 1 · Gancho -->
  <div id="t1" class="title" data-start="0.1" data-duration="3.7">
    <div class="l1">La <b>Virgen del Carmen</b></div>
    <div class="l2">PATRONA DE LOS MARINEROS</div>
  </div>
  <div id="stk" class="sticker" data-start="1.6" data-duration="2.2">Sin mar → Por el río</div>

  <!-- 3 · Capítulo Sevilla -->
  <div id="c1" class="chap" data-start="7.35" data-duration="4.1">
    <span class="a">Sevilla:</span><span class="b">Por el río</span>
    <span class="spark s1" style="left:250px;top:-30px">✦</span><span class="spark s2" style="left:820px;top:-10px">✦</span><span class="spark s3" style="left:900px;top:110px;font-size:26px">✦</span>
  </div>

  <!-- 4 · Tarjeta -->
  <div id="card" class="card" data-start="13.4" data-duration="9.9">
    <div class="hd"><b>Las <span>2</span> Vírgenes del río</b><em>GUÁRDALO</em></div>
    <div class="cols">
      <div id="col1"><div class="n">I</div><div class="nm">Carmen de<br>Calatrava</div><div class="sub">Dama de Calatrava</div></div>
      <div id="col2"><div class="n">II</div><div class="nm">Carmen del Puente<br>de Triana</div><div id="hl" class="sub">Mañana por la tarde</div></div>
    </div>
  </div>

  <!-- 6 · Capítulo escapulario -->
  <div id="c2" class="chap" data-start="28.8" data-duration="2.05">
    <span class="a">Regala el</span><span class="b">Escapulario</span>
    <span class="spark s4" style="left:200px;top:-26px">✦</span><span class="spark s5" style="left:880px;top:0px">✦</span>
  </div>
  <div id="pill" class="pill" data-start="30.9" data-duration="3.87">Escapulario <span>del Carmen</span></div>
  <div id="arr" class="arrow" data-start="31.05" data-duration="3.72"></div>

  <!-- subtítulos -->
  {chr(10).join('  ' + c for c in caps_html)}

  <!-- transiciones -->
  <div id="f1" class="flash" data-start="7.05" data-duration="0.5"></div>
  <div id="f2" class="flash" data-start="28.45" data-duration="0.5"></div>

  <!-- 7 · Cierre -->
  <img id="endbg" class="clip" src="assets/endbg.jpg" data-start="{VID}" data-duration="{round(DUR - VID, 2)}" />
  <div id="end" class="end" data-start="{VID}" data-duration="{round(DUR - VID, 2)}">
    <div id="e1" class="k1">ESCAPULARIOS DE LA</div>
    <div id="e2" class="k2">Virgen del Carmen</div>
    <div id="e3" class="brand"><b>OROBRIS CARMEN</b><small>JOYERÍA · SEVILLA</small></div>
  </div>
</div>

<script>
  const tl = gsap.timeline({{ paused: true }});
  const cam = "#cam", cam2 = "#cam2";

  // ---- cámara: empujes lentos, saltos de zoom en frases clave, alejamiento para la tarjeta ----
  tl.fromTo(cam, {{ scale: 1.0 }}, {{ scale: 1.06, duration: 3.8, ease: "none" }}, 0);
  tl.to(cam, {{ scale: 1.08, duration: 0.18, ease: "power3.out" }}, 3.8);
  tl.to(cam, {{ scale: 1.06, duration: 3.3, ease: "sine.inOut" }}, 3.98);
  tl.set(cam, {{ scale: 1.0 }}, 7.3);
  tl.to(cam, {{ scale: 1.04, duration: 4.9, ease: "none" }}, 7.3);
  tl.to(cam, {{ scale: 1.08, duration: 0.2, ease: "power3.out" }}, 12.22);
  tl.to(cam, {{ scale: 1.09, duration: 0.98, ease: "none" }}, 12.42);
  tl.to(cam, {{ scale: 1.02, duration: 1.2, ease: "power2.inOut" }}, 13.4);
  tl.to(cam, {{ scale: 1.05, x: -18, duration: 8.7, ease: "sine.inOut" }}, 14.6);
  tl.to(cam, {{ scale: 1.07, x: 0, duration: 0.18, ease: "power3.out" }}, 23.4);
  tl.to(cam, {{ scale: 1.08, duration: 3.1, ease: "none" }}, 23.58);
  tl.to(cam, {{ scale: 1.12, duration: 0.8, ease: "power2.out" }}, 26.62);
  tl.to(cam, {{ scale: 1.11, duration: 1.2, ease: "none" }}, 27.42);
  tl.set(cam, {{ scale: 1.0 }}, 28.7);
  tl.to(cam, {{ scale: 1.04, duration: 2.1, ease: "none" }}, 28.7);
  tl.to(cam2, {{ scale: 1.12, duration: 1.5, ease: "power2.inOut" }}, 30.8);
  tl.to(cam2, {{ scale: 1.0, duration: 1.8, ease: "power2.inOut" }}, 32.6);

  // ---- gancho ----
  tl.from("#t1 .l1", {{ opacity: 0, y: 30, filter: "blur(14px)", duration: 0.45, ease: "power3.out" }}, 0.1);
  tl.from("#t1 .l2", {{ opacity: 0, y: 14, scaleX: 1.25, duration: 0.6, ease: "power3.out" }}, 0.35);
  tl.to("#t1", {{ opacity: 0, y: -10, duration: 0.25 }}, 3.55);
  tl.from("#stk", {{ scale: 0, rotation: -14, duration: 0.42, ease: "back.out(2.4)" }}, 1.6);
  tl.to("#stk", {{ scale: 0.6, opacity: 0, duration: 0.2 }}, 3.6);

  // ---- transiciones (barrido dorado) ----
  ["#f1", "#f2"].forEach((f, i) => {{
    const t = i ? 28.45 : 7.05;
    tl.fromTo(f, {{ xPercent: -90 }}, {{ xPercent: 90, duration: 0.5, ease: "power2.inOut" }}, t);
  }});

  // ---- capítulos ----
  [["#c1", 7.35, 11.2], ["#c2", 28.8, 30.6]].forEach(([c, a, b]) => {{
    tl.from(c + " .a", {{ opacity: 0, x: -40, duration: 0.35, ease: "power3.out" }}, a);
    tl.from(c + " .b", {{ opacity: 0, scale: 0.8, filter: "blur(10px)", duration: 0.5, ease: "power3.out" }}, a + 0.1);
    tl.from(c + " .spark", {{ opacity: 0, scale: 0, rotation: -90, duration: 0.5, stagger: 0.1, ease: "back.out(3)" }}, a + 0.25);
    tl.to(c + " .spark", {{ scale: 1.35, opacity: 0.55, duration: 0.6, yoyo: true, repeat: 3, ease: "sine.inOut", stagger: 0.15 }}, a + 0.8);
    tl.to(c, {{ opacity: 0, y: -12, duration: 0.25 }}, b);
  }});

  // ---- tarjeta ----
  tl.from("#card", {{ y: 160, opacity: 0, duration: 0.55, ease: "power3.out" }}, 13.4);
  tl.from("#col1", {{ opacity: 0, y: 24, duration: 0.35, ease: "back.out(2)" }}, 16.0);
  tl.from("#col2", {{ opacity: 0, y: 24, duration: 0.35, ease: "back.out(2)" }}, 18.36);
  tl.to("#hl", {{ backgroundColor: "#F6D04D", color: "#1D2433", scale: 1.06, duration: 0.3, ease: "back.out(3)" }}, 21.88);
  tl.to("#card", {{ y: 140, opacity: 0, duration: 0.35, ease: "power2.in" }}, 23.0);

  // ---- etiqueta del escapulario ----
  tl.from("#pill", {{ scale: 0.4, opacity: 0, duration: 0.4, ease: "back.out(2.2)" }}, 30.9);
  tl.from("#arr", {{ scaleY: 0, duration: 0.35, ease: "power2.out" }}, 31.05);

  // ---- subtítulos: entrada con pequeño salto ----
  document.querySelectorAll(".cap").forEach((el) => {{
    const s = parseFloat(el.dataset.start);
    tl.from(el.querySelector(".ln"), {{ opacity: 0, y: 18, scale: 0.92, duration: 0.16, ease: "power2.out" }}, s);
    const big = el.querySelector(".big");
    if (big) tl.from(big, {{ scale: 0.4, opacity: 0, duration: 0.4, ease: "back.out(2.6)" }}, s);
  }});

  // ---- cierre ----
  tl.from("#endbg", {{ opacity: 0, duration: 0.35 }}, {VID});
  tl.from("#e1", {{ opacity: 0, y: 20, duration: 0.35, ease: "power3.out" }}, {VID} + 0.15);
  tl.from("#e2", {{ opacity: 0, scale: 0.85, filter: "blur(10px)", duration: 0.5, ease: "power3.out" }}, {VID} + 0.3);
  tl.from("#e3", {{ opacity: 0, y: 60, duration: 0.5, ease: "back.out(1.8)" }}, {VID} + 0.6);

  window.__timelines["main"] = tl;
  tl.seek(0);
</script>
</body>
</html>
"""
open(f"{OUT}/index.html", "w", encoding="utf-8").write(html)
print("ok", len(CAPS), "subtítulos")
