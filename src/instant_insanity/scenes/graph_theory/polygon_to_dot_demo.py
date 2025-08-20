"""
This module creates a scene that demonstrates the PolygonToDot animator.
"""
import numpy as np
from manim import Scene, tempconfig, Square, Dot, LEFT, RIGHT, UP, DOWN, RED, BLUE, BLACK, ORIGIN, OUT

from instant_insanity.animators.polygon_to_dot_animator import PolygonToDotAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.scenes.coordinate_grid import GridMixin


class PolygonToDotDemo(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        blue_square: Square = Square(fill_color=BLUE, fill_opacity=1.0, stroke_color=BLACK, stroke_width=2.0)
        blue_square.rotate(np.pi / 3, axis=OUT, about_point=ORIGIN)
        blue_square.shift(2 * LEFT + UP)

        red_dot: Dot = Dot(fill_color=RED, fill_opacity=1.0, stroke_color=BLACK, stroke_width=2.0, radius=0.1)
        red_dot.shift(2 * RIGHT + 1 * DOWN)

        self.add(red_dot, blue_square)

        animorph: PolygonToDotAnimorph = PolygonToDotAnimorph(blue_square, red_dot)
        animorph.play(self, alpha=1.0, run_time=3.0)

        self.wait()

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = PolygonToDotDemo()
        scene.render()
