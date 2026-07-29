# tessello — project roadmap

## Prime outcome
A from-scratch 2D Delaunay mesh generator, targeting OpenFOAM's native
`polyMesh` format, validated against the Schäfer-Turek cylinder-in-channel
benchmark. Built to learn computational geometry from first principles,
not to compete with existing tools.

## The 6 phases
1. **Unconstrained 2D Delaunay triangulation** — done: predicates,
   Bowyer-Watson, basic plotting. *(Days 1-8 below)*
2. **Constrained Delaunay** — force the triangulation to respect a real
   domain boundary (channel walls, cylinder surface). *(Days 9-14 below)*
3. **Quality refinement** (Ruppert's algorithm) — eliminate slivers,
   guarantee solver-usable mesh quality. *Not yet broken into days.*
4. **Boundary layer insertion** — CFD-specific near-wall mesh structure.
   *Not yet broken into days.*
5. **OpenFOAM `polyMesh` writer** — translate internal mesh representation
   to OpenFOAM's file format. *Not yet broken into days.*
6. **Validation** — Schäfer-Turek benchmark, checked against prior
   hand-built Gmsh/OpenFOAM results. *Not yet broken into days.*

Phases 3-6 are real, known destinations — but scoping them into single-day
tasks now, before Phase 2 is even finished, would mean guessing rather
than planning. Each phase gets broken into days only once the phase
before it is actually done — same reasoning that kept this roadmap at
Day 14 rather than inventing detail further out.

---

# Daily session roadmap

Rule for every session: **one outcome, then stop.** If you finish early, commit
and walk away rather than pulling in the next day's item — momentum across
days matters more than depth in one sitting. If a session runs long without
resolving, commit whatever's working (even if incomplete) and pick it up
fresh tomorrow rather than pushing through tired.

Each day is scoped for 30-45 minutes. Some will finish in 15. That's fine.

---

## Day 1 — Test bowyer_watson on a tiny case ✅ DONE
**Outcome:** run `bowyer_watson()` on 4-5 hand-picked points, print the
resulting triangle count, confirm it doesn't crash.
**Result:** 5-point square + center case, 4 triangles — matches the
`2n-h-2` formula (n=5, h=4) exactly. Confirmed correct, not just non-crashing.

## Day 2 — Debug Day 1's crash (if any) / verify triangle count makes sense ✅ DONE
**Outcome:** sanity-checked via the formula above — no crash, no bug found.

## Day 3 — Write `io/plot.py` ✅ DONE
**Outcome:** built as `viz/plot.py` (renamed from the original `io/`
sketch). Ran it on the 5-point square test case — visualized successfully.

## Day 4 — Visual sanity pass
**Outcome:** run `bowyer_watson()` + plot on 10-15 random points. Look for
obviously broken output — overlapping triangles, gaps, one giant sliver
spanning everything (usually means a scaffold-corner leaked into `final`).
**Stop when:** you've either confirmed it looks like a real triangulation,
or logged what looks wrong in `docs/notes.md`.

## Day 5 — Fix whatever Day 4 found, OR stress-test with more points
**Outcome:** if Day 4 found a bug, fix it. If it looked clean, push to
30-50 random points and re-check visually.
**Stop when:** one fix is made, or one larger test is run and recorded.

## Day 6 — Commit, update README status, write a notes.md entry
**Outcome:** no new code today. Update the README's status section to
reflect that basic unconstrained Delaunay is working. Write a short
`docs/notes.md` entry in your own words: what Bowyer-Watson does and why
the empty-circumcircle rule makes it work — a self-check, no references.
**Stop when:** the entry's written, even if imperfect. This is retrieval
practice, not documentation for others.

## Day 7 — Rest / buffer day
No coding goal. If you're ahead of schedule, do nothing new — reread your
own code instead, or just don't open the repo. If you're behind, use this
day to catch up on whichever earlier day didn't finish.

---

## After Day 7: milestone reached
At this point you have a working, visualized, tested, documented
unconstrained 2D Delaunay triangulator. That's the real "milestone one"
from the very start of this project.

---

## Day 8 — Reread everything, no new code
**Outcome:** read `primitives.py`, `predicates.py`, `delaunay.py` top to
bottom in one sitting. Try to explain each function out loud (or in
notes.md) without opening chat for help.
**Stop when:** you've been through all three files once.

## Day 9 — Define the constraint problem on paper
**Outcome:** no code. Sketch (on paper or in notes.md) what "constrained"
means for your actual target case — the Schäfer-Turek channel: which
edges (channel walls, cylinder boundary) must appear in the final
triangulation even if plain Delaunay wouldn't naturally produce them.
**Stop when:** you can state, in one paragraph, what a "constrained edge"
is and why plain Bowyer-Watson doesn't guarantee it.

## Day 10 — Segment intersection test
**Outcome:** write and test one function: given two line segments, does
the current triangulation have any edge crossing a constrained edge.
**Stop when:** the test function works on 2-3 hand-built cases.

## Day 11 — Read about edge-flipping for constraint enforcement
**Outcome:** no code. This is a "go check the reference" day — read the
constrained Delaunay section of the de Berg textbook (or Shewchuk's
notes), specifically the edge-flip approach for forcing an edge into the
triangulation.
**Stop when:** you can describe the flip approach in your own words in
notes.md, even roughly.

## Day 12 — Implement one edge flip
**Outcome:** given one offending edge, perform one flip, confirm the mesh
stays valid (still Delaunay elsewhere, still watertight).
**Stop when:** one flip works on one hand-built test case.

## Day 13 — Loop the flip over all constrained edges
**Outcome:** wire Day 12's single flip into a loop that walks all
constraint edges for your test geometry.
**Stop when:** it runs without crashing on a small test case, even if not
fully correct yet.

## Day 14 — Test against a real simple boundary
**Outcome:** define a simple closed boundary (a rectangle, or a rectangle
with a small hole for a "cylinder") as a list of constraint edges, run
full constrained triangulation, plot it.
**Stop when:** you get a plotted result, correct or not — this is a real
integration test, expect it to be messy the first time.

---

## Beyond Day 14: intentionally left open
This is as far as this roadmap goes with real, individually-scoped days.
Quality refinement, boundary layers, and the polyMesh writer aren't broken
into single-day tasks yet — not because they're being skipped, but because
scoping them accurately right now, before constrained Delaunay is even
working, would mean guessing rather than planning. Once Day 14 is done and
you've spent a Day-8-style reread/consolidation pass, extend this file
with the next phase then, using the same one-outcome-per-day format.

Don't let an unplanned future phase create pressure — "the roadmap doesn't
go further yet" is a true, fine state for a project at this stage, not a
gap to anxiously fill in advance.

---

## Guardrails, not just goals
- If a session's outcome is done in 10 minutes, **stop anyway.** Don't
  reach into tomorrow's scope. Understanding settles between sessions,
  not just during them.
- If you're stuck past 45 minutes on a single bug, commit a comment in the
  code describing where you're stuck and stop. Fresh eyes tomorrow are
  worth more than one more hour tonight.
- GATE prep and this project are not in competition on any given day —
  but across a week, if tessello is consistently eating into GATE study
  time, shrink tessello's days, not the reverse.
