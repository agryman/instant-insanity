from manim import *

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.scenes.coordinate_grid import GridMixin


class BezierBecomeDemo(GridMixin, Scene):
    def construct(self):
        red_bez = CubicBezier(LEFT, UP, RIGHT, DOWN, stroke_color=RED)
        first_points = red_bez.points.copy()
        self.add(red_bez)
        self.wait()

        # Animate the control points moving
        self.play(
            red_bez.animate.put_start_and_end_on([-4, -2, 0], [4, -2, 0])  # moves endpoints
        )
        second_points = red_bez.points.copy()

        # Now animate control points directly
        third_points = np.array([
            [-4, -2, 0],   # new start
            [-2,  2, 0],   # new control1
            [ 2,  2, 0],   # new control2
            [ 4, -2, 0],   # new end
        ], dtype=np.float64)
        start_anchor, start_handle, end_handle, end_anchor = tuple(third_points)
        blue_bez = CubicBezier(start_anchor, start_handle, end_handle, end_anchor, stroke_color=BLUE)
        fourth_points = blue_bez.points.copy()
        self.play(
            red_bez.animate.become(blue_bez),
        )
        self.wait()

        blue_bez.set_points(first_points)
        self.play(FadeIn(blue_bez))
        self.wait()

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = BezierBecomeDemo()
        scene.render()
