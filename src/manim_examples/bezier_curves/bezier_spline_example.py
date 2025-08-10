from manim import *
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.manim_scenes.coordinate_grid import add_coordinate_grid


class BezierSplineExample(Scene):
    def construct(self):
        add_coordinate_grid(self)

        p1 = np.array([-3, 1, 0])
        p1b = p1 + [1, 0, 0]
        d1 = Dot(point=p1).set_color(BLUE)
        l1 = Line(p1, p1b, color=BLACK)
        p2 = np.array([3, -1, 0])
        p2b = p2 - [1, 0, 0]
        d2 = Dot(point=p2).set_color(RED)
        l2 = Line(p2, p2b, color=BLACK)
        start_anchor = p1b
        end_anchor = p2b
        start_handle = start_anchor + 3 * RIGHT
        end_handle = end_anchor - 3 * RIGHT
        bezier = CubicBezier(start_anchor, start_handle, end_handle, end_anchor)
        d3 = Dot(point=start_anchor).set_color(GREEN)
        d4 = Dot(point=start_handle).set_color(ORANGE)
        d5 = Dot(point=end_handle).set_color(YELLOW)
        d6 = Dot(point=end_anchor).set_color(PURPLE)
        start_tangent = Arrow(start_anchor, start_handle, color=GRAY, buff=0, tip_shape=StealthTip)
        end_tangent = Arrow(end_anchor, end_handle, color=GRAY, buff=0, tip_shape=StealthTip)
        self.add(l1, d1, l2, d2, bezier, start_tangent, end_tangent, d3, d4, d5, d6)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = BezierSplineExample()
        scene.render()
