#!/usr/bin/env python3
"""Graph-paper renderers for the plots.

Each renderer returns a list of (caption, svg_string) figures. The build embeds
them on the plot page. RENDERERS maps a plot file stem to its renderer; stems
not present fall back to the ASCII text panel. Renderers are pure functions of
the (already verified) geometry, so regeneration is deterministic.
"""

from graphpaper import Paper


# --- 05 shear -------------------------------------------------------------
def shear():
    figs = []
    for i in range(3):
        p = Paper(-0.3, 3.6, -0.3, 2.3)
        p.grid().dots(0, 3, 0, 2)
        corners = [(0, 0), (1, 0), (1 + i, 1), (i, 1)]
        p.poly(corners, "cell")
        p.vector(0, 0, 1, 0)              # e1 pinned
        p.vector(0, 0, i, 1) if i else p.vector(0, 0, 0, 1)
        p.mark(i, 1, "tip")
        p.label(i, 1, f"({i},1)", dx=5, dy=-6, cls="label r")
        label = "frame 0 (I)" if i == 0 else (
            "frame 1 (T)" if i == 1 else "frame 2 (T applied twice)")
        figs.append((label, p.svg()))
    # vector view
    p = Paper(-0.3, 3.6, -0.3, 1.8)
    p.grid().dots(0, 3, 0, 1)
    for x in range(4):
        p.mark(x, 1, "tip")
    p.polyline([(0, 1), (3, 1)], "path")
    p.vector(0, 0, 1, 0)
    p.label(0, 1, "(0,1)", dx=4, dy=-7, cls="label r")
    p.label(3, 1, "(3,1)", dx=4, dy=-7, cls="label r")
    figs.append(("vector view: the tip walks right along y=1", p.svg()))
    return figs


# --- 06 rotate ------------------------------------------------------------
def rotate():
    p = Paper(-1.7, 1.7, -1.7, 1.7)
    p.grid().dots(-1, 1, -1, 1)
    pos = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for k, (x, y) in enumerate(pos):
        p.vector(0, 0, x, y)
        p.mark(x, y, "tip")
        p.label(x, y, str(k if k else 0) if False else f"{k+1}",
                dx=7 if x >= 0 else -14, dy=-7, cls="label b")
    p.label(1, 0, "start (1,0)", dx=6, dy=14, cls="label")
    return [("e1 swung to the four compass points; the 4th returns to the 1st",
             p.svg())]


# --- 04 mediant -----------------------------------------------------------
def mediant():
    p = Paper(-0.3, 3.3, -0.3, 2.3)
    p.grid().dots(0, 3, 0, 2)
    # parallelogram spanned by (1,0) and (1,1)
    p.poly([(0, 0), (1, 0), (2, 1), (1, 1)], "cell2")
    p.vector(0, 0, 1, 0)                 # 0/1
    p.vector(0, 0, 1, 1)                 # 1/1
    p.seg(0, 0, 2, 1, "vec2")            # sum direction
    p.mark(2, 1, "tip")
    p.label(1, 0, "0/1 = (1,0)", dx=4, dy=16, cls="label b")
    p.label(1, 1, "1/1 = (1,1)", dx=6, dy=-7, cls="label b")
    p.label(2, 1, "1/2 = (2,1)", dx=6, dy=-7, cls="label r")
    return [("0/1 + 1/1 = 1/2 ; the spanned cell has area 1, none inside",
             p.svg())]


# --- 02 fixed point (cobweb) ----------------------------------------------
def cobweb():
    f = lambda x: 1 + x / 2
    p = Paper(-0.2, 3.2, -0.2, 2.5)
    p.grid()
    p.curve(lambda x: x, 0, 2.5, "diag")     # y = x
    p.curve(f, -0.2, 3.2, "curve")           # y = 1 + x/2
    # staircase corners
    pts = [(0.0, 0.0)]
    x = 0.0
    for _ in range(6):
        y = f(x)
        pts.append((x, y))
        pts.append((y, y))
        x = y
    p.polyline(pts, "path")
    p.mark(2, 2, "tip")
    p.label(2, 2, "(2,2) fixed point", dx=7, dy=-7, cls="label r")
    p.label(3.0, f(3.0), "y = 1 + x/2", dx=-4, dy=-7, cls="label b", anchor="end")
    p.label(2.4, 2.4, "y = x", dx=6, dy=10, cls="label")
    return [("the cobweb staircase climbing to the crossing (2,2)", p.svg())]


RENDERERS = {
    "02-fixed-point": cobweb,
    "04-mediant": mediant,
    "05-shear": shear,
    "06-rotate": rotate,
}
