"""
This scene demonstrates MoveToAnimorph to validate the Animorph framework.
"""
from manim import Scene, tempconfig, Circle, Square, RIGHT, LEFT, UP, DOWN, BLUE, RED, Mobject, ValueTracker
from manim.typing import Point3D

from instant_insanity.animators.animorph import MoveToAnimorph
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.core.config import LINEN_CONFIG


class MoveToAnimorphDemo(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        square: Square = Square(color=BLUE)
        square_start_point: Point3D = 2 * RIGHT
        square.move_to(square_start_point)

        circle_start_point: Point3D = 2 * LEFT
        circle: Circle = Circle(color=RED)
        circle.move_to(circle_start_point)

        self.add(square, circle)
        self.wait()

        square_end_point: Point3D = 3 * RIGHT + 2 * UP
        square_animorph: MoveToAnimorph = MoveToAnimorph(square, square_end_point)
        square_animorph.play(self)
        self.wait()

        circle_endpoint: Point3D = 3 * LEFT + 2 * DOWN
        circle_animorph: MoveToAnimorph = MoveToAnimorph(circle, circle_endpoint)
        circle_animorph.play(self)
        self.wait()

        alpha_tracker: ValueTracker = ValueTracker(1.0)
        square.add_updater(lambda m: square_animorph.morph_to(alpha_tracker.get_value()))
        circle.add_updater(lambda m: circle_animorph.morph_to(alpha_tracker.get_value()))
        self.play(alpha_tracker.animate.set_value(0.0))

        self.wait()

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = MoveToAnimorphDemo()
        scene.render()
