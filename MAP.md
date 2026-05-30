# Map of the manifest, and the order in which to draw it

This file is the index for the repository. It lists every object in the `nickjoven/harmonics` `MANIFEST.yml` that can be drawn on a coordinate grid as stepwise motion, and it fixes the order in which those objects will be drawn. It also names the objects that have no honest grid drawing and records why each one is left out. The drawing language itself is defined in `README.md`, and the first drawing, the shear, is in `plots/shear.txt`.

## The ordering principle

The order is ontological, which here means that it follows dependency. An object is drawn only after every object it is built from has already been drawn. A reader who follows the sequence in order therefore never meets a thing before meeting its parts. The integer grid comes first because every later drawing is made of it. The moves that send the grid to itself come before the structures those moves build, and the structures come before the measured values that sit at the end of them. The measured values from the scorecard are drawn last because each one is an arrival that rests on everything above it.

The sequence is grouped into six layers. Layers are numbered with Roman numerals and individual drawings are numbered in a single running sequence so that each drawing has a stable name. A drawing marked DONE already exists in the repository.

## I. Ground

**01 — The integer grid (Z).** Source: `primitives.list`, "Integers Z (counting)". This is the lattice itself, drawn first as a number line and then as the plane of points whose two coordinates are both whole numbers. Counting is the act of stepping from one point to the next by a fixed unit, so the grid carries stepwise motion in its construction. Every later drawing is made of these points. This is the ground that the rest of the repository stands on.

## II. The generative acts

These three primitives are the first things the integers do. Each one rests only on the grid from layer I.

**02 — Fixed point, x = f(x).** Source: `primitives.list`, "Fixed-point x = f(x) (self-reference)". A fixed point is a place where a function returns its own input unchanged. It is drawn as a cobweb: the diagonal line y = x and the curve y = f(x) are plotted, a starting value is chosen, and the path steps vertically to the curve and then horizontally back to the diagonal, over and over. The path is a staircase that walks in toward the crossing point, and that crossing point is the arrival. This is the cleanest stepwise drawing in the whole set because it is already a staircase by definition.

**03 — Parabola, x² + μ = 0.** Source: `primitives.list`, "Parabola x² + μ = 0 (bifurcation)". This is the curve y = x² + μ drawn for several values of μ. When μ is positive the curve clears the x-axis and has no root, when μ is zero it touches the axis at one point, and when μ is negative it crosses the axis at the two points plus and minus the square root of minus μ. Stepping μ downward past zero is the bifurcation: one solution splits into two. The motion here is the motion of μ, and the arrival is the pair of roots opening apart.

**04 — Mediant, (a+c)/(b+d).** Source: `primitives.list`, "Mediant ... derived from energy conservation + stability (D29)". The mediant combines two fractions a/b and c/d into the single fraction (a+c)/(b+d) that lies between them. It is drawn on the lattice by treating each fraction as a vector, (b,a) and (d,c), and adding the two vectors tip to tail; the sum vector points at the mediant. The step is the single act of addition, and the arrival is the new vector landing between the two it came from. This is the primitive that turns the integers into every fraction used later.

## III. The moves that preserve the grid

These are the elements of the modular group SL(2,Z), the integer matrices of determinant 1. Each one sends the lattice exactly onto itself and keeps every area unchanged. They rest on the grid from layer I, and the group as a whole organizes the mediant from item 04.

**05 — Shear, the lean, T = [[1,1],[0,1]]. DONE.** Source: this language; the shear appears throughout `harmonics` as the unipotent factor (`planck_scale.md`, `speed_of_light.md`, `isotropy_lemma.md`). It slides each point to the right by its height and pins the x-axis, tipping the grid over while keeping area at 1. The drawing exists in `plots/shear.txt`.

**06 — Rotate, the turn, S = [[0,-1],[1,0]].** Source: this language; S is the second generator of the modular group. It spins the whole grid a quarter turn about the origin, sending (x,y) to (-y,x). Applied four times it returns to the start, so it is drawn as a four-frame cycle, and applied twice it gives the point reflection through the origin. The turn and the lean together are enough to build every move in the group.

**07 — The group SL(2,Z) = ⟨T,S⟩.** Source: `primitives` and the framework's use of the modular group. This drawing takes the basis vectors e1 and e2 and shows a few words spelled out of shears and turns carrying that basis to other bases, every one of which still spans a cell of area exactly 1. The whole view here makes the central fact visible: the set of lattice points never changes, and only the chosen frame moves. This is the home that items 05 and 06 live inside.

**08 — Iwasawa factoring, k·a·n.** Source: the Iwasawa decomposition used across `harmonics` (`planck_scale.md`, `lie_group_characterization.md`, `speed_of_light.md`). Any move can be written as a turn k, then a stretch a along the axes, then a lean n, applied in that order. The drawing applies the three factors to the unit cell one at a time, so the reader sees a single move taken apart into turn, stretch, and lean. The stretch factor a is the squeeze that returns later as the Lorentz boost in item 20, which is why this factoring is drawn before the arrivals.

## IV. The structure the moves build

These objects are what the mediant and the group produce together. They rest on items 04 and 07.

**09 — Farey sequence and the Stern-Brocot tree, |F_6| = 13.** Source: `klein_bottle.farey_count: 13`. The Farey sequence is built on the interval from 0 to 1 by repeatedly inserting the mediant of each pair of neighbours, and the number of fractions at level six is thirteen. Each insertion is one step, so the construction is a process whose count is the arrival. The neighbouring fractions at every stage satisfy the relation bc − ad = 1, which means the vectors they stand for span a lattice parallelogram of area 1 with no point inside it; this is the same determinant-1 fact from the group in item 07, now seen as the reason the mediant is the simplest fraction between two others.

**10 — The Klein-bottle integers.** Source: `klein_bottle` (q2 = 2, q3 = 3, product = 6, farey_count = 13, total_budget = 19, exponent = 54, double_exponent = 108). These are the specific integers the framework selects, and each is drawn as a count or an area on the grid. The product 6 is a two-by-three rectangle, the Farey count 13 is the result carried over from item 09, the budget 19 is shown as the rectangle of 6 set beside the count of 13, the exponent 54 is the block 2 times 3 cubed, and the double exponent 108 is two of those. The whole drawing collects the integers that every scorecard value is later assembled from.

**11 — The cubes and the duty cycle.** Source: `bare_k1_identities` and `klein_bottle`. In dimension three the two integers become cubes: q2 cubed is 8, drawn as a two-by-two-by-two block, and q3 cubed is 27, drawn as a three-by-three-by-three block, and their sum is 35. The bare reference values are then drawn as comparisons of these volumes: 8/35 for sin²θ_W, 27/8 for the ratio of strong to weak coupling, 35 for the inverse electromagnetic coupling at tree level, 1/2 for the Higgs-to-vacuum ratio, and 1/8 for the Higgs quartic. The manifest records these as substrate-side values rather than predictions at the Z scale, and the drawings show them as exact volume ratios with that status noted.

## V. The arrivals

These are the scorecard values, each drawn as a path that lands on the grid or as a partition that tiles it. Every one rests on the layers above.

**12 — Dark energy, Ω_Λ = 13/19.** Source: `scorecard.dark_energy` (13/19 = 0.6842). This is drawn as the Stern-Brocot path of left and right mediant steps that lands on 13/19, and also as the lattice vector (19,13) with the staircase that approximates its slope. The path is the process and the fraction is the arrival.

**13 — The cosmic budget that tiles the grid.** Source: `scorecard.dark_matter_fraction`, `baryon_fraction`, `dm_baryon_ratio`, `dark_energy_fraction_two_component`. On a bar of length 19 the single-component budget splits exactly as 1 for baryons, 5 for dark matter, and 13 for dark energy, and one plus five plus thirteen is nineteen. On the refined bar of length 264 the two-component split is 13 for baryons, 70 for dark matter, and 181 for dark energy, and thirteen plus seventy plus one hundred eighty-one is two hundred sixty-four. The ratio of dark matter to baryons is 70/13. The drawing is the two bars, each cut into pieces that fill it with nothing left over, which is the closure the framework calls Class 5.

**14 — Born rule, exponent 2.** Source: `scorecard.born_rule` (computed 2, source D1, D9). A length is drawn along the grid, and then the square built on that length is drawn as the area it encloses. Probability is the area, amplitude is the side, and the exponent that connects them is two. The step from a side to its square is the motion, and the exponent is the arrival.

**15 — Uncertainty, τ × Δθ = 1.** Source: `scorecard.uncertainty` (computed 1.000000, source D7, D9). The constraint that a product equals one is the hyperbola xy = 1 drawn on the grid. A point sliding along that curve trades a larger τ for a smaller Δθ while the rectangle under it always has area exactly one, which is the same area-1 fact that runs through the whole group. The motion is the slide along the curve, and the arrival is the fixed product.

**16 — Spatial dimension, 3.** Source: `scorecard.spatial_dimension` (computed 3, source D14). This is the dimension ladder drawn as a build: a point, then a line that is one dimension, then a square that is two, then a cube that is three. Each rung adds one independent direction to the grid, and the arrival is the third rung, the cube, which is also the dimension that makes the cubes in item 11.

**17 — The scale ladders, R = 6 × 13⁵⁴ and Λℓ_P² = 13⁻¹⁰⁸/12.** Source: `scorecard.hierarchy` and `scorecard.lambda_planck`. The hierarchy between the Planck and Hubble scales is reached by starting at 6 and multiplying by 13 fifty-four times, and the cosmological constant in Planck units is reached by dividing by 13 one hundred eight times and then by twelve. These are drawn as logarithmic ladders where every rung is one factor of 13, with the first rungs drawn in full and the rung count written out, since the full ladders are too long to draw to the end. The motion is the repeated scaling and the arrival is the value at the last rung.

**18 — The gauge group as root lattices, SU(3) × SU(2) × U(1).** Source: `scorecard.gauge_group` (source D41, D42). The factor SU(2), tied to q2, is drawn as the root system on a line with two roots, plus and minus one. The factor SU(3), tied to q3, is drawn as the root system on the triangular lattice with six roots arranged in a hexagon. The factor U(1) is a single axis. The arrival is the three root pictures set side by side, the gauge content of the standard model shown as lattices.

**19 — Anomaly cancellation as a closed walk.** Source: `scorecard.anomaly_cancellation` (all 6 conditions = 0, source D41). Each anomaly condition is a sum of charges that must come to zero. It is drawn by laying the charges end to tail as vectors along the grid and showing that the walk returns exactly to the origin. The motion is the walk and the arrival is the return to the start, which is the cancellation.

**20 — Lorentz symmetry as the boost squeeze, Spin(3,1).** Source: `scorecard.lorentz` (source D14, D15) and `speed_of_light.md`. On a grid of space against time the Lorentz boost is the squeeze that stretches one diagonal of the light cone and shrinks the other while leaving the cone lines themselves fixed. This squeeze is the stretch factor a from the Iwasawa factoring in item 08, now read as motion through spacetime, which is why the boost is drawn after that factoring. The motion is the squeeze and the invariant cone is the arrival.

## Not drawn

These manifest entries have no honest stepwise drawing on a coordinate grid, and they are left out for the reasons given.

**Spectral tilt, n_s = 0.963–0.966.** Source: `scorecard.spectral_tilt`. This is a continuous value close to one with no integer-path structure, so the only possible drawing is a mark showing its distance from one, which is not motion. It is left out.

**MOND scale, a₀ = 1.25 × 10⁻¹⁰ m/s².** Source: `scorecard.mond_scale`. This is a dimensionful physical constant produced by the numerical solver in the `rfe` repository, and it has no path on the lattice. It is left out.

**Number of e-folds, N = 61.3.** Source: `scorecard.efolds`. This is a predicted count awaiting measurement, and although it could be shown as a doubling ladder, it has no integer structure that the ladder would reveal, so the ladder would add nothing. It is left out for now.

**Strong CP angle, θ = 0.** Source: `scorecard.strong_cp`. This is an angle pinned at zero, which is drawable only as a fixed point that does not move; that content is already carried by the fixed-point drawing in item 02, so it is folded there rather than given its own drawing.

**Structural counts.** The manifest also records `derivation_count: 47`, `phases: 16`, and the proposition counts of proof chains A, B, and C (8, 11, 7). These count the framework's own parts rather than objects on the coordinate grid, so they are kept here as metadata and not drawn.
