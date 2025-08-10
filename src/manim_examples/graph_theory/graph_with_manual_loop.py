from manim import *
import numpy as np

from instant_insanity.core.config import LINEN_CONFIG


def attach_loop(scene: Scene, g: Graph, v, radius=0.30, angle=PI/4,
                color=BLACK, stroke_width=2) -> VMobject:
    """Attach a loop (circle) to vertex v that follows it during animations."""
    vert = g[v]
    loop = Circle(radius=radius, color=color, stroke_width=stroke_width)

    # Place slightly outside the vertex, at the given angle
    vr = getattr(vert, "radius", 0.15)  # works for Dot
    direction = np.array([np.cos(angle), np.sin(angle), 0.0])

    def _update(m: VMobject):
        m.move_to(vert.get_center() + (vr + radius) * direction)

    loop.add_updater(_update)
    _update(loop)               # position immediately
    return loop

class GraphWithManualLoop(Scene):
    def construct(self):
        # Positions
        p1 = LEFT * 4 + DOWN * 1
        p2 = LEFT * 1 + UP * 2
        p3 = RIGHT * 2 + DOWN * 2
        p4 = RIGHT * 4 + UP * 1

        # Graph with a single edge (1–2)
        g = Graph(
            vertices=[1, 2, 3, 4],
            edges=[(1, 2)],
            layout={1: p1, 2: p2, 3: p3, 4: p4},
            vertex_type=Dot,
            vertex_config={'radius': 0.18, 'stroke_color': BLACK},
            edge_config={'stroke_color': BLACK, 'stroke_width': 2},
        )

        # Colors for clarity
        g[1].set_fill(RED, 1)
        g[2].set_fill(BLUE, 1)
        g[3].set_fill(GREEN, 1)
        g[4].set_fill(YELLOW, 1)

        # Create loop first, then add in back-to-front order for Cairo
        loop = attach_loop(self, g, 3, radius=0.30, angle=PI/3, color=BLACK, stroke_width=2)
        self.add(loop, g)

        self.wait(0.3)

        # Animate: move vertex 1 → p3 and 2 → p3 (edge 1–2 collapses),
        # the loop at 3 stays visible and tracks vertex 3.
        self.play(
            g[1].animate.move_to(p3),
            g[2].animate.move_to(p3),
            run_time=1.8
        )
        self.wait(0.5)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphWithManualLoop()
        scene.render()
