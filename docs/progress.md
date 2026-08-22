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
- Written and tested against random points and structured points.

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

### [2026-08-02]
## Constrained-Delunay
- Looked into the concept of inserting boundaries. found resource for the whole pipeline - Lecture Notes on Delaunay Mesh Generation by Jonathan Richard Shewchuk. can be kept for reference.
- Explored several ways to force a required boundary edge (A-B) to survive triangulation when plain Bowyer-Watson doesn't naturally produce it.
- Initially assumed the "flip" mechanic (single quadrilateral, swap the diagonal) generalizes directly to the multi-crossing case. It doesn't — worked through a concrete counterexample: a chain of points near but never crossing the straight A-B line (A-C-D-E-F-G-H-B) has no crossing edge to even start flipping from. This matches Shewchuk's formal definition, which uses a visibility condition, not a straight-line-crossing test.
- Landed on a cleaner, self-consistent model instead: treat the region between the existing mesh and the required edge as a single cavity (same idea as Bowyer-Watson's point-insertion cavity), delete it, and retriangulate the whole thing at once with the required edge forced in. This handles both the simple crossing case and the no-crossing chain case with one unified procedure, since both are just "some cavity shape" — sometimes a simple quadrilateral, sometimes a longer sliver.
- Known limitation: this is correct but not work-minimal. Shewchuk's actual segment-insertion algorithm (see Lecture Notes on Delaunay Mesh Generation, 2012) does provably minimal work by only touching edges that actually cross the required edge's path. Worth reading properly and comparing once the cavity-based version is implemented and tested.
- Decision: build the cavity-based version first, behind a swappable interface (insert_constrained_edge(triangles, points, edge)), documented as non-optimal, so a Shewchuk-based replacement can drop in later without touching any calling code.
### [2026-08-09]
## Intersecting triangles
- worked through the algorithm for finding the intersecting triangles and wrote the function for finding it using the segmentsIntesect funciton created earlier
- worked through finding the algorithm used for re triangulation after forcing the edge
- Planning to go with ear clipping algorithm to split between the subpolygons after the cavity has been done
- Next steps after this session - 
- [] delete intersecting triangles from existing triangle list 
- [] find the boundary edge using find_boundary_edge function  
- [] split the boundary using the boundary edge
- [] use ear clipping to retrianglulate the sub polygons
- [] push back the new triangle list into the triangles list

### [2026-08-10]
- wrote a small line of code to remove intersecting triangles from triangles list. Now i need to test it. 
### [2026-08-11]
- Tested using claude. It works. i will cross veriy later. for now the first step is done
- Next steps after this session - 
- [x] delete intersecting triangles from existing triangle list 
- [] find the boundary edge using find_boundary_edge function  
- [] split the boundary using the boundary edge
- [] use ear clipping to retrianglulate the sub polygons
- [] push back the new triangle list into the triangles list
### [2026-08-21]
- Next steps after this session - 
- [x] delete intersecting triangles from existing triangle list 
- [x] find the boundary edge using find_boundary_edge function- step is redundant, just passing the intersectingTriangles to find_boundary_edges function might cut it.
- [] split the boundary using the boundary edge
- [] use ear clipping to retrianglulate the sub polygons
- [] push back the new triangle list into the triangles list
