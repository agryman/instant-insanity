import logging
import numpy as np
from manim import logger, Scene, console, Dot, RED, BLACK, LEFT, Mobject, RIGHT, tempconfig

from instant_insanity.core.config import LINEN_CONFIG

logger.setLevel(logging.DEBUG)

class DotAnimateLoggingDemo(Scene):
    """Scene demonstrating Manim's logger and console.

    Logs at INFO/DEBUG levels and prints to the rich console.
    Uses an updater with throttling to periodically report a dot's position.
    """

    def construct(self) -> None:
        logger.info('LoggingDemo: construct() started')
        console.print('[bold green]Console:[/bold green] hello from LoggingDemo')

        dot = Dot(fill_color=RED, radius=0.5, stroke_color=BLACK, stroke_width=2).move_to(LEFT * 3)
        self.add(dot)

        # Throttled updater: log dot center about twice per second.
        throttle_every = 0.5  # seconds
        elapsed: float = 0.0

        def report_position(mob: Mobject, dt: float) -> None:
            nonlocal elapsed
            elapsed += dt
            if elapsed >= throttle_every:
                p: np.ndarray = mob.get_center()
                logger.debug(f'dot center ≈ {p.tolist()}')
                elapsed = 0.0

        dot.add_updater(report_position)

        logger.info('Animating dot to the right...')
        self.play(dot.animate.shift(RIGHT * 6), run_time=3)

        dot.clear_updaters()
        logger.warning('Animation finished; updaters cleared.')
        self.wait(0.5)
        logger.info('LoggingDemo: construct() completed')


if __name__ == '__main__':
    # Run directly without CLI using your preferred tempconfig pattern.
    with tempconfig(LINEN_CONFIG):
        scene = DotAnimateLoggingDemo()
        scene.render()