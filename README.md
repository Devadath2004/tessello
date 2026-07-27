# tessello

A from-scratch 2D Delaunay mesh generator, built as a serious side project to
learn computational geometry from first principles and contribute something
usable to the open-source CFD ecosystem.

## Why this exists

Plenty of mature mesh generators already exist (Gmsh, CGAL, Triangle, and
others). This project isn't trying to compete with them. The goal is to
build a real, working Delaunay triangulator entirely from scratch — deriving
the geometry, not just implementing known formulas — and eventually target
OpenFOAM's native `polyMesh` format so the output is immediately usable in a
real CFD solver.

## Status

Early and actively developed. Currently implemented:

- `geometry/primitives.py` — `Point` and `Triangle` data structures
- `geometry/predicates.py` — `orientation()` and `in_circumcircle()`,
  the two core geometric predicates Delaunay triangulation is built on
- `triangulate/delaunay.py` — in progress:
  - `super_triangle()` — builds an enclosing triangle to seed the algorithm
  - `find_bad_triangles()` — finds triangles whose circumcircle is violated
    by a new point
  - `find_boundary_edges()` — traces the boundary of the resulting cavity
  - `make_triangle()` — constructs a triangle with guaranteed
    counter-clockwise winding

Not yet implemented: the main Bowyer-Watson insertion loop, and everything
past basic unconstrained 2D triangulation.

## License

MIT — see `LICENSE`.
