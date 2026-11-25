"""Genera los HTML de los juegos a partir de plantilla.html y juegos.py."""
import json, pathlib, sys
AQUI = pathlib.Path(__file__).parent
sys.path.insert(0, str(AQUI))
from juegos import JUEGOS

plantilla = (AQUI / "plantilla.html").read_text(encoding="utf-8")
for j in JUEGOS:
    cfg = {k: j[k] for k in ("rounds", "vis", "intro", "finale", "stepLabel", "q", "doneStep", "doneText")}
    html = plantilla
    for k, v in {"__TITLE__": j["title"], "__HL__": j["hl"], "__EYEBROW__": j["eyebrow"], "__H1__": j["h1"],
                 "__LEAD__": j["lead"], "__UNIT__": j["unit"], "__FOOTER__": j["footer"]}.items():
        html = html.replace(k, v)
    html = html.replace("__CONFIG__", json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/"))
    out = AQUI.parent / f"{j['slug']}.html"
    out.write_text(html, encoding="utf-8")
    print(out.name)
