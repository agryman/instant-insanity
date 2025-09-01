"""
This module illustrates the Line3D FadeIn bug in OpenGL.
"""
import numpy as np
from manim import (DEGREES, ThreeDScene, Line3D, config, tempconfig, RendererType,
                   LEFT, RIGHT, Text, UL, BLACK, WHITE, FadeIn)

# RENDERER_TYPE: RendererType = RendererType.CAIRO
RENDERER_TYPE: RendererType = RendererType.OPENGL

config.background_color = WHITE  # must be set before scene instantiation

class FadeInLine3D(ThreeDScene):
    def construct(self):

        renderer_str = f"renderer: {config.renderer.value}"
        renderer_text = Text(renderer_str, font_size=24, color=BLACK)
        self.add_fixed_in_frame_mobjects(renderer_text)
        renderer_text.to_corner(UL)

        self.set_camera_orientation(phi=-15 * DEGREES, theta=-90 * DEGREES, gamma=0 * DEGREES)


        delay: float = 1.0
        self.wait(delay)

        line: Line3D = Line3D(LEFT, RIGHT, color=BLACK)
        self.play(FadeIn(line), run_time=delay)
        self.wait(delay)


# For running the scene directly
if __name__ == "__main__":
    with tempconfig({
        "renderer": RENDERER_TYPE
    }):
        scene = FadeInLine3D()
        scene.render(preview=True)
