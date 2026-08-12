"""
This module creates the kwargs.xyz logo.
"""
import numpy as np
from manim.typing import Point3D
from manim import Scene, RIGHT, UP, DOWN, BLACK, GREY, WHITE, Line, Dot, tempconfig, VGroup, Text
from kwargs_xyz.config import PREVIEW_CONFIG


def mk_logo(scale: float = 2.0) -> VGroup:
    logo: VGroup = VGroup()

    delta_x: Point3D = np.sqrt(3) * RIGHT
    i: int
    u_list: list[Point3D] = [scale * (UP + i * delta_x) for i in [-1, 0, 1]]
    d_list: list[Point3D] = [scale * (DOWN + i * delta_x) for i in [-1, 0, 1]]

    stroke_defaults: dict = {
        'stroke_color': BLACK,
        'stroke_width': scale * 4
    }

    u: Point3D
    d: Point3D
    for u in u_list:
        for d in d_list:
            line: Line = Line(u, d, **stroke_defaults)
            logo.add(line)

    dot_radius: float = scale * 0.20
    dot: Dot
    for u in u_list:
        dot = Dot(point=u,
                  radius=dot_radius,
                  fill_color=GREY,
                  **stroke_defaults)
        logo.add(dot)

    for d in d_list:
        dot = Dot(point=d,
                  radius=dot_radius,
                  fill_color=WHITE,
                  **stroke_defaults)
        logo.add(dot)

    # add the name below the graph
    name: Text = Text('kwargs.xyz', color=BLACK, font_size=48, font='sans-serif')
    name.next_to(logo, DOWN, buff=0.25)
    logo.add(name)

    return logo


class LogoScene(Scene):
    def construct(self):
        logo = mk_logo(scale=1.25)
        self.add(logo)
        self.wait()


if __name__ == "__main__":
    with tempconfig(PREVIEW_CONFIG):
        scene = LogoScene()
        scene.render()
