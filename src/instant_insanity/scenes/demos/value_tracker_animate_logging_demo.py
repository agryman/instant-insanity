from typing import Optional
import numpy as np
from manim import logger, tempconfig, Scene, Dot, BLUE, BLACK, LEFT, ValueTracker, Mobject
from instant_insanity.core.config import LINEN_CONFIG

logger.setLevel('DEBUG')

class ValueTrackerAnimateLoggingDemo(Scene):
    """Logs the dot's position continuously by driving it with a ValueTracker."""

    def construct(self) -> None:
        dot = Dot(fill_color=BLUE, stroke_color=BLACK).move_to(LEFT * 3)
        self.add(dot)

        # Drive x-position with a tracker that we animate.
        x = ValueTracker(-3.0)

        # Updater moves the *real* dot each frame based on the tracker.
        def move_and_log(mob: Mobject) -> None:
            mob.move_to(np.array([x.get_value(), 0.0, 0.0]))
            logger.debug(f'dot center ≈ {mob.get_center().tolist()}')

        dot.add_updater(move_and_log)

        # Animate the tracker; the updater moves the dot and logs every frame.
        self.play(x.animate.set_value(3.0), run_time=3)

        dot.clear_updaters()
        self.wait(0.3)

if __name__ == '__main__':
    with tempconfig(LINEN_CONFIG):
        scene = ValueTrackerAnimateLoggingDemo()
        scene.render()