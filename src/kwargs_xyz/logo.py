"""
This module creates the kwargs.xyz logo.
"""
import numpy as np
from manim.typing import Point3D
from manim import Scene, RIGHT, UP, DOWN, BLACK, GREY, WHITE, Line, Dot, tempconfig
from kwargs_xyz.config import PREVIEW_CONFIG
class LogoScene(Scene):
    def construct(self):

        scale: float = 2.0

        delta_x: Point3D = np.sqrt(3) * RIGHT
        i: int
        u_list: list[Point3D] = [scale * (UP + i * delta_x) for i in [-1, 0, 1]]
        d_list: list[Point3D] = [scale * (DOWN + i * delta_x) for i in [-1, 0, 1]]

        stroke_defaults: dict ={
            'stroke_color': BLACK,
            'stroke_width': scale * 4
        }

        u: Point3D
        d: Point3D
        for u in u_list:
            for d in d_list:
                line: Line = Line(u, d, **stroke_defaults)
                self.add(line)

        dot_radius: float = scale * 0.25
        dot: Dot
        for u in u_list:
            dot = Dot(point=u,
                           radius=dot_radius,
                           fill_color=GREY,
                           **stroke_defaults)
            self.add(dot)

        for d in d_list:
            dot = Dot(point=d,
                           radius=dot_radius,
                           fill_color=WHITE,
                           **stroke_defaults)
            self.add(dot)

        # circle_radius: float = float(np.linalg.norm(delta_x + UP)) + 2.0 * dot_radius
        # circle: Circle = Circle(radius=circle_radius, stroke_color=BLACK)
        # self.add(circle)

        # square: Square = Square(side_length=2.0 * circle_radius, stroke_color=BLACK)
        # self.add(square)


if __name__ == "__main__":
    with tempconfig(PREVIEW_CONFIG):
        scene = LogoScene()
        scene.render()
