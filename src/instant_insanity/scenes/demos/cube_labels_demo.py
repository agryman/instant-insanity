from typing import cast

from manim import tempconfig, DOWN, OUT, PI
from manim.typing import Vector3D
from manim_voiceover import VoiceoverScene

from instant_insanity.animators.puzzle_3d_animators import Puzzle3DCubeRotationAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import Puzzle, WINNING_MOVES_PUZZLE, PuzzleCubeNumber
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.mobjects.puzzle_3d import Puzzle3D
from instant_insanity.mobjects.puzzle_face_labeller import PuzzleFaceLabeller
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.helpers import morph_and_checkpoint
from instant_insanity.scenes.part_3_graph_theory.graph_theory_scene_3 import GraphTheoryScene3
from instant_insanity.scenes.subscene import SubsceneMixin


class CubeLabelsDemo(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):

    puzzle: Puzzle
    puzzle3d: Puzzle3D
    puzzle_face_labeller: PuzzleFaceLabeller

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)
        self.say("This demo shows how to label the faces of a cube.")
        self.wait()

        puzzle: Puzzle =  WINNING_MOVES_PUZZLE
        projection: Projection = mk_standard_orthographic_projection()
        puzzle3d: Puzzle3D = GraphTheoryScene3.mk_puzzle3d(puzzle, projection)
        self.puzzle3d = puzzle3d
        self.add(puzzle3d)

        self.puzzle_face_labeller = PuzzleFaceLabeller(self, puzzle3d)

        # create the labels for the puzzle and add them to the scene
        for cube_number in PuzzleCubeNumber:
            self.puzzle_face_labeller.update_cube_texts(cube_number)

        self.wait(3.0)

        self.say("Now rotate the cubes into the solution and confirm that the rotated labels are correct.")

        solution_rotation_axes: dict[PuzzleCubeNumber, list[Vector3D]] = {
            PuzzleCubeNumber.ONE: [OUT],
            PuzzleCubeNumber.TWO: [OUT, OUT],
            PuzzleCubeNumber.THREE: [DOWN, OUT, OUT],
            PuzzleCubeNumber.FOUR: [OUT, OUT],
        }

        rotation: Vector3D
        for cube_number in PuzzleCubeNumber:
            key_cube_number: PuzzleCubeNumber
            mask: dict[PuzzleCubeNumber, bool] = {
                key_cube_number: key_cube_number == cube_number for key_cube_number in PuzzleCubeNumber
            }
            with self.voiceover(text=f"Rotate cube {cube_number}.") as tracker:
                voiceover_wait(self, tracker, 2.0)

            cube_rotation_axes: list[Vector3D] = solution_rotation_axes[cube_number]
            cube_rotation_axis: Vector3D
            for cube_rotation_axis in cube_rotation_axes:

                # remove the Text labels from the scene before rotating the cube
                self.puzzle_face_labeller.remove_cube_texts(cube_number)

                # rotate the cube
                rotation = cast(Vector3D, cube_rotation_axis * PI / 2.0)
                animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(puzzle3d, rotation, mask)
                morph_and_checkpoint(self, animorph)

                # rotate the cube plane-to-label mapping
                self.puzzle_face_labeller.rotate_plane_to_label_mapping(cube_number, cube_rotation_axis)

                # create the Text labels for the rotated cube and add them to the scene
                self.puzzle_face_labeller.update_cube_texts(cube_number)

                self.wait(2.0)
        self.wait(3.0)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = CubeLabelsDemo()
        scene.render()


