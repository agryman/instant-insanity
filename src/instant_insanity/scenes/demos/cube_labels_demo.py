from typing import cast

from manim import tempconfig, Polygon, Tex, BLACK, DOWN, Text, RIGHT, UP, OUT, PI
from manim.typing import Vector3D
from manim_voiceover import VoiceoverScene

from instant_insanity.animators.puzzle_3d_animators import Puzzle3DCubeRotationAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FacePlane
from instant_insanity.core.cube_rotations import PlaneToLabelMapping, INITIAL_PLANE_TO_LABEL_MAPPING, VisibleCubeTexts, \
    mk_label_from_str, rotate_by_vector
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import Puzzle, WINNING_MOVES_PUZZLE, PuzzleCubeNumber, FaceLabel
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, Puzzle3DPolygonName
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.helpers import morph_and_checkpoint
from instant_insanity.scenes.part_3_graph_theory.graph_theory_scene_3 import GraphTheoryScene3

# only front, right, and top cube faces are visible in the standard orthographic projection
VISIBLE_PLANES: list[FacePlane] = [FacePlane.FRONT, FacePlane.RIGHT, FacePlane.TOP]

# these are the relative positions of the labels with respect to the face polygons
TEXT_DIRECTIONS: list[Vector3D] = [DOWN, RIGHT, UP]

class CubeLabelsDemo(GridMixin, DiscussionMixin, VoiceoverScene):

    playlist: list[object]
    puzzle: Puzzle
    puzzle3d: Puzzle3D

    def update_texts(
            self,
            cube_number: PuzzleCubeNumber,
            plane_to_label_mapping: dict[FacePlane, FaceLabel],
            texts: VisibleCubeTexts
    ) -> None:
        """
        Updates the Text objects associated with the labels of a cube
        and adds them to the scene.
        It mutates the texts object in place.

        Args:
            cube_number: the cube number.
            plane_to_label_mapping: the mapping from face plane to face label for the cube.
            texts: the Text objects associated with the visible faces of the cube.
        """
        for visible_plane, direction in zip(VISIBLE_PLANES, TEXT_DIRECTIONS):
            # get the face label for the face plane
            visible_label: FaceLabel = plane_to_label_mapping[visible_plane]

            # create a Text object from the face label value
            text: Text = mk_label_from_str(visible_label.value)
            texts.set_label(visible_plane, text)

            # get the polygon for the face label and position the Text near it
            key: Puzzle3DPolygonName = (cube_number, visible_label)
            polygon: Polygon = self.puzzle3d.key_to_scene_polygon[key]
            text.next_to(polygon, direction, buff=0.1)
            self.add(text)

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)
        self.playlist = [
        ]
        self.say("This demo shows how to label the faces of a cube.")
        self.wait()

        puzzle: Puzzle =  WINNING_MOVES_PUZZLE
        projection: Projection = mk_standard_orthographic_projection()
        puzzle3d: Puzzle3D = GraphTheoryScene3.mk_puzzle3d(puzzle, projection)
        self.puzzle3d = puzzle3d
        self.add(puzzle3d)

        # we need to keep track of the face plane to face label mapping for each cube
        cube_number: PuzzleCubeNumber
        cube_to_mapping: dict[PuzzleCubeNumber, PlaneToLabelMapping] = {
            cube_number: INITIAL_PLANE_TO_LABEL_MAPPING for cube_number in PuzzleCubeNumber
        }

        # we need to keep track of the label mobjects so we can remove them before a rotation
        cube_to_visible_texts: dict[PuzzleCubeNumber, VisibleCubeTexts] = {
            cube_number: VisibleCubeTexts(front=Text(""), right=Text(""), top=Text(""))
            for cube_number in PuzzleCubeNumber
        }

        # create the labels for the puzzle and add them to the scene
        for cube_number in PuzzleCubeNumber:

            # create a Text object for each visible face plane
            plane_to_label_mapping: PlaneToLabelMapping = cube_to_mapping[cube_number]
            texts: VisibleCubeTexts = cube_to_visible_texts[cube_number]
            self.update_texts(cube_number, plane_to_label_mapping, texts)
            # for visible_plane, direction in zip(VISIBLE_PLANES, TEXT_DIRECTIONS):
            #
            #     # get the face label for the face plane
            #     visible_label: FaceLabel = plane_to_label_mapping[visible_plane]
            #
            #     # create a Text object from the face label value
            #     text: Text = mk_label_from_str(visible_label.value)
            #     texts.set_label(visible_plane, text)
            #
            #     # get the polygon for the face label and position the Text near it
            #     key: Puzzle3DPolygonName = (cube_number, visible_label)
            #     polygon: Polygon = puzzle3d.key_to_scene_polygon[key]
            #     text.next_to(polygon, direction, buff=0.1)
            #     self.add(text)
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

            texts = cube_to_visible_texts[cube_number]

            cube_rotation_axes: list[Vector3D] = solution_rotation_axes[cube_number]
            cube_rotation_axis: Vector3D
            for cube_rotation_axis in cube_rotation_axes:

                # remove the Text labels from the scene before rotating the cube
                for visible_plane in VISIBLE_PLANES:
                    text = texts.get_label(visible_plane)
                    self.remove(text)

                # rotate the cube
                rotation = cast(Vector3D, cube_rotation_axis * PI / 2.0)
                animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(puzzle3d, rotation, mask)
                morph_and_checkpoint(self, animorph)

                # rotate the cube plane-to-label mapping
                plane_to_label_mapping = cube_to_mapping[cube_number]
                plane_to_label_mapping = rotate_by_vector(cube_rotation_axis, plane_to_label_mapping)
                cube_to_mapping[cube_number] = plane_to_label_mapping

                # create the Text labels for the rotated cube and add them to the scene
                self.update_texts(cube_number, plane_to_label_mapping, texts)

                self.wait(2.0)
        self.wait(3.0)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = CubeLabelsDemo()
        scene.render()


