import numpy as np

from manim import (Scene, tempconfig, ORIGIN, RIGHT, LEFT, UP, OUT,
                   RED, GREEN, BLUE, YELLOW, BLACK, PI, ManimColor, PURPLE)

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.projection import Projection, PerspectiveProjection
from instant_insanity.core.puzzle import PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC
from instant_insanity.mobjects.puzzle_3d import Puzzle3D
from instant_insanity.scenes.coordinate_grid import GridMixin


class Puzzle3DDemo(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        # create a projection
        camera_z: float = 2.0
        viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
        projection: Projection = PerspectiveProjection(viewpoint, camera_z=camera_z)

        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        puzzle3d: Puzzle3D = Puzzle3D(projection, puzzle_spec)

        self.add(puzzle3d)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = Puzzle3DDemo()
        scene.render()

