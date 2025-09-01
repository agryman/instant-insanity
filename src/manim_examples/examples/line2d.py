"""
This module illustrates drawing lines over a square in a 2D scene using Manim.
"""
import numpy as np
from manim import (Scene, Axes, Line, Square, config, tempconfig, RendererType,
                   LEFT, RIGHT, UP, OUT, BLACK, WHITE, RED, BLUE, Text, UL)

class Line2DExample(Scene):
    def construct(self):

        renderer_str = f"renderer: {config.renderer.value}"
        renderer_text = Text(renderer_str, color=WHITE)
        renderer_text.to_corner(UL)
        self.add(renderer_text)
        
        axes = Axes()
        x_label = axes.get_x_axis_label('x')
        y_label = axes.get_y_axis_label('y')
        self.add(axes, x_label, y_label)
        
        # the square is in the plane z = 0
        square = Square(side_length=3.0, color=RED, fill_opacity=1.0, stroke_color=BLUE, stroke_width=10)

        # the 5 lines are in the planes z = -2, -1, 0, 1, 2
        lines = [Line(2.0 * LEFT + t * (UP + OUT), 2.0 * RIGHT + t * (UP + OUT), color=WHITE, stroke_width=10)
                 for t in np.linspace(-2.0, 2.0, 5)]

        # square and lines are added in the correct order
        self.add(lines[0], lines[1], lines[2], square, lines[3], lines[4])


my_config = {
    "renderer": RendererType.CAIRO,
    "background_color": BLACK
}

# For running the scene directly
if __name__ ==  "__main__":
    with tempconfig(my_config):
        scene = Line2DExample()
        scene.render(preview=True)
