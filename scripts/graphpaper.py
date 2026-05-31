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

    # --- animation (SMIL; runs when the SVG is inlined in the page) ----------
    def _pointstr(self, pts):
        return " ".join(f"{_n(self.sx(x))},{_n(self.sy(y))}" for x, y in pts)

    def ghost(self, pts, cls="ghost"):
        # a faint static shape, e.g. the starting state left behind
        self.body.append(f'<polygon points="{self._pointstr(pts)}" class="{cls}"/>')
        return self

    def anim_poly(self, frames, dur=4.0, cls="cell"):
        # morph a polygon through the frames and back (yo-yo loop). Every frame
        # must have the same number of points.
        seq = list(frames) + list(frames[-2::-1])
        vals = ";".join(self._pointstr(fr) for fr in seq)
        self.body.append(
            f'<polygon points="{self._pointstr(frames[0])}" class="{cls}">'
            f'<animate attributeName="points" dur="{dur}s" values="{vals}" '
            f'repeatCount="indefinite" calcMode="linear"/></polygon>')
        return self

    def anim_dot(self, positions, dur=4.0, cls="tip", r=3.4, yoyo=True):
        seq = list(positions) + (list(positions[-2::-1]) if yoyo else [])
        cxs = ";".join(_n(self.sx(x)) for x, _ in seq)
        cys = ";".join(_n(self.sy(y)) for _, y in seq)
        x0, y0 = positions[0]
        self.body.append(
            f'<circle cx="{_n(self.sx(x0))}" cy="{_n(self.sy(y0))}" r="{r}" '
            f'class="{cls}">'
            f'<animate attributeName="cx" dur="{dur}s" values="{cxs}" '
            f'repeatCount="indefinite"/>'
            f'<animate attributeName="cy" dur="{dur}s" values="{cys}" '
            f'repeatCount="indefinite"/></circle>')
        return self

    def anim_spin(self, x, y, dur=4.0, cls="vec", direction=360):
        # a vector from the origin to (x,y), with a tip, spun about the origin.
        ox, oy = self.sx(0), self.sy(0)
        tx, ty = self.sx(x), self.sy(y)
        self.body.append(
            f'<g><line x1="{_n(ox)}" y1="{_n(oy)}" x2="{_n(tx)}" y2="{_n(ty)}" '
            f'class="{cls}" marker-end="url(#arrow)"/>'
            f'<circle cx="{_n(tx)}" cy="{_n(ty)}" r="3.4" class="tip"/>'
            f'<animateTransform attributeName="transform" type="rotate" '
            f'from="0 {_n(ox)} {_n(oy)}" to="{direction} {_n(ox)} {_n(oy)}" '
            f'dur="{dur}s" repeatCount="indefinite"/></g>')
        return self

    def anim_vector(self, frames, dur=4.0, cls="vec"):
        # an arrowed line whose endpoint moves through frames (list of (x,y)),
        # tail fixed at frames are (x0,y0,x1,y1) tuples
        seq = list(frames) + list(frames[-2::-1])
        x1s = ";".join(_n(self.sx(f[2])) for f in seq)
        y1s = ";".join(_n(self.sy(f[3])) for f in seq)
        f0 = frames[0]
        self.body.append(
            f'<line x1="{_n(self.sx(f0[0]))}" y1="{_n(self.sy(f0[1]))}" '
            f'x2="{_n(self.sx(f0[2]))}" y2="{_n(self.sy(f0[3]))}" class="{cls}" '
            f'marker-end="url(#arrow)">'
            f'<animate attributeName="x2" dur="{dur}s" values="{x1s}" '
            f'repeatCount="indefinite"/>'
            f'<animate attributeName="y2" dur="{dur}s" values="{y1s}" '
            f'repeatCount="indefinite"/></line>')
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
.gp .min { stroke:#dcebf6; stroke-width:1; }
.gp .maj { stroke:#bcd6ec; stroke-width:1; }
.gp .axis { stroke:#7f97ad; stroke-width:1.4; }
.gp .origin { fill:#7f97ad; }
.gp .latt { fill:#c2d2e0; }
.gp .dot { fill:#33424f; }
.gp .mark { fill:#2b5d86; }
.gp .tip { fill:#c0392b; }
.gp .vec { stroke:#2b5d86; stroke-width:2; fill:none; }
.gp .vec2 { stroke:#c0392b; stroke-width:2; stroke-dasharray:4 3; fill:none; }
.gp .edge { stroke:#33424f; stroke-width:1.6; }
.gp .cell { fill:rgba(43,93,134,0.12); stroke:#2b5d86; stroke-width:1.6; }
.gp .cell2 { fill:rgba(192,57,43,0.10); stroke:#c0392b; stroke-width:1.4; }
.gp .ghost { fill:none; stroke:#9fb3c6; stroke-width:1.2; stroke-dasharray:4 3; }
.gp .path { stroke:#c0392b; stroke-width:1.8; fill:none; }
.gp .curve { stroke:#2b5d86; stroke-width:1.8; fill:none; }
.gp .diag { stroke:#7f97ad; stroke-width:1.4; fill:none; stroke-dasharray:5 3; }
.gp .arrowhead { fill:#2b5d86; }
.gp .label { fill:#33424f; font-size:11px; }
.gp .label.r { fill:#c0392b; }
.gp .label.b { fill:#2b5d86; }
"""
