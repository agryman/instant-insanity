import numpy as np

from manim import (Scene, Circle, Square, Create, Transform, FadeOut, PINK, TAU, RIGHT, DEGREES, LEFT, UP, DOWN, OUT, 
                   Dot3D, Line3D, VGroup, ThreeDScene, WHITE, YELLOW, ORANGE, always_redraw, Axes, TangentLine, ValueTracker,
                   Dot, RED, GREEN, BLUE, BLACK, linear, ORIGIN, config)

config.background_color = WHITE  # must be set before scene instantiation


class DefaultTemplate(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.flip(RIGHT)  # flip horizontally
        square.rotate(-3 * TAU / 8)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation

from manim import *

class ConnectedDots3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

        # Create two dots
        dot1 = Dot3D(point=LEFT + DOWN, radius=0.1, color=YELLOW)
        dot2 = Dot3D(point=RIGHT + UP, radius=0.1, color=ORANGE)

        # Create a line between them
        line = Line3D(dot1.get_center(), dot2.get_center(), color=WHITE)

        # Add updater to the line
        line.add_updater(lambda m: m.put_start_and_end_on(dot1.get_center(), dot2.get_center()))

        # Group them for convenience (optional)
        group = VGroup(dot1, dot2, line)

        self.add(group)
        self.wait()

        # Animate the dots – the line updates automatically
        self.play(dot1.animate.shift(2 * UP + 1 * OUT), dot2.animate.shift(2 * LEFT + 1 * OUT))
        self.wait()

class ConnectedDots3DFixed(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

        # Create two moving dots
        dot1 = Dot3D(point=LEFT + DOWN, radius=0.1, color=YELLOW)
        dot2 = Dot3D(point=RIGHT + UP, radius=0.1, color=ORANGE)

        # Use always_redraw to regenerate the line each frame
        line = always_redraw(lambda: Line3D(dot1.get_center(), dot2.get_center(), color=WHITE))

        self.add(dot1, dot2, line)

        # Animate the dots — line stays attached
        self.play(dot1.animate.shift(2 * UP + 1 * OUT), dot2.animate.shift(2 * LEFT + 1 * OUT))
        self.wait()
        
from manim import *

class TangentAnimation(Scene):
    def construct(self):
        ax = Axes()
        sine = ax.plot(np.sin, color=RED)
        alpha = ValueTracker(0)
        point = always_redraw(
            lambda: Dot(
                sine.point_from_proportion(alpha.get_value()),
                color=BLUE
            )
        )
        tangent = always_redraw(
            lambda: TangentLine(
                sine,
                alpha=alpha.get_value(),
                color=YELLOW,
                length=4
            )
        )
        self.add(ax, sine, point, tangent)
        self.play(alpha.animate.set_value(1), rate_func=linear, run_time=2)


class DotExample(ThreeDScene):
    def construct(self):

        # create a square and add it to the scene
        square = Square(side_length=1.0, color=RED, fill_opacity=1.0, stroke_color=BLACK, stroke_width=2).shift(LEFT + 3 * UP)
        self.add(square)
        self.wait(1)

        dot1 = Dot(point=LEFT + UP, radius=0.1, color=RED, stroke_color=BLACK, stroke_width=2)
        dot2 = Dot(point=RIGHT + UP, radius=0.1, color=GREEN, stroke_color=BLACK, stroke_width=2)
        dot3 = Dot(point=LEFT + DOWN, radius=0.1, color=BLUE, stroke_color=BLACK, stroke_width=2)
        dot4 = Dot(point=RIGHT + DOWN, radius=0.1, color=WHITE, stroke_color=BLACK, stroke_width=2)
        self.add(dot1, dot2, dot3, dot4)
        self.wait(1)

        self.play(Transform(square, dot1), run_time=2)

        

# For running the scene directly
if __name__ == "__main__":
    scene = DotExample()
    scene.render(preview=True)
