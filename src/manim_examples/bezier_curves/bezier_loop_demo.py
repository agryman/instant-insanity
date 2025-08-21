from manim import *
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.scenes.coordinate_grid import add_coordinate_grid, GridMixin


class BezierLoopDemo(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        start_anchor = ORIGIN
        end_anchor = ORIGIN
        start_handle = start_anchor + 1.5 * RIGHT
        end_handle = end_anchor + 1.5 * UP
        red_bezier = CubicBezier(start_anchor, start_handle, end_handle, end_anchor, color=RED)

        self.play(FadeIn(red_bezier))
        self.wait()

        self.play(FadeOut(red_bezier))

        p1 = 2 * RIGHT + UP
        p2 = p1 + 3 * RIGHT + UP
        blue_line = Line(p1, p2, color=BLUE)
        self.play(FadeIn(blue_line))

        self.play(Transform(blue_line, red_bezier), run_time=2)
        self.wait()


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = BezierLoopDemo()
        scene.render()
