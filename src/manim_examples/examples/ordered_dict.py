from manim import *
from collections import OrderedDict
from instant_insanity.core.config import LINEN_CONFIG

class NamedMobjectDict(Scene):
    def construct(self):
        # Create an OrderedDict to store named Mobjects
        node_map: OrderedDict[str, Mobject] = OrderedDict()

        # Example: create and store four Dots with unique names
        positions = [LEFT + UP, RIGHT + UP, RIGHT + DOWN, LEFT + DOWN]
        names = ['A', 'B', 'C', 'D']
        colors = [RED, GREEN, BLUE, WHITE]

        for name, pos, color in zip(names, positions, colors):
            dot = Dot(
                point=pos,
                radius=DEFAULT_DOT_RADIUS * 2,
                color=BLACK,
                fill_color=color,
                stroke_color=BLACK,
                stroke_width=2
            )
            node_map[name] = dot
            self.add(dot)

        # Access and animate a specific Mobject by name
        self.play(node_map['B'].animate.shift(UP))

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = NamedMobjectDict()
        scene.render()
