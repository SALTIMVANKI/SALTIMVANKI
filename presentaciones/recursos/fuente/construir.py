"""Genera los 3 recursos (premios de la feria) a partir de comun.html y cada fuente."""
import pathlib
AQUI = pathlib.Path(__file__).parent
comun = (AQUI / "comun.html").read_text(encoding="utf-8")
RECURSOS = [("guia-cerebro", "Dale cerebro a tu IA"), ("ganchos", "30 ganchos que paran el scroll"), ("ideas", "50 ideas de contenido")]
for slug, title in RECURSOS:
    src = (AQUI / f"{slug}.html").read_text(encoding="utf-8")
    i = src.index("<script>")
    html = comun.replace("__TITLE__", title).replace("__BODY__", src[:i]).replace("__SCRIPT__", src[i:])
    (AQUI.parent / f"{slug}.html").write_text(html, encoding="utf-8")
    print(slug)
