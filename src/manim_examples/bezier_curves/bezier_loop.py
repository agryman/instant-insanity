from manim import *
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.manim_scenes.coordinate_grid import add_coordinate_grid


class BezierLoop(Scene):
    def construct(self):
        add_coordinate_grid(self)
        start_anchor = ORIGIN
        end_anchor = ORIGIN
        start_handle = start_anchor + 1.5 * RIGHT
        end_handle = end_anchor + 1.5 * UP
        bezier = CubicBezier(start_anchor, start_handle, end_handle, end_anchor, color=RED)
        #self.add(bezier)

        p1 = 2 * RIGHT + UP
        p2 = p1 + 3 * RIGHT + UP
        line = Line(p1, p2, color=BLUE)
        self.add(line)

        self.play(Transform(line, bezier), run_time=2)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = BezierLoop()
        scene.render()
