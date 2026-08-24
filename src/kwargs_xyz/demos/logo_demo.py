"""
This module creates a manim Scene that displays the kwarg.xyz logo.
"""
from manim import Scene, tempconfig

from kwargs_xyz.config import LINEN_CONFIG
from kwargs_xyz.logo import mk_logo


class LogoDemo(Scene):
    def construct(self):
        logo = mk_logo(scale=1.25)
        self.add(logo)
        self.wait()


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = LogoDemo()
        scene.render()
