"""
This module contains an animation of a cubic Bezier directed graph edge using the arrow tip object.
"""
from manim import Scene, tempconfig, UP, DOWN, LEFT, RIGHT, CubicBezier, BLACK, PURE_RED, \
    StealthTip, PURE_GREEN
from manim.typing import Point3D

from instant_insanity.mobjects.stealth_tip import mk_stealth_tip_from_cubic_bezier
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.core.config import LINEN_CONFIG


class StealthTipDemo(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        # draw a cubic Bezier curve

        # Create nodes at various positions
        node_positions = {
            'A': 2 * UP + 2 * LEFT,
            'B': 2 * UP + 2 * RIGHT,
            'C': 2 * DOWN + 2 * RIGHT,
            'D': 2 * DOWN + 2 * LEFT
        }

        p0: Point3D = node_positions['A']
        p1: Point3D = node_positions['B']
        p2: Point3D = node_positions['C']
        p3: Point3D = node_positions['D']
        edge: CubicBezier = CubicBezier(
            p0,
            p1,
            p2,
            p3,
            color=BLACK,
            stroke_width=2
        )
        self.add(edge)

        forward_tip: StealthTip = mk_stealth_tip_from_cubic_bezier(edge)
        forward_tip.set_fill(color=PURE_GREEN)
        self.add(forward_tip)

        backward_tip: StealthTip = mk_stealth_tip_from_cubic_bezier(edge, forward=False)
        backward_tip.set_fill(color=PURE_RED)
        self.add(backward_tip)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = StealthTipDemo()
        scene.render()
