"""
This module illustrates drawing lines over a square in a 3D scene using Manim.
"""
import numpy as np
from manim import (ThreeDScene, ThreeDAxes, Line3D, Square, config, tempconfig, RendererType,
                   LEFT, RIGHT, UP, OUT, WHITE, RED, BLUE, Text, UL)

class Line3DExample(ThreeDScene):
    def construct(self):

        renderer_str = f"renderer: {config.renderer.value}"
        renderer_text = Text(renderer_str)
        self.add_fixed_in_frame_mobjects(renderer_text)
        renderer_text.to_corner(UL)
        
        axes = ThreeDAxes()
        x_label = axes.get_x_axis_label('x')
        y_label = axes.get_y_axis_label('y')
        z_label = axes.get_z_axis_label('z')
        self.add(axes, x_label, y_label, z_label)
        
        # the square is in the plane z = 0
        square = Square(side_length=3.0, color=RED, fill_opacity=1.0, stroke_color=BLUE, stroke_width=10)

        # the 5 lines are in the planes z = -2, -1, 0, 1, 2
        lines = [Line3D(2.0 * LEFT + t * (UP + OUT), 2.0 * RIGHT + t * (UP + OUT), color=WHITE) 
                 for t in np.linspace(-2.0, 2.0, 5)]

        # square and lines are added in the correct order
        self.add(lines[0], lines[1], lines[2], square, lines[3], lines[4])


# opengl renders the scene correctly
# lines[3] is drawn over the square
OPENGL_CONFIG = {
    "renderer": RendererType.OPENGL
}

# cairo renders the scene incorrectly
# lines[3] is drawn under the square
# this is a bug in cairo renderer
CAIRO_CONFIG = {
    "renderer": RendererType.CAIRO
}

# For running the scene directly
if __name__ == "__main__":
    with tempconfig(OPENGL_CONFIG):
        scene = Line3DExample()
        scene.render(preview=True)
