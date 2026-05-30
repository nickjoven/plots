#!/usr/bin/env python3
"""Build the static site under docs/ from the repository sources.

Inputs:
  README.md          -> docs/grammar.html
  MAP.md             -> docs/map.html
  plots/*.txt        -> docs/<name>.html   (one page per plot, in a <pre>)
Generated:
  docs/index.html    the ordered list of plots, grouped by layer
  docs/style.css     graph-paper styling
  docs/.nojekyll     serve files as-is, no Jekyll

No third-party dependencies. The pages use relative links so the site can be
opened straight from disk (file://docs/index.html) with no server.
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PLOTS = ROOT / "plots"

# Map of plot-number ranges to the layer headings from MAP.md. Used only to
# group the index; the plot files themselves carry their own titles.
LAYERS = [
    (1, 1, "I. Ground"),
    (2, 4, "II. The generative acts"),
    (5, 8, "III. The moves that preserve the grid"),
    (9, 11, "IV. The structure the moves build"),
    (12, 20, "V. The arrivals"),
]


def page(title, body, css="style.css"):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{css}">
</head>
<body>
<main>
<p class="back"><a href="index.html">&larr; index</a></p>
{body}
</main>
</body>
</html>
"""


# --- minimal markdown -> html (only the constructs used in README/MAP) ---

def inline(text):
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def md_to_html(md):
    lines = md.splitlines()
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        # heading
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            i += 1
            continue
        # table: a run of lines that start with '|'
        if stripped.startswith("|"):
            tbl = []
            while i < n and lines[i].strip().startswith("|"):
                tbl.append(lines[i].strip())
                i += 1
            cells = [
                [c.strip() for c in row.strip("|").split("|")]
                for row in tbl
            ]
            header = cells[0]
            rows = cells[2:]  # skip the |---| separator row
            out.append("<table>")
            out.append("<thead><tr>" + "".join(
                f"<th>{inline(c)}</th>" for c in header) + "</tr></thead>")
            out.append("<tbody>")
            for r in rows:
                out.append("<tr>" + "".join(
                    f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            out.append("</tbody></table>")
            continue
        # unordered list
        if stripped.startswith("- "):
            items = []
            while i < n and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            out.append("<ul>" + "".join(
                f"<li>{inline(it)}</li>" for it in items) + "</ul>")
            continue
        # paragraph: gather until blank line
        para = []
        while i < n and lines[i].strip() and not lines[i].strip().startswith(
                ("#", "|", "- ")):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "\n".join(out)


def plot_number(name):
    m = re.match(r"^(\d+)", name)
    return int(m.group(1)) if m else 999


def build():
    DOCS.mkdir(exist_ok=True)
    (DOCS / ".nojekyll").write_text("")
    (DOCS / "style.css").write_text(CSS)

    # plot pages
    plots = sorted(PLOTS.glob("*.txt"), key=lambda p: plot_number(p.stem))
    entries = []
    for p in plots:
        text = p.read_text()
        title = text.splitlines()[0].strip() if text.strip() else p.stem
        body = (f"<h1>{html.escape(title)}</h1>\n"
                f"<pre class=\"plot\">{html.escape(text)}</pre>")
        out_name = f"{p.stem}.html"
        (DOCS / out_name).write_text(page(title, body))
        entries.append((plot_number(p.stem), p.stem, title, out_name))

    # grammar + map
    (DOCS / "grammar.html").write_text(
        page("plots — grammar", md_to_html((ROOT / "README.md").read_text())))
    (DOCS / "map.html").write_text(
        page("plots — map", md_to_html((ROOT / "MAP.md").read_text())))

    # index
    body = ["<h1>plots</h1>",
            "<p>A drawing language for the harmonics framework. Each plot is a "
            "coordinate-grid figure meant to be redrawn by hand. The order is "
            "ontological: nothing is drawn before the parts it is built from.</p>",
            '<p class="links"><a href="grammar.html">grammar</a> &middot; '
            '<a href="map.html">map and order</a></p>']
    for lo, hi, label in LAYERS:
        group = [e for e in entries if lo <= e[0] <= hi]
        body.append(f"<h2>{html.escape(label)}</h2>")
        if not group:
            body.append('<p class="planned">(not yet drawn &mdash; see the '
                        '<a href="map.html">map</a>)</p>')
            continue
        body.append("<ul class=\"index\">")
        for num, stem, title, out_name in group:
            body.append(
                f'<li><span class="num">{num:02d}</span> '
                f'<a href="{out_name}">{html.escape(title)}</a></li>')
        body.append("</ul>")
    index = page("plots", "\n".join(body))
    # the index has no back-link
    index = index.replace(
        '<p class="back"><a href="index.html">&larr; index</a></p>\n', "")
    (DOCS / "index.html").write_text(index)

    print(f"built {len(entries)} plot pages + index, grammar, map into {DOCS}")


CSS = """\
:root {
  --ink: #1a1a1a;
  --line: #cfe0ee;
  --line2: #e7eff6;
  --accent: #2b5d86;
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  color: var(--ink);
  font: 15px/1.6 ui-monospace, "SFMono-Regular", Menlo, Consolas, monospace;
  background-color: #fbfdff;
  background-image:
    linear-gradient(var(--line2) 1px, transparent 1px),
    linear-gradient(90deg, var(--line2) 1px, transparent 1px);
  background-size: 24px 24px;
}
main {
  max-width: 820px;
  margin: 0 auto;
  padding: 32px 20px 80px;
}
h1 { font-size: 22px; margin: 0 0 16px; }
h2 { font-size: 17px; margin: 28px 0 8px; border-bottom: 1px solid var(--line); padding-bottom: 4px; }
h3 { font-size: 15px; margin: 20px 0 6px; }
h4 { font-size: 15px; margin: 16px 0 6px; }
p { margin: 10px 0; }
a { color: var(--accent); }
.back { font-size: 13px; margin-bottom: 20px; }
.links { font-size: 14px; }
.planned { color: #8a99a8; }
ul.index { list-style: none; padding: 0; }
ul.index li { margin: 4px 0; }
ul.index .num { color: #8a99a8; margin-right: 8px; }
pre.plot {
  background: #ffffff;
  border: 1px solid var(--line);
  border-radius: 4px;
  padding: 18px 20px;
  overflow-x: auto;
  line-height: 1.35;
  font-size: 13px;
}
table { border-collapse: collapse; margin: 12px 0; font-size: 13px; }
th, td { border: 1px solid var(--line); padding: 4px 10px; text-align: left; vertical-align: top; }
th { background: #f1f7fc; }
code { background: #f1f7fc; padding: 1px 4px; border-radius: 3px; }
"""


if __name__ == "__main__":
    build()
