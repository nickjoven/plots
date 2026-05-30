# plots

This repository is a drawing language for the harmonics framework. Its purpose is to take an object from the mathematics, such as a vector, a lattice, an element of the group SL(2,Z), or a mediant, and draw that object on a coordinate grid. The drawings are meant to be plain enough that a person with graph paper can reproduce them by hand and follow which part of the object moved and where it went.

The quantitative values used in these drawings are taken from the `MANIFEST.yml` file in the `nickjoven/harmonics` repository. This repository does not restate the derivations that produce those values. It draws the objects that the derivations are about.

## Grid

The drawing surface is the integer lattice, which is the set of points whose coordinates are both whole numbers. The two axes are drawn as reference lines, and the origin at coordinate (0,0) is marked with the letter `O`. An ordinary lattice point is drawn as a small dot `·`. A point that is being marked or tracked through a sequence is drawn as `*`. The tip of a vector under discussion is drawn as `o`.

Each coordinate is written in the form `(x,y)`. The picture itself is only an aid to reading, and the list of coordinates printed beneath each frame is the actual source of truth. When the ASCII drawing is too coarse to be exact, the coordinates should be used to redraw the figure accurately. One square of the grid stands for one unit of distance, and no scaling is applied unless a drawing says otherwise.

## Moves (the verbs)

Each move in this language is a two-by-two matrix of integers that acts on a column vector. The verb is the everyday word for what that matrix does to the grid, and it is the name this repository uses for the move. The determinant, written `det`, records how the move changes area: a determinant of 1 means area is preserved exactly.

| verb          | matrix              | action on (x,y) | det |
|---------------|---------------------|-----------------|-----|
| shear / lean  | [[1,1],[0,1]] = T   | (x+y, y)        | 1   |
| rotate / turn | [[0,-1],[1,0]] = S  | (-y, x)         | 1   |
| translate     | add a fixed vector  | (x+a, y+b)      | —   |
| mediant / merge | a/b combined with c/d | (a+c)/(b+d) | —   |

The shear, which this language also calls the lean, slides each point to the right by an amount equal to its height, while the points on the x-axis stay where they are. The result is that the grid tips over to one side, and because the determinant is 1 the area of every shape is left unchanged. The rotate, also called the turn, spins the whole grid a quarter turn around the origin, and it too preserves area. The translate moves every point by the same fixed amount without turning or leaning the grid. The mediant combines two fractions by adding the vectors that define them, and it produces the fraction that sits between them; this is the primitive introduced in derivation D29 of the harmonics framework.

The two moves T and S together generate the whole group SL(2,Z). Every move drawn in this repository is therefore either a sequence of shears and turns or a mediant.

## Views

The same object can be drawn from three points of view, and a given figure will say which one it is using.

The **whole** view shows the entire lattice or tessellation at once. Its purpose is to make clear that a move from SL(2,Z) sends the lattice onto itself, so that the set of points is unchanged and only the chosen cell or basis has moved.

The **coordinate** view shows a single row or column, which means one coordinate is held fixed while the other varies. Its purpose is to show how the move acts on one line of points in isolation.

The **vector** view shows a single tracked point together with the path it follows. Its purpose is to show the move as the motion of one tip across the grid.

## Motion

A drawing shows motion in one of two ways. A **process** is a sequence of frames in which one move is applied per frame, and reading the frames in order traces the path. An **arrival** is a single final state, such as a fixed point where x equals f(x) or a settled value such as a Farey fraction, and it is drawn as one frame with a note recording the path that reached it.

## Preview

The drawings are plain text and can be read directly from the `plots/` folder.
A rendered version is also built into the `docs/` folder as a small static site,
and the same site is published by GitHub Pages from that folder. To look at it
locally there are two equally simple options. Opening the file `docs/index.html`
in a browser works on its own, because the pages link to each other with
relative paths and need no server. Running `make preview` instead starts a local
server on port 8000 and serves the same folder, which is closer to how the
published site behaves. The site is regenerated from the source files by running
`make build`, which calls `scripts/build_site.py` and has no dependencies beyond
Python.

The published site is at https://nickjoven.github.io/plots/.

## Files

The file `MAP.md` is the index. It lists every object in the manifest that can be drawn as stepwise motion, fixes the order in which they are drawn, and records the objects that are left out and why. The order is ontological: an object is drawn only after the objects it is built from have been drawn.

The file `plots/shear.txt` draws the shear move T, shown first as a process and then as an arrival, and given in all three views. It is drawing 05 in the map. The drawings before it (the integer grid, the fixed point, the parabola, and the mediant) and after it (the rotate, the group, the Iwasawa factoring, and the arrivals) follow the order set in `MAP.md`.
