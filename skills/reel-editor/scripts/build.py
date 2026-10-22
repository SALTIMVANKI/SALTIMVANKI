#!/usr/bin/env python3
"""Genera la composición HyperFrames (index.html) y los efectos (sfx.json) desde project.json.

Uso: python3 build.py PROYECTO
Las posiciones verticales salen de safe_top: todo lo que dura en pantalla va por debajo de la cara.
"""
import html as H, json, os, random, re, sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = sys.argv[1]
pj = json.load(open(f"{P}/project.json"))
st = json.load(open(f"{SKILL}/styles/{pj['style']}.json"))
C, F, CAM = st["colors"], st["fonts"], st["camera"]
VID = pj["video_end"]
DUR = round(VID + (pj["end_card_duration"] if pj.get("end_card") else 0), 2)
S = pj["safe_top"]
sfx, body, js = [], [], []


def rich(t):
    """*palabra* -> clave dorada, **palabra** -> clave grande. El resto se escapa."""
    t = H.escape(t)
    t = re.sub(r"\*\*(.+?)\*\*", r'<span class="kw big">\1</span>', t)
    return re.sub(r"\*(.+?)\*", r'<span class="kw">\1</span>', t)


def clip(id_, cls, a, b, inner, style=""):
    st_ = f' style="{style}"' if style else ""
    body.append(f'<div id="{id_}" class="{cls}" data-start="{a}" data-duration="{round(b - a, 2)}"{st_}>{inner}</div>')


# ---------- gancho ----------
hook = pj.get("hook")
if hook:
    a, b = hook["start"], hook["end"]
    clip("t1", "title", a, b, f'<div class="l1">{rich(hook["line1"])}</div>' +
         (f'<div class="l2">{H.escape(hook["line2"])}</div>' if hook.get("line2") else ""))
    js += [f'tl.from("#t1 .l1", {{opacity:0, y:30, filter:"blur(14px)", duration:.45, ease:"power3.out"}}, {a});',
           f'tl.from("#t1 .l2", {{opacity:0, y:14, scaleX:1.25, duration:.6, ease:"power3.out"}}, {a + .25});',
           f'tl.to("#t1", {{opacity:0, y:-10, duration:.25}}, {b - .25});']
    sfx.append((a, "shimmer", .55))
    sk = hook.get("sticker")
    if sk:
        clip("stk", "sticker", sk["start"], sk["end"], H.escape(sk["text"]))
        js += [f'tl.from("#stk", {{scale:0, rotation:-14, duration:.42, ease:"back.out(2.4)"}}, {sk["start"]});',
               f'tl.to("#stk", {{scale:.6, opacity:0, duration:.2}}, {sk["end"] - .2});']
        sfx.append((sk["start"], "pop", .7))

# ---------- capítulos (+ barrido dorado opcional) ----------
resets = []
for i, ch in enumerate(pj.get("chapters", [])):
    a, b, cid = ch["start"], ch["end"], f"c{i}"
    clip(cid, "chap", a, b, f'<span class="a">{H.escape(ch["a"])}</span><span class="b">{H.escape(ch["b"])}</span>'
         '<span class="spark" style="left:22%;top:-30px">✦</span><span class="spark" style="left:78%;top:-8px">✦</span>'
         '<span class="spark" style="left:85%;top:110px;font-size:26px">✦</span>')
    js += [f'tl.from("#{cid} .a", {{opacity:0, x:-40, duration:.35, ease:"power3.out"}}, {a});',
           f'tl.from("#{cid} .b", {{opacity:0, scale:.8, filter:"blur(10px)", duration:.5, ease:"power3.out"}}, {a + .1});',
           f'tl.from("#{cid} .spark", {{opacity:0, scale:0, rotation:-90, duration:.5, stagger:.1, ease:"back.out(3)"}}, {a + .25});',
           f'tl.to("#{cid} .spark", {{scale:1.35, opacity:.55, duration:.6, yoyo:true, repeat:3, ease:"sine.inOut", stagger:.15}}, {a + .8});',
           f'tl.to("#{cid}", {{opacity:0, y:-12, duration:.25}}, {b - .25});']
    sfx.append((a + .05, "shimmer", .5))
    if ch.get("transition", True):
        fa = round(a - .3, 2)
        clip(f"f{i}", "flash", fa, fa + .5, "")
        js.append(f'tl.fromTo("#f{i}", {{xPercent:-90}}, {{xPercent:90, duration:.5, ease:"power2.inOut"}}, {fa});')
        sfx.append((fa - .2, "whoosh", .8))
        resets.append(round(a - .05, 2))

# ---------- tarjeta "guárdalo" ----------
card = pj.get("card")
if card:
    a, b = card["start"], card["end"]
    cols = "".join(
        f'<div id="ci{k}"><div class="n">{H.escape(it.get("n", ""))}</div><div class="nm" style="font-size:{card.get("name_px", 30)}px">{H.escape(it["name"]).replace("|", "<br>")}</div>'
        f'<div class="sub" id="cs{k}">{H.escape(it.get("sub", ""))}</div></div>' for k, it in enumerate(card["items"]))
    tag = f'<em>{H.escape(card["tag"])}</em>' if card.get("tag") else ""
    clip("card", "card", a, b, f'<div class="hd"><b>{rich(card["title"])}</b>{tag}</div>'
         f'<div class="cols" style="grid-template-columns:repeat({len(card["items"])},1fr)">{cols}</div>')
    js += [f'tl.from("#card", {{y:160, opacity:0, duration:.55, ease:"power3.out"}}, {a});',
           f'tl.to("#card", {{y:140, opacity:0, duration:.35, ease:"power2.in"}}, {b - .35});']
    sfx.append((a - .1, "whoosh", .6))
    for k, it in enumerate(card["items"]):
        if it.get("at"):
            js.append(f'tl.from("#ci{k}", {{opacity:0, y:24, duration:.35, ease:"back.out(2)"}}, {it["at"]});')
            sfx.append((it["at"], "pop", .6))
    hl = card.get("highlight")
    if hl:
        js.append(f'tl.to("#cs{hl["item"]}", {{backgroundColor:"{C["sticker"]}", color:"{C["ink"]}", scale:1.06, duration:.3, ease:"back.out(3)"}}, {hl["at"]});')
        sfx.append((hl["at"], "tick", .6))

# ---------- etiqueta de producto ----------
co = pj.get("callout")
if co:
    a, b = co["start"], co["end"]
    clip("pill", "pill", a, b, rich(co["text"]), f'right:{co.get("right", 60)}px;top:{co["top"]}px')
    js.append(f'tl.from("#pill", {{scale:.4, opacity:0, duration:.4, ease:"back.out(2.2)"}}, {a});')
    sfx.append((a, "pop", .65))
    if co.get("arrow_right") is not None:
        clip("arr", "arrow", a + .15, b, "", f'right:{co["arrow_right"]}px;top:{co["top"] + 83}px')
        js.append(f'tl.from("#arr", {{scaleY:0, duration:.35, ease:"power2.out"}}, {a + .15});')

# ---------- pila de pegatinas (se acumulan y salen volando) ----------
pile = pj.get("stickers")
if pile:
    pal = C.get("sticker_palette", [C["sticker"]])
    clear = pile["clear"]
    for k, it in enumerate(pile["items"]):
        bg = it.get("color", pal[k % len(pal)])
        fg = "#fff" if bg.lower() in ("#3b4bff", "#1e3557", "#e0207a") else C["ink"]
        clip(f"pl{k}", "pst", it["at"], clear + .6, H.escape(it["text"]),
             f'left:{it["x"]}px;top:{it["y"]}px;background:{bg};color:{fg};font-size:{it.get("fs", 44)}px')
        js.append(f'tl.set("#pl{k}", {{xPercent:-50, yPercent:-50, rotation:{it.get("rot", 0)}}}, 0);')
        js.append(f'tl.from("#pl{k}", {{scale:0, rotation:{it.get("rot", 0) - 20}, duration:.35, ease:"back.out(2.6)", immediateRender:false}}, {it["at"]});')
        sfx.append((it["at"], "pop", .55))
    # valores fijos por pegatina: el render usa varios procesos y random() daría resultados distintos
    rnd = random.Random(7)
    for k, it in enumerate(pile["items"]):
        r0 = it.get("rot", 0)
        js.append(f'tl.to("#pl{k}", {{x:{rnd.uniform(-14, 14):.1f}, rotation:{r0 + rnd.uniform(-6, 6):.1f}, duration:.06, repeat:4, yoyo:true}}, {clear - .32});')
        js.append(f'tl.to("#pl{k}", {{y:{rnd.uniform(500, 800):.0f}, x:{rnd.uniform(-300, 300):.0f}, rotation:{rnd.uniform(-90, 90):.0f}, '
                  f'opacity:0, duration:.55, ease:"power2.in"}}, {clear + k * .025:.3f});')
    sfx.append((clear - .05, "whoosh", .8))

# ---------- subtítulos ----------
caps, left_from = pj["captions"], pj.get("captions_left_from")
emph = set(pj.get("emphasis", []))
for i, cap in enumerate(caps):
    s, txt = cap[0], cap[1]
    e = cap[2] if len(cap) > 2 else (caps[i + 1][0] if i + 1 < len(caps) else VID)  # 3er valor = fin explícito
    cls = "cap left" if left_from is not None and s >= left_from else "cap"
    clip(f"k{i}", cls, s, e, f'<span class="ln">{rich(txt)}</span>')
    js.append(f'tl.from("#k{i} .ln", {{opacity:0, y:18, scale:.92, duration:.16, ease:"power2.out"}}, {s});')
    if "**" in txt:
        js.append(f'tl.from("#k{i} .big", {{scale:.4, opacity:0, duration:.4, ease:"back.out(2.6)"}}, {s});')
        if not any(abs(s - t) < .2 for t in emph):
            sfx.append((s, "pop", .6))

# ---------- cámara ----------
ev = [(t, "punch") for t in pj.get("punches", [])] + [(t, "emph") for t in emph] + [(t, "reset") for t in resets]
if card:
    ev.append((card["start"], "card"))
ev.sort()
cam, s = [f'tl.fromTo("#cam", {{scale:1}}, {{scale:{1 + CAM["drift"] * 2:.3f}, duration:{(ev[0][0] if ev else VID):.2f}, ease:"none"}}, 0);'], 1 + CAM["drift"] * 2
for j, (t, kind) in enumerate(ev):
    nxt = ev[j + 1][0] if j + 1 < len(ev) else VID
    if kind == "punch":
        s = CAM["punch"]; cam.append(f'tl.to("#cam", {{scale:{s}, x:0, duration:.18, ease:"power3.out"}}, {t});'); t0 = t + .18
        sfx.append((t, "tick", .5))
    elif kind == "emph":
        s = min(s + CAM["emphasis"], CAM["max"]); cam.append(f'tl.to("#cam", {{scale:{s:.3f}, x:0, duration:.8, ease:"power2.out"}}, {t});'); t0 = t + .8
        sfx.append((t, "shimmer", .6))
    elif kind == "reset":
        s = 1.0; cam.append(f'tl.set("#cam", {{scale:1, x:0}}, {t});'); t0 = t
    else:  # card: alejar para que la tarjeta respire y panear suave
        cam.append(f'tl.to("#cam", {{scale:1.02, x:0, duration:1.2, ease:"power2.inOut"}}, {t});')
        cam.append(f'tl.to("#cam", {{scale:1.05, x:-18, duration:{max(nxt - t - 1.2, .1):.2f}, ease:"sine.inOut"}}, {t + 1.2});')
        s = 1.05; continue
    end = min(s + CAM["drift"], CAM["max"])
    if nxt - t0 > .1:
        cam.append(f'tl.to("#cam", {{scale:{end:.3f}, duration:{nxt - t0:.2f}, ease:"none"}}, {t0:.2f});'); s = end
pz = pj.get("product_zoom")
if pz:
    body_origin = pz.get("origin", "78% 86%")
    cam.append(f'tl.to("#cam2", {{scale:{CAM["product_zoom"]}, duration:1.5, ease:"power2.inOut"}}, {pz["start"]});')
    cam.append(f'tl.to("#cam2", {{scale:1, duration:1.8, ease:"power2.inOut"}}, {pz["end"] - 1.8});')
else:
    body_origin = "50% 50%"

# ---------- cierre ----------
ec = pj.get("end_card")
if ec:
    body.append(f'<img id="endbg" class="clip" src="assets/endbg.jpg" data-start="{VID}" data-duration="{round(DUR - VID, 2)}" />')
    clip("end", "end", VID, DUR, f'<div id="e1" class="k1">{H.escape(ec.get("kicker", ""))}</div>'
         f'<div id="e2" class="k2">{H.escape(ec["title"])}</div>'
         f'<div id="e3" class="brand"><b>{H.escape(ec["brand"])}</b><small>{H.escape(ec.get("sub", ""))}</small></div>')
    js += [f'tl.from("#endbg", {{opacity:0, duration:.35}}, {VID});',
           f'tl.from("#e1", {{opacity:0, y:20, duration:.35, ease:"power3.out"}}, {VID + .15});',
           f'tl.from("#e2", {{opacity:0, scale:.85, filter:"blur(10px)", duration:.5, ease:"power3.out"}}, {VID + .3});',
           f'tl.from("#e3", {{opacity:0, y:60, duration:.5, ease:"back.out(1.8)"}}, {VID + .6});']
    sfx += [(VID - .17, "whoosh", .7), (VID + .33, "shimmer", .5)]

css = f"""
:root {{ --gold:{C['gold']}; --gold-deep:{C['gold_deep']}; --cream:{C['cream']}; --ink:{C['ink']};
  --navy:{C['navy']}; --sticker:{C['sticker']}; --display:{F['display']}; --sans:{F['sans']};
  --dstyle:{F.get('display_style', 'italic')}; --dweight:{F.get('display_weight', '700')};
  --kw-stroke:{C.get('kw_stroke', 'rgba(60,40,10,.45)')}; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:var(--sans); }}
#cam {{ position:absolute; inset:0; transform-origin:50% 45%; will-change:transform; }}
#cam2 {{ position:absolute; inset:0; transform-origin:{body_origin}; will-change:transform; }}
#base {{ position:absolute; inset:0; width:1080px; height:1920px; object-fit:cover; }}
#vignette {{ position:absolute; inset:0; pointer-events:none;
  background: radial-gradient(ellipse 85% 70% at 50% 42%, transparent 55%, rgba(20,12,4,.38) 100%),
              linear-gradient(to bottom, transparent 58%, rgba(0,0,0,.30) 100%); }}
.cap {{ position:absolute; left:60px; right:60px; bottom:330px; text-align:center; font-weight:800; font-size:68px;
  line-height:1.08; color:#fff; letter-spacing:-.5px; text-shadow:0 4px 14px rgba(0,0,0,.65), 0 0 30px rgba(0,0,0,.35); }}
.cap.left {{ right:400px; text-align:left; }}
.cap .ln {{ display:inline-block; }}
.kw {{ font-family:var(--display); font-style:var(--dstyle); font-weight:var(--dweight); color:var(--gold); font-size:1.12em;
  -webkit-text-stroke:2px var(--kw-stroke); paint-order:stroke fill; }}
.kw.big {{ display:block; font-size:2.1em; line-height:.95; }}
.title {{ position:absolute; left:0; right:0; top:{S + 5}px; text-align:center; color:#fff; text-shadow:0 4px 18px rgba(0,0,0,.55); }}
.title .l1 {{ font-family:var(--display); font-style:var(--dstyle); font-weight:var(--dweight); font-size:94px; line-height:1; }}
.title .l1 .kw {{ font-size:1em; -webkit-text-stroke:0; }}
.title .l2 {{ margin-top:14px; font-weight:700; font-size:30px; letter-spacing:13px; }}
.sticker {{ position:absolute; left:92px; top:{S + 182}px; transform:rotate(-3deg); background:var(--sticker); color:var(--ink);
  font-weight:800; font-size:50px; padding:10px 26px 12px; border-radius:14px; box-shadow:0 10px 26px rgba(0,0,0,.35); }}
.chap {{ position:absolute; left:0; right:0; top:{S + 15}px; text-align:center; color:#fff; text-shadow:0 4px 18px rgba(0,0,0,.55); white-space:nowrap; }}
.chap .a {{ font-weight:700; font-size:56px; vertical-align:10px; margin-right:14px; }}
.chap .b {{ font-family:var(--display); font-style:var(--dstyle); font-weight:var(--dweight); font-size:116px; color:var(--gold); }}
.spark {{ position:absolute; color:#FFF1C9; font-size:40px; text-shadow:0 0 14px rgba(255,220,140,.9); }}
.card {{ position:absolute; left:60px; right:60px; top:{S - 12}px; background:var(--cream); border-radius:34px;
  padding:22px 34px 26px; color:var(--ink); box-shadow:0 16px 44px rgba(0,0,0,.38); }}
.card .hd {{ display:flex; justify-content:space-between; align-items:baseline; border-bottom:2px solid #E8DABD; padding-bottom:12px; margin-bottom:16px; }}
.card .hd b {{ font-family:var(--display); font-style:var(--dstyle); font-weight:var(--dweight); font-size:52px; }}
.card .hd b .kw {{ color:var(--gold-deep); font-size:1em; -webkit-text-stroke:0; }}
.card .hd em {{ font-style:normal; font-weight:700; font-size:20px; letter-spacing:5px; color:#B08B44; }}
.card .cols {{ display:grid; gap:24px; text-align:center; }}
.card .n {{ font-family:var(--display); font-weight:var(--dweight); font-size:46px; color:var(--navy); line-height:1; }}
.card .nm {{ font-weight:800; font-size:30px; line-height:1.12; margin-top:6px; }}
.card .sub {{ display:inline-block; margin-top:8px; font-size:24px; font-weight:600; color:#6B6252; padding:2px 10px; border-radius:8px; }}
.pst {{ position:absolute; font-weight:800; font-size:44px; padding:8px 22px 10px;
  border-radius:14px; white-space:nowrap; box-shadow:0 8px 20px rgba(0,0,0,.35); }}
.pill {{ position:absolute; background:var(--cream); color:var(--ink); font-weight:800; font-size:36px; padding:14px 28px;
  border-radius:60px; box-shadow:0 10px 26px rgba(0,0,0,.35); }}
.pill .kw {{ color:#9A7120; font-size:1em; -webkit-text-stroke:0; }}
.arrow {{ position:absolute; width:6px; height:62px; background:var(--gold); border-radius:3px; transform-origin:top center; }}
.arrow::after {{ content:""; position:absolute; left:-13px; bottom:-6px; border:16px solid transparent; border-top:22px solid var(--gold); border-bottom:0; }}
.flash {{ position:absolute; inset:-200px; pointer-events:none;
  background:linear-gradient(115deg, transparent 0 35%, {C['flash_a']} 42% 58%, {C['flash_b']} 60%, transparent 68%); }}
#endbg {{ position:absolute; inset:0; width:1080px; height:1920px; object-fit:cover; }}
.end {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:38px;
  text-align:center; color:#fff; padding:0 90px; }}
.end .k1 {{ font-weight:700; font-size:44px; letter-spacing:4px; }}
.end .k2 {{ font-family:var(--display); font-style:var(--dstyle); font-weight:var(--dweight); font-size:120px; line-height:1; color:var(--gold); text-shadow:0 6px 24px rgba(0,0,0,.45); }}
.end .brand {{ background:var(--cream); color:var(--ink); border-radius:36px; padding:34px 64px 30px; box-shadow:0 18px 50px rgba(0,0,0,.4); }}
.end .brand b {{ display:block; font-family:var(--display); font-weight:var(--dweight); font-size:72px; letter-spacing:6px; }}
.end .brand small {{ display:block; margin-top:8px; font-weight:600; font-size:30px; letter-spacing:8px; color:#8A6A2A; }}
"""

doc = f"""<!doctype html>
<html lang="es" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<link rel="stylesheet" href="fonts/local.css" />
<script src="gsap.min.js"></script>
<style>{css}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
<div id="cam"><div id="cam2"><video id="base" class="clip" src="assets/base.mp4" muted data-start="0" data-duration="{VID}"></video></div></div>
<div id="vignette"></div>
{chr(10).join(body)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(cam)}
{chr(10).join(js)}
window.__timelines["main"] = tl;
tl.seek(0);
</script>
</body>
</html>
"""
open(f"{P}/index.html", "w", encoding="utf-8").write(doc)
sfx.sort()
json.dump({"duration": DUR, "music_volume": st["music"]["volume"], "sfx": [[round(t, 2), n, v] for t, n, v in sfx]},
          open(f"{P}/sfx.json", "w"))
print(f"index.html ({len(caps)} subtítulos, {len(sfx)} efectos, {DUR}s)")
