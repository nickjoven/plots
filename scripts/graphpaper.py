#!/usr/bin/env python3
"""Virtual graph paper: a tiny SVG builder for coordinate-grid figures.

No dependencies. A Paper holds a coordinate window in grid units and draws the
graph-paper background (minor lines every unit, major every five, axes, origin)
plus primitives: dots, marked points, arrowed vectors, polygons, open
polylines, sampled curves, and text. Call .svg() for the finished SVG string.

Screen mapping: x grows right, y grows up (SVG y is flipped here so the figures
read like paper). One grid unit is `cell` pixels.
"""

import math


def _n(v):
    # compact number formatting for SVG
    return f"{v:.2f}".rstrip("0").rstrip(".")


class Paper:
    def __init__(self, xmin, xmax, ymin, ymax, cell=34, pad=0.7):
        self.xmin, self.xmax = xmin, xmax
        self.ymin, self.ymax = ymin, ymax
        self.cell = cell
        self.pad = pad
        self.w = (xmax - xmin + 2 * pad) * cell
        self.h = (ymax - ymin + 2 * pad) * cell
        self.body = []

    # coordinate -> pixel
    def sx(self, x):
        return (x - self.xmin + self.pad) * self.cell

    def sy(self, y):
        return (self.ymax - y + self.pad) * self.cell

    # --- background ---------------------------------------------------------
    def grid(self):
        e = []
        x0 = math.floor(self.xmin)
        x1 = math.ceil(self.xmax)
        y0 = math.floor(self.ymin)
        y1 = math.ceil(self.ymax)
        for x in range(x0, x1 + 1):
            major = (x % 5 == 0)
            e.append(
                f'<line x1="{_n(self.sx(x))}" y1="{_n(self.sy(y1))}" '
                f'x2="{_n(self.sx(x))}" y2="{_n(self.sy(y0))}" '
                f'class="{"maj" if major else "min"}"/>')
        for y in range(y0, y1 + 1):
            major = (y % 5 == 0)
            e.append(
                f'<line x1="{_n(self.sx(x0))}" y1="{_n(self.sy(y))}" '
                f'x2="{_n(self.sx(x1))}" y2="{_n(self.sy(y))}" '
                f'class="{"maj" if major else "min"}"/>')
        # axes if zero is in range
        if y0 <= 0 <= y1:
            e.append(
                f'<line x1="{_n(self.sx(x0))}" y1="{_n(self.sy(0))}" '
                f'x2="{_n(self.sx(x1))}" y2="{_n(self.sy(0))}" class="axis"/>')
        if x0 <= 0 <= x1:
            e.append(
                f'<line x1="{_n(self.sx(0))}" y1="{_n(self.sy(y1))}" '
                f'x2="{_n(self.sx(0))}" y2="{_n(self.sy(y0))}" class="axis"/>')
        if x0 <= 0 <= x1 and y0 <= 0 <= y1:
            e.append(f'<circle cx="{_n(self.sx(0))}" cy="{_n(self.sy(0))}" '
                     f'r="2.6" class="origin"/>')
        self.body = e + self.body
        return self

    # --- primitives ---------------------------------------------------------
    def dot(self, x, y, cls="dot"):
        self.body.append(
            f'<circle cx="{_n(self.sx(x))}" cy="{_n(self.sy(y))}" r="2" '
            f'class="{cls}"/>')
        return self

    def dots(self, x0, x1, y0, y1):
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                self.dot(x, y, "latt")
        return self

    def mark(self, x, y, cls="mark"):
        self.body.append(
            f'<circle cx="{_n(self.sx(x))}" cy="{_n(self.sy(y))}" r="3.4" '
            f'class="{cls}"/>')
        return self

    def vector(self, x0, y0, x1, y1, cls="vec"):
        self.body.append(
            f'<line x1="{_n(self.sx(x0))}" y1="{_n(self.sy(y0))}" '
            f'x2="{_n(self.sx(x1))}" y2="{_n(self.sy(y1))}" '
            f'class="{cls}" marker-end="url(#arrow)"/>')
        return self

    def seg(self, x0, y0, x1, y1, cls="edge"):
        self.body.append(
            f'<line x1="{_n(self.sx(x0))}" y1="{_n(self.sy(y0))}" '
            f'x2="{_n(self.sx(x1))}" y2="{_n(self.sy(y1))}" class="{cls}"/>')
        return self

    def poly(self, pts, cls="cell"):
        s = " ".join(f"{_n(self.sx(x))},{_n(self.sy(y))}" for x, y in pts)
        self.body.append(f'<polygon points="{s}" class="{cls}"/>')
        return self

    def polyline(self, pts, cls="path"):
        s = " ".join(f"{_n(self.sx(x))},{_n(self.sy(y))}" for x, y in pts)
        self.body.append(f'<polyline points="{s}" class="{cls}"/>')
        return self

    def curve(self, f, x0, x1, cls="curve", samples=60):
        pts = []
        for i in range(samples + 1):
            x = x0 + (x1 - x0) * i / samples
            pts.append((x, f(x)))
        self.polyline(pts, cls)
        return self

    def label(self, x, y, text, dx=6, dy=-6, cls="label", anchor="start"):
        self.body.append(
            f'<text x="{_n(self.sx(x) + dx)}" y="{_n(self.sy(y) + dy)}" '
            f'text-anchor="{anchor}" class="{cls}">{text}</text>')
        return self

    # --- output -------------------------------------------------------------
    def svg(self):
        defs = (
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0,0 L10,5 L0,10 z" class="arrowhead"/></marker></defs>')
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {_n(self.w)} {_n(self.h)}" '
            f'width="{_n(self.w)}" height="{_n(self.h)}" class="gp">'
            f'{defs}<style>{STYLE}</style>'
            f'{"".join(self.body)}</svg>')


STYLE = """
.gp { background:#ffffff; font-family:ui-monospace,Menlo,Consolas,monospace; }
.min { stroke:#dcebf6; stroke-width:1; }
.maj { stroke:#bcd6ec; stroke-width:1; }
.axis { stroke:#7f97ad; stroke-width:1.4; }
.origin { fill:#7f97ad; }
.latt { fill:#c2d2e0; }
.dot { fill:#33424f; }
.mark { fill:#2b5d86; }
.tip { fill:#c0392b; }
.vec { stroke:#2b5d86; stroke-width:2; fill:none; }
.vec2 { stroke:#c0392b; stroke-width:2; stroke-dasharray:4 3; fill:none; }
.edge { stroke:#33424f; stroke-width:1.6; }
.cell { fill:rgba(43,93,134,0.12); stroke:#2b5d86; stroke-width:1.6; }
.cell2 { fill:rgba(192,57,43,0.10); stroke:#c0392b; stroke-width:1.4; }
.path { stroke:#c0392b; stroke-width:1.8; fill:none; }
.curve { stroke:#2b5d86; stroke-width:1.8; fill:none; }
.diag { stroke:#7f97ad; stroke-width:1.4; fill:none; stroke-dasharray:5 3; }
.arrowhead { fill:#2b5d86; }
.label { fill:#33424f; font-size:11px; }
.label.r { fill:#c0392b; }
.label.b { fill:#2b5d86; }
"""
