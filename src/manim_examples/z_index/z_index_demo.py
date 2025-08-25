from manim import *

from instant_insanity.core.config import PREVIEW_CONFIG

class ZIndexDemo(Scene):
    def construct(self):
        back = Square().set_fill('#cccccc', 1).set_stroke(width=0).shift(LEFT)
        mid  = Circle().set_fill('#88ccff', 1).set_stroke(width=0)
        top  = Triangle().set_fill('#ff8888', 1).set_stroke(width=0).shift(RIGHT)

        # Same z_index -> insertion order decides (top is drawn last)
        back.z_index = 0
        mid.z_index = 0
        top.z_index = 0

        self.add(back, mid, top)  # triangle on top
        self.wait(0.5)

        # Now force the circle above the triangle
        mid.z_index = 10           # higher z_index wins
        self.wait(0.5)

        # Bring square to the very top (without touching z_index)
        self.bring_to_front(back)  # adjusts ordering so 'back' is last drawn
        self.wait(0.5)

if __name__ == "__main__":
    with tempconfig(PREVIEW_CONFIG):
        scene = ZIndexDemo()
        scene.render()
