"""This module creates the kwargs.xyz logo."""

from typing import Any

import numpy as np
from manim import (
    BLACK,
    DOWN,
    GREY,
    RIGHT,
    UP,
    WHITE,
    Dot,
    Line,
    Scene,
    Text,
    VGroup,
    tempconfig,
)
from manim.typing import Point3D

from kwargs_xyz_core.config import LINEN_CONFIG


def mk_logo(scale: float = 2.0) -> VGroup:
    """Make a manim VGroup that contains the kwargs.xyz logo.

    Args:
        scale: The scale factor for the logo.

    Returns:
        A manim VGroup that contains the logo.
    """
    logo: VGroup = VGroup()

    delta_x: Point3D = np.sqrt(3) * RIGHT
    u_list: list[Point3D] = [scale * (UP + i * delta_x) for i in [-1, 0, 1]]
    d_list: list[Point3D] = [scale * (DOWN + i * delta_x) for i in [-1, 0, 1]]

    stroke_defaults: dict[str, Any] = {"stroke_color": BLACK, "stroke_width": scale * 4}

    u: Point3D
    d: Point3D
    for u in u_list:
        for d in d_list:
            line: Line = Line(u, d, **stroke_defaults)
            logo.add(line)

    dot_radius: float = scale * 0.20
    dot: Dot
    for u in u_list:
        dot = Dot(point=u, radius=dot_radius, fill_color=GREY, **stroke_defaults)
        logo.add(dot)

    for d in d_list:
        dot = Dot(point=d, radius=dot_radius, fill_color=WHITE, **stroke_defaults)
        logo.add(dot)

    # add the name below the graph
    name: Text = Text("kwargs.xyz", color=BLACK, font_size=48, font="sans-serif")
    name.next_to(logo, DOWN, buff=0.25)
    logo.add(name)

    return logo


class LogoDemo(Scene):
    """A manim scene that displays the kwargs.xyz logo."""

    def construct(self) -> None:
        """Create a manim scene that contains the kwargs.xyz logo."""
        logo = mk_logo(scale=1.25)
        self.add(logo)
        self.wait()


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = LogoDemo()
        scene.render()
