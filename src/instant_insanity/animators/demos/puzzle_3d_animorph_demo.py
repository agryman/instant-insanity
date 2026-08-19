from typing import cast

from manim import tempconfig, Scene, UP, RIGHT, PI, LEFT
from manim.typing import Vector3D

from instant_insanity.animators.puzzle_3d_animators import Puzzle3DTranslationAnimorph, Puzzle3DCubeRotationAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import Puzzle, PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC, WINNING_MOVES_PUZZLE
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, mk_standard_puzzle3d
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.helpers import morph_and_checkpoint
from instant_insanity.scenes.subscene import SubsceneMixin


class Puzzle3DAnimorphDemo(GridMixin, SubsceneMixin, DiscussionMixin, Scene):
    """
    This class demonstrates translation and rotation of the cubes in the puzzle.

    Attributes
    puzzle: the puzzle
    puzzle3d: the 3d puzzle
    """
    puzzle: Puzzle
    puzzle3d: Puzzle3D

    def construct(self):
        self.add_grid(True)

        # create and display the 3D puzzle
        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        puzzle: Puzzle = WINNING_MOVES_PUZZLE
        projection: Projection = mk_standard_orthographic_projection()

        self.puzzle = puzzle
        self.puzzle3d = mk_standard_puzzle3d(puzzle_spec, projection, centre=True)
        self.add(self.puzzle3d)
        self.wait()

        puzzle3d: Puzzle3D = self.puzzle3d
        scene_per_model: float = puzzle3d.projection.conversion.scene_per_model
        translate_up: Vector3D = (2.0 / scene_per_model) * UP
        move_up: Puzzle3DTranslationAnimorph = Puzzle3DTranslationAnimorph(puzzle3d, translate_up)

        morph_and_checkpoint(self, move_up)
        self.wait()

        rotation_right_90: Vector3D = cast(Vector3D, RIGHT * PI / 2.0)
        rotate_right_90: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(puzzle3d, rotation_right_90)

        morph_and_checkpoint(self, rotate_right_90, run_time=0.5)
        self.wait()

        translate_right: Vector3D = (2.0 / scene_per_model) * RIGHT
        move_up: Puzzle3DTranslationAnimorph = Puzzle3DTranslationAnimorph(puzzle3d, translate_right)
        morph_and_checkpoint(self, move_up)
        self.wait()


        rotation_right_180: Vector3D = 2.0 * rotation_right_90
        rotate_right_180: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(puzzle3d, rotation_right_180)
        morph_and_checkpoint(self, rotate_right_180, run_time=1.0)
        self.wait()

        translate_left: Vector3D = (2.0 / scene_per_model) * LEFT
        move_up: Puzzle3DTranslationAnimorph = Puzzle3DTranslationAnimorph(puzzle3d, translate_left)
        morph_and_checkpoint(self, move_up)
        self.wait()

        rotation_right_360: Vector3D = 4.0 * rotation_right_90
        rotate_right_360: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(puzzle3d, rotation_right_360)
        morph_and_checkpoint(self, rotate_right_360, run_time=2.0)
        self.wait()

        translate_down: Vector3D = -1.0 * translate_up
        move_down: Puzzle3DTranslationAnimorph = Puzzle3DTranslationAnimorph(puzzle3d, translate_down)
        morph_and_checkpoint(self, move_down)
        self.wait()

        morph_and_checkpoint(self, rotate_right_90, run_time=0.5)
        self.wait()


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = Puzzle3DAnimorphDemo()
        scene.render()
