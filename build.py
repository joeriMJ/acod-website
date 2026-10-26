#!/usr/bin/env python3
"""Bouwt de site: voegt layout + pagina's samen, per thema.

Gebruik: python3 build.py
Pagina's staan in src/pages/*.html en zijn gedeeld door alle thema's. Een thema
(src/themes/<naam>/) heeft een layout.html en style.css, en kan pagina's
overschrijven in src/themes/<naam>/pages/.
De eerste regel van elke pagina is een commentaar met titel en beschrijving:
    <!-- title: Lid worden | desc: Waarom en hoe je lid wordt -->
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "site"

# Pas deze waarden aan. Alles tussen [vierkante haken] is nog aan te leveren.
SITE = {
    "name": "ACOD Telecom-Vliegwezen",
    "short": "ACOD",
    "sector": "Telecom-Vliegwezen",
    "street": "[straat en nummer]",
    "city": "[postcode gemeente]",
    "email": "info@voorbeeld.be",  # TODO: echt adres van het secretariaat
    "facebook": "",  # TODO: link naar Facebookpagina, leeg = verbergen
    # Zolang de site een ontwerp is, vragen we zoekmachines om ze niet op te nemen.
    # Leegmaken ("") bij de echte lancering.
    "robots": '<meta name="robots" content="noindex">',
}

NAV = [
    ("over-ons.html", "Over ons"),
    ("bedrijven.html", "Bedrijven"),
    ("nieuwsbrief.html", "Nieuwsbrief"),
    ("eisenbundel.html", "Eisenbundel"),
    ("hulp.html", "Hulp en tools"),
    ("faq.html", "Vragen"),
    ("contact.html", "Contact"),
]


def nav_html(current):
    items = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == current else ""
        items.append(f'<li><a href="{href}"{cur}>{label}</a></li>')
    return "\n          ".join(items)


def render(page_path, layout):
    raw = page_path.read_text(encoding="utf-8")
    m = re.match(r"<!--\s*title:\s*(.*?)\s*\|\s*desc:\s*(.*?)\s*-->\s*", raw)
    if not m:
        raise SystemExit(f"{page_path.name}: eerste regel mist title/desc")
    title, desc = m.group(1), m.group(2)
    body = raw[m.end():]
    full_title = SITE["name"] if page_path.name == "index.html" else f"{title} | {SITE['name']}"
    html = layout.replace("{{content}}", body)
    html = html.replace("{{title}}", full_title).replace("{{desc}}", desc)
    html = html.replace("{{nav}}", nav_html(page_path.name))
    html = html.replace("{{facebook}}", (
        f'<li><a href="{SITE["facebook"]}">Facebook</a></li>' if SITE["facebook"] else ""))
    for key, val in SITE.items():
        html = html.replace("{{" + key + "}}", val)
    leftover = re.findall(r"\{\{\w+\}\}", html)
    if leftover:
        raise SystemExit(f"{page_path.name}: onbekende placeholders {leftover}")
    return html


# thema -> uitvoermap
THEMES = {
    "v2": OUT,
    "v1": OUT / "v1",
}


def build_theme(theme, out):
    tdir = SRC / "themes" / theme
    layout = (tdir / "layout.html").read_text(encoding="utf-8")
    shutil.copytree(SRC / "assets", out / "assets")
    if (tdir / "assets").exists():  # thema-eigen bestanden overschrijven de gedeelde
        shutil.copytree(tdir / "assets", out / "assets", dirs_exist_ok=True)
    shutil.copy(tdir / "style.css", out / "assets" / "style.css")
    pages = {p.name: p for p in (SRC / "pages").glob("*.html")}
    pages.update({p.name: p for p in (tdir / "pages").glob("*.html")})
    for name in sorted(pages):
        (out / name).write_text(render(pages[name], layout), encoding="utf-8")
    print(f"gebouwd: {theme} ({len(pages)} pagina's) in {out.relative_to(ROOT)}/")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    for theme, out in THEMES.items():
        build_theme(theme, out)


if __name__ == "__main__":
    main()
