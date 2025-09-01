from manim import *
from instant_insanity.core.config import LINEN_CONFIG

def cubic_edge(u_pt: np.ndarray, v_pt: np.ndarray,
               min_len: float = 1.0,
               loop_scale: float = 0.6) -> CubicBezier:
    """
    Single cubic Bézier that morphs from a straight segment to a loop.
    - For d >= min_len: looks straight (control points along the chord).
    - For d <  min_len: endpoints collapse toward the midpoint; control points
      add a perpendicular and a 'closing' component so that when the endpoints
      coincide the start/end tangents are perpendicular.
    loop_scale controls the loop radius at coincidence (≈ loop_scale * min_len/2).
    """
    a = np.array(u_pt, dtype=float)
    b = np.array(v_pt, dtype=float)
    dvec = b - a
    d = float(np.linalg.norm(dvec))

    # Unit chord direction (fallback if coincident)
    if d > 1e-9:
        u = dvec / d
    else:
        u = np.array([1.0, 0.0, 0.0])
    n = np.array([-u[1], u[0], 0.0])  # +90° in xy-plane
    m = 0.5 * (a + b)

    # Blend parameter: 1 → straight; 0 → loop
    t = min(1.0, d / min_len)

    # Endpoints:
    # - For large d, they are the true endpoints a,b.
    # - For small d, they collapse to the midpoint (distance shrinks ~ t).
    if d >= min_len:
        e1, e2 = a, b
        half = 0.5 * d
    else:
        half = 0.5 * (min_len * t)     # goes to 0 as dots coincide
        e1 = m - half * u
        e2 = m + half * u

    # Along-chord component for a straight-looking cubic
    along = (2.0 * half / 3.0) * t     # equals d/3 when t=1

    # Perpendicular/loop component grows as endpoints meet
    loop_r = (min_len * 0.5) * loop_scale * (1.0 - t)

    # Control points:
    # c1 adds perpendicular; c2 adds a component along +u so that
    # at coincidence (t=0): P0=P3=m, P1 = m + loop_r*n, P2 = m + loop_r*u,
    # giving perpendicular start/end tangents (n ⟂ u).
    c1 = e1 + along * u + loop_r * n
    c2 = e2 - along * u + loop_r * u

    return CubicBezier(e1, c1, c2, e2, stroke_color=BLACK, stroke_width=2)


class LineToLoop(Scene):
    def construct(self):
        # Positions
        p1 = LEFT * 4 + DOWN * 1
        p2 = LEFT * 1 + UP * 2
        p3 = RIGHT * 2 + DOWN * 2
        p4 = RIGHT * 4 + UP * 1

        # Graph with vertices only (we'll draw the edge ourselves)
        g = Graph(
            vertices=[1, 2, 3, 4],
            edges=[],  # no edges; the cubic below is our dynamic edge
            layout={1: p1, 2: p2, 3: p3, 4: p4},
            vertex_type=Dot,
            vertex_config={'radius': 0.18, 'stroke_color': BLACK},
        )
        g[1].set_fill(RED, 1)
        g[2].set_fill(BLUE, 1)
        g[3].set_fill(GREEN, 1)
        g[4].set_fill(YELLOW, 1)

        min_len = 1.0      # your requested minimum visible length for the edge
        bend_max = 1.2     # how “round” the loop gets at coincidence

        # Always redraw the cubic from current vertex positions
        edge = always_redraw(lambda: cubic_edge(g[1].get_center(),
                                                g[2].get_center(),
                                                min_len=min_len))

        # Add edge first (back), graph second (front) for Cairo Painter's Algorithm
        self.add(edge, g)
        self.wait(0.3)

        # Animate: move vertex 1 → p3 and 2 → p3 in parallel (edge morphs into a loop)
        self.play(
            g[1].animate.move_to(p3),
            g[2].animate.move_to(p3),
            run_time=2.0,
        )
        self.wait(0.6)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = LineToLoop()
        scene.render()
