"""SUJET.md -> SUJET.pdf, charte Code Runners.

Usage : uv run --with markdown sujet/build_pdf.py [sujet/SUJET.md]
Requiert Google Chrome (impression headless) et Internet pour les polices Google Fonts.
"""
import html
import re
import subprocess
import sys
from pathlib import Path

import markdown

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"  # ponytail: macOS only, add a lookup if someone builds on Linux


def parse(src: str) -> tuple[dict, str]:
    meta_block, body = src.split("---", 2)[1:]
    meta = dict(line.split(":", 1) for line in meta_block.strip().splitlines())
    return {k.strip(): v.strip() for k, v in meta.items()}, body


def code_line(text: str) -> str:
    """Colore une ligne de code d'accroche : mots-clés en menthe, fonctions en jaune."""
    out = html.escape(text)
    out = re.sub(r"\b(if|while|for|else)\b", r'<span class="k">\1</span>', out)
    return re.sub(r"\b(\w+)(?=\()", r'<span class="fn">\1</span>', out)


def body_html(md: str) -> str:
    out = markdown.markdown(md, extensions=["tables"])
    # Markdown fusionne les blockquotes consécutives : on recoupe à chaque ℹ️.
    out = re.sub(r"</p>\s*<p>ℹ️\s*", '</p>\n</blockquote>\n<blockquote>\n<p>ℹ️ ', out)
    out = re.sub(r"<blockquote>\s*<p>ℹ️\s*", '<blockquote class="info">\n<p>', out)
    # Une <section> par titre h2, numérotée pour l'eyebrow « // 01 ».
    parts = re.split(r"(?=<h2>)", out)
    n = 0
    sections = []
    for part in parts:
        if part.startswith("<h2>"):
            n += 1
            part = part.replace("<h2>", f'<h2 data-n="{n:02d}">', 1)
        sections.append(f"<section>{part}</section>")
    return "\n".join(sections)


def render(meta: dict, md: str) -> str:
    d = meta["defi"].zfill(2)
    slug = meta["titre"].lower()
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<link rel="stylesheet" href="style.css">
<style>@page {{ @bottom-right {{ content: "défi_{d} · {slug} · {meta["version"]} · p. " counter(page); }} }}</style>
</head><body>
<div class="cover">
  <div class="prompt"><span class="u">alveoles@techsud</span>:<span class="p">~/code-runners/defi-{d}</span>$ cat SUJET.md</div>
  <div class="brand">Alvéoles <span class="x">×</span> Epitech</div>
  <div class="title"><span class="code">CODE</span><span class="run">RUN</span><span class="ners">NERS</span></div>
  <div class="bar"><span class="h"></span><span class="f"></span></div>
  <div class="badge">// DÉFI {d}</div>
  <div class="defi">{html.escape(meta["titre"])}</div>
  <div class="soustitre">{html.escape(meta["sous_titre"])}</div>
  <div class="accroche">{code_line(meta["accroche"])}<span class="cursor"></span></div>
  <div class="spacer"></div>
  <div class="date"><span class="j">MERCREDI</span><span class="d">02.12</span><span class="y">2026</span></div>
  <div class="lieu">lieu = {{ <span class="k">site</span>: <span class="v">"Technopole · Parc Techsud"</span>, <span class="k">ville</span>: <span class="v">"Saint-Pierre"</span> }}</div>
  <div class="soutien"><span>Avec le soutien de</span><span><b>CCCA BTP</b> · <b>WinLab'</b></span></div>
</div>
{body_html(md)}
<div class="version">{meta["version"]}</div>
</body></html>"""


def main() -> None:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).with_name("SUJET.md")).resolve()
    meta, md = parse(src.read_text(encoding="utf-8"))
    page = src.with_suffix(".html")
    page.write_text(render(meta, md), encoding="utf-8")
    pdf = src.with_suffix(".pdf")
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=10000", f"--print-to-pdf={pdf}", page.as_uri()],
                   check=True, capture_output=True)
    page.unlink()
    assert pdf.stat().st_size > 10_000, "PDF vide : Chrome n'a rien imprimé"
    print(pdf)


if __name__ == "__main__":
    main()
