from manim import *

from instant_insanity.core.config import LINEN_CONFIG


class GraphWithLoop(Scene):
    def construct(self):
        p1 = LEFT * 4 + DOWN * 1
        p2 = LEFT * 1 + UP * 2
        p3 = RIGHT * 2 + DOWN * 2
        p4 = RIGHT * 4 + UP * 1

        g = Graph(
            vertices=[1, 2, 3, 4],
            edges=[(1, 2)],
            layout={1: p1, 2: p2, 3: p3, 4: p4},
            vertex_type=Dot,
            vertex_config={'radius': 0.18, 'stroke_color': BLACK},
            edge_config={'stroke_color': BLACK, 'stroke_width': 2},
        )

        g.vertices[1].set_fill(RED)
        g.vertices[2].set_fill(BLUE)
        g.vertices[3].set_fill(GREEN)
        g.vertices[4].set_fill(YELLOW)

        self.add(g)
        self.wait(0.3)

        # Move both vertices to p3
        self.play(
            g[1].animate.move_to(p3),
            g[2].animate.move_to(p3),
            run_time=1.5
        )

        # Draw a loop manually at p3
        loop = Circle(radius=0.4, color=BLACK).move_to(p3 + RIGHT * 0.25)
        self.play(Create(loop))
        self.wait(0.5)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphWithLoop()
        scene.render()
