# tessello — progress log

Consolidated from the working session(s) so far. No real calendar dates
attached — split this into actual days as you like, or just use it as a
running record and add dated entries below it from here on.

---

## Setup phase
- Decided scope: from-scratch 2D Delaunay mesh generator for CFD, targeting
  OpenFOAM's polyMesh format eventually.
- Chose to build from scratch rather than wrap an existing mesher.
- Set up local repo, `.gitignore`, git basics.
- Named the project **tessello**, after checking `ezmesh` and `dmesh` were
  both already taken by existing tools.
- Chose **MIT license** (weighed against GPL — MIT for lower-friction
  adoption and easier future relicensing).
- Resolved a real git snag: local commits and GitHub's auto-generated
  LICENSE had diverged histories — merged with
  `--allow-unrelated-histories`, fixed `master`/`main` branch mismatch, set
  up SSH auth.

## Core data structures
- Built `geometry/primitives.py`: `Point` and `Triangle` as `@dataclass`es.
  Triangle stores point *indices*, not embedded coordinates.
- Learned along the way: classes, dataclasses, type hints, `__init__.py`
  and package structure, tuple unpacking.

## Geometric predicates (`geometry/predicates.py`)
- Built `orientation(a, b, c)` — 2D cross product, tells you CCW/CW/collinear.
- Built `in_circumcircle(a, b, c, d)` — the empty-circumcircle Delaunay test.
- Did a full first-principles derivation, not just implementation:
  - Why Delaunay triangulations minimize sliver triangles (angle-maximizing
    property).
  - The paraboloid-lifting trick: lifting 2D points onto z=x²+y², proving
    algebraically that a circle's lifted points are always coplanar.
  - Why "inside the circle" corresponds to "below that plane."
  - Cross product → scalar triple product → determinant, and why they're
    the same computation under different notation.
  - Derived the cross product formula itself from the perpendicularity
    requirement, then from cofactor-expanding the formal `[î ĵ k̂; v; w]`
    matrix.
  - Worked out that the determinant's sign convention is fixed by input
    order (not universal), verified with a hand-computed example (det=2
    for a known-inside point).
  - Settled the "does the paraboloid move" question — mathematically
    equivalent either way; "one fixed paraboloid, points get shifted" and
    "paraboloid re-centered at d each time" are the same computation from
    two reference frames.
  - Connected `orientation` and `in_circumcircle`'s relationship:
    orientation enforces winding at construction time; in_circumcircle
    trusts that invariant at query time.
- Both predicates written, hand-tested, committed.

## Bowyer-Watson pipeline (`triangulate/delaunay.py`)
- `super_triangle(points)` — builds an enclosing triangle from a bounding
  box + margin. Found and fixed a real bug (p2 using max_y instead of
  min_y — typo in the source).
- `find_bad_triangles(triangles, points, new_point)` — filters triangles
  via `in_circumcircle`.
- `find_boundary_edges(bad_triangles)` — canonical-edge counting to find
  the cavity's outer rim (count==1 → boundary, count==2 → interior,
  discarded). Found and fixed a real indentation bug (return was inside
  the outer loop, causing early exit after the first triangle).
- `make_triangle(i1, i2, i3, points)` — orientation-enforcing constructor
  wrapper, guarantees CCW winding regardless of input order.
- `bowyer_watson(input_points)` — the main loop, tying all of the above
  together: seed with super-triangle, insert points one at a time
  (find bad → remove → find boundary → fan new triangles), strip
  scaffold-touching triangles at the end.
- Written, not yet tested end-to-end.

## Process / meta
- Wrote README.md (trimmed — status only, no speculative roadmap).
- Set up a daily session roadmap (30-45 min/day, one outcome per session,
  explicit permission to stop early) to prevent overworking.
- Discussed how to reference the de Berg et al. *Computational Geometry*
  textbook — as a post-hoc check, not a starting point; noted it's dense
  and best used for targeted lookup rather than linear reading.

---

## Not yet done
- `bowyer_watson()` has not been run/tested at all yet.
- No plotting (`io/plot.py`) exists yet.
- No constrained Delaunay, refinement, boundary layers, or polyMesh writer.

---

## Add new entries below, dated, as you go:

### [date]
-
