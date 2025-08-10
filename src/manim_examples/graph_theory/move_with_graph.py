from manim import *
from instant_insanity.core.config import LINEN_CONFIG

class MoveWithGraph(Scene):
    def construct(self):
        # Positions
        p1 = LEFT * 4 + DOWN * 1
        p2 = LEFT * 1 + UP * 2
        p3 = RIGHT * 2 + DOWN * 2
        p4 = RIGHT * 4 + UP * 1

        # Graph with 4 vertices and one edge (1–2)
        g = Graph(
            vertices=[1, 2, 3, 4],
            edges=[(1, 2)],
            layout={1: p1, 2: p2, 3: p3, 4: p4},
            vertex_type=Dot,
            vertex_config={
                'radius': 0.18,
                'stroke_color': BLACK,
            },
            labels=False,
            edge_config={'stroke_color': BLACK, 'stroke_width': 2},
        )

        # Per-vertex fill colors
        g.vertices[1].set_fill(RED, opacity=1)
        g.vertices[2].set_fill(BLUE, opacity=1)
        g.vertices[3].set_fill(GREEN, opacity=1)
        g.vertices[4].set_fill(YELLOW, opacity=1)

        self.add(g)
        self.wait(0.3)

        # Animate: move vertex 1 → position of 3, and 2 → position of 4 (edges update automatically)
        self.play(
            g[1].animate.move_to(p3),
            g[2].animate.move_to(p4),
            run_time=2
        )
        self.wait(0.5)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = MoveWithGraph()
        scene.render()
