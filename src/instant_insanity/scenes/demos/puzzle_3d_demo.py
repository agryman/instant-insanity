import numpy as np

from manim.typing import Point3D, Vector3D
from manim import Scene, tempconfig, RIGHT, IN, UP

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC, Puzzle
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, DEFAULT_CUBE_SIDE_LENGTH, mk_standard_puzzle3d
from instant_insanity.scenes.coordinate_grid import GridMixin


class Puzzle3DDemo(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        projection: Projection = mk_standard_orthographic_projection()
        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        puzzle3d: Puzzle3D = mk_standard_puzzle3d(puzzle_spec, projection)
        self.add(puzzle3d)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = Puzzle3DDemo()
        scene.render()

