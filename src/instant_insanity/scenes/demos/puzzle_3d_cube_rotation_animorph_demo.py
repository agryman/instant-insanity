import numpy as np

from manim.typing import Vector3D
from manim import Scene, tempconfig, PI, DOWN, RIGHT

from instant_insanity.animators.puzzle_3d_animators import Puzzle3DCubeRotationAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import WINNING_MOVES_PUZZLE_SPEC
from instant_insanity.mobjects.puzzle_3d import PuzzleSpec, Puzzle3D, mk_standard_puzzle3d
from instant_insanity.scenes.coordinate_grid import GridMixin


class Puzzle3DCubeRotationAnimorphDemo(GridMixin, Scene):
    """
    This class demonstrates how to play a puzzle 3d cube rotation.
    """
    def construct(self):
        self.add_grid(True)

        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        projection: Projection = mk_standard_orthographic_projection()
        puzzle3d: Puzzle3D = mk_standard_puzzle3d(puzzle_spec, projection, centre=True)
        self.add(puzzle3d)
        self.wait()

        # rotate the puzzle
        axis: Vector3D
        for axis in [RIGHT, DOWN]:
            rotation: Vector3D = axis * PI / 2.0
            animorph = Puzzle3DCubeRotationAnimorph(puzzle3d, rotation)
            for n in range(4):
                puzzle3d.conceal_polygons()
                animorph.play(self, run_time=1.0)
                self.wait()
                puzzle3d.checkpoint()

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = Puzzle3DCubeRotationAnimorphDemo()
        scene.render()
