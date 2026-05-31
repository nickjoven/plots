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
    # the action: the cell leans as T is applied, from square through the two
    # frames and back. The pinned base stays; the top edge slides right.
    frames = [[(0, 0), (1, 0), (1 + i, 1), (i, 1)] for i in (0, 1, 2)]
    p = Paper(-0.3, 3.6, -0.3, 2.3)
    p.grid().dots(0, 3, 0, 2)
    p.ghost([(0, 0), (1, 0), (1, 1), (0, 1)])        # where it started
    p.anim_poly(frames, dur=4.0, cls="cell")
    p.vector(0, 0, 1, 0)                              # e1 pinned
    p.anim_dot([(0, 1), (1, 1), (2, 1)], dur=4.0, cls="tip")
    p.label(0.5, 0, "pinned", dx=0, dy=15, cls="label")
    figs = [("the cell leans as the shear is applied; base pinned, top slides "
             "right (loops)", p.svg())]
    # vector view: the tip walks right along y=1
    p = Paper(-0.3, 3.6, -0.3, 1.8)
    p.grid().dots(0, 3, 0, 1)
    p.vector(0, 0, 1, 0)
    p.anim_dot([(0, 1), (1, 1), (2, 1), (3, 1)], dur=4.0, cls="tip")
    figs.append(("vector view: the tracked tip walks right at constant height",
                 p.svg()))
    return figs


# --- 06 rotate ------------------------------------------------------------
def rotate():
    p = Paper(-1.7, 1.7, -1.7, 1.7)
    p.grid().dots(-1, 1, -1, 1)
    for (x, y) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:   # the compass marks
        p.dot(x, y, "mark")
    p.anim_spin(1, 0, dur=4.0)                          # the turning vector
    return [("the vector turns through the four compass points and returns "
             "(loops)", p.svg())]


# --- 04 mediant -----------------------------------------------------------
def mediant():
    p = Paper(-0.3, 3.3, -0.3, 2.3)
    p.grid().dots(0, 3, 0, 2)
    p.poly([(0, 0), (1, 0), (2, 1), (1, 1)], "cell2")   # the area-1 cell
    p.vector(0, 0, 1, 0)                                 # v1 = 0/1, fixed
    p.ghost([(0, 0), (1, 1)])                            # v2 at its start
    # v2 slides tip-to-tail onto v1: tail 0->(1,0), head (1,1)->(2,1)
    p.anim_vector([(0, 0, 1, 1), (1, 0, 2, 1)], dur=4.0, cls="vec")
    p.mark(2, 1, "tip")
    p.label(1, 0, "0/1", dx=4, dy=16, cls="label b")
    p.label(1, 1, "1/1", dx=6, dy=-7, cls="label")
    p.label(2, 1, "1/2 = (2,1)", dx=6, dy=-7, cls="label r")
    return [("the second vector slides tip-to-tail onto the first; the sum is "
             "the mediant 1/2 (loops)", p.svg())]


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
    p.polyline(pts, "ghost")                  # the track, faint
    p.mark(2, 2, "mark")
    p.anim_dot(pts, dur=5.0, cls="tip")       # the dot steps up the track
    p.label(2, 2, "(2,2) fixed point", dx=7, dy=-7, cls="label r")
    p.label(3.0, f(3.0), "y = 1 + x/2", dx=-4, dy=-7, cls="label b", anchor="end")
    p.label(2.4, 2.4, "y = x", dx=6, dy=10, cls="label")
    return [("a dot steps up the cobweb toward the crossing (2,2), then back "
             "(loops)", p.svg())]


RENDERERS = {
    "02-fixed-point": cobweb,
    "04-mediant": mediant,
    "05-shear": shear,
    "06-rotate": rotate,
}


# --- the book: one page per degree of freedom ------------------------------
def _edges(p, pts, cls="edge"):
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        p.seg(a[0], a[1], b[0], b[1], cls)


def dof_pages():
    """One graph-paper page per degree of freedom (the dimension ladder).

    Every page uses the same paper size so paging does not jump. The figure on
    page N is the figure on page N-1 swept along one new direction; the 4th
    cannot lie flat and is shown projected.
    """
    pages = []

    def paper():
        return Paper(-0.5, 5.0, -0.5, 5.0, cell=30).grid()

    # 0 — a point
    p = paper()
    p.mark(2, 2, "tip")
    p.label(2, 2, "a point", dx=9, dy=-8)
    pages.append(("0 degrees of freedom — a point", p.svg()))

    # 1 — a line
    p = paper()
    p.seg(1, 2, 4, 2, "edge")
    p.mark(1, 2, "tip")
    p.mark(4, 2, "tip")
    p.label(2.5, 2, "a line", dx=0, dy=-11)
    pages.append(("1 degree of freedom — a line", p.svg()))

    # 2 — a plane
    p = paper()
    p.poly([(1, 1), (4, 1), (4, 4), (1, 4)], "cell")
    p.label(2.5, 1, "a plane", dx=0, dy=20)
    pages.append(("2 degrees of freedom — a plane", p.svg()))

    # 3 — a volume (cube, oblique)
    p = paper()
    off = (0.95, 0.72)
    front = [(1, 1), (3.2, 1), (3.2, 3.2), (1, 3.2)]
    back = [(c[0] + off[0], c[1] + off[1]) for c in front]
    _edges(p, front)
    _edges(p, back)
    for a, b in zip(front, back):
        p.seg(a[0], a[1], b[0], b[1])
    p.label(1, 3.2, "a volume", dx=2, dy=-26)
    pages.append(("3 degrees of freedom — a volume", p.svg()))

    # 4 — a projection (tesseract, oblique)
    p = paper()
    off, woff = (0.8, 0.6), (-0.7, 1.05)
    front = [(0.9, 0.6), (2.6, 0.6), (2.6, 2.3), (0.9, 2.3)]
    back = [(c[0] + off[0], c[1] + off[1]) for c in front]
    cubeA = front + back
    cubeB = [(c[0] + woff[0], c[1] + woff[1]) for c in cubeA]
    _edges(p, front)
    _edges(p, back)
    for a, b in zip(front, back):
        p.seg(a[0], a[1], b[0], b[1])
    _edges(p, cubeB[:4], "diag")
    _edges(p, cubeB[4:], "diag")
    for a, b in zip(cubeB[:4], cubeB[4:]):
        p.seg(a[0], a[1], b[0], b[1], "diag")
    for a, b in zip(cubeA, cubeB):
        p.seg(a[0], a[1], b[0], b[1], "diag")
    p.label(0.0, 4.4, "a projection — the 4th cannot lie flat", dx=0, dy=0)
    pages.append(("4 degrees of freedom — a projection onto the page", p.svg()))

    return pages
