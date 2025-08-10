from manim import *

from instant_insanity.core.config import LINEN_CONFIG


class MoveDotsUpdateLine(Scene):
    """Animate dot1→dot3 and dot2→dot4 while a connecting line stays attached.

    The line connects the centers of dot1 and dot2 and updates continuously
    during the motion.
    """

    def construct(self):
        # Four dots
        dot1 = Dot(LEFT * 4 + DOWN * 1, color=RED, radius=0.18)
        dot2 = Dot(LEFT * 1 + UP * 2,  color=BLUE, radius=0.18)
        dot3 = Dot(RIGHT * 2 + DOWN * 2, color=GREEN, radius=0.18)
        dot4 = Dot(RIGHT * 4 + UP * 1,   color=YELLOW, radius=0.18)

        # Line that always connects current centers of dot1 and dot2
        line = always_redraw(lambda: Line(dot1.get_center(), dot2.get_center(), color=BLACK))

        self.add(dot3, dot4, dot1, dot2, line)
        self.wait(0.3)

        # Animate in parallel
        # self.play(
        #     dot1.animate.move_to(dot3.get_center()),
        #     dot2.animate.move_to(dot4.get_center()),
        #     run_time=2
        # )
        self.play(Transform(dot1, dot3),
                  Transform(dot2, dot4), run_time=2.0)
        self.wait(0.5)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = MoveDotsUpdateLine()
        scene.render()
