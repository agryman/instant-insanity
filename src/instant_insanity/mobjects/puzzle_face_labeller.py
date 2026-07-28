"""
This class manages the labels on the visible faces of cubes in a puzzle.

It assumes that each cube in the puzzle is initially in the standard position as
defined by the Carteblache labelling scheme:
Front is x
Back is x'
Right is y
Left  is y'
Top is z
Bottom is z'

We allow any cube in the puzzle to be rotated by 90 degrees about the unit outward-pointing
normal vector at the centre of each face. The rotation results in a permuation of the labels.
We are only interested in labels for the visible faces. We assume the scene is drawn
by projecting the 3d-cube onto a 2d camera plane. Initially, only the front, right, and top
faces are visible.

The face labels are manim Text objects. We remove them from the scenebefore an animated rotation and
add them back to the scene after the rotations is completed.
"""
from manim import Scene, Text, Polygon, DOWN, RIGHT, UP
from manim.typing import Vector3D

from instant_insanity.core.cube import FacePlane
from instant_insanity.core.cube_rotations import VisibleCubeTexts, PlaneToLabelMapping, INITIAL_PLANE_TO_LABEL_MAPPING, \
    mk_label_from_str, rotate_by_vector
from instant_insanity.core.puzzle import PuzzleCubeNumber, FaceLabel
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, Puzzle3DPolygonName


# only front, right, and top cube faces are visible in the standard orthographic projection
VISIBLE_PLANES: list[FacePlane] = [FacePlane.FRONT, FacePlane.RIGHT, FacePlane.TOP]

# these are the relative positions of the text labels with respect to the face polygons
TEXT_DIRECTIONS: list[Vector3D] = [DOWN, RIGHT, UP]

class PuzzleFaceLabeller:
    scene: Scene
    puzzle3d: Puzzle3D
    cube_to_mapping: dict[PuzzleCubeNumber, PlaneToLabelMapping]
    cube_to_visible_texts: dict[PuzzleCubeNumber, VisibleCubeTexts]

    def __init__(self, scene: Scene, puzzle3d: Puzzle3D) -> None:
        self.scene = scene
        self.puzzle3d = puzzle3d

        cube_number: PuzzleCubeNumber

        # we need to keep track of the mapping from face plane to face label for each cube
        self.cube_to_mapping ={
            cube_number: INITIAL_PLANE_TO_LABEL_MAPPING for cube_number in PuzzleCubeNumber
        }

        # we need to keep track of the text label mobjects so we can remove them before a rotation
        self.cube_to_visible_texts = {
            cube_number: VisibleCubeTexts(front=Text(""), right=Text(""), top=Text(""))
            for cube_number in PuzzleCubeNumber
        }

    def update_cube_texts(
            self,
            cube_number: PuzzleCubeNumber
    ) -> None:
        """
        Updates the Text objects associated with the labels of a cube
        and adds them to the scene.
        It mutates the texts object in place.

        Args:
            cube_number: the cube number.
        """
        plane_to_label_mapping: dict[FacePlane, FaceLabel] = self.cube_to_mapping[cube_number]
        texts: VisibleCubeTexts = self.cube_to_visible_texts[cube_number]

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
            self.scene.add(text)

    def update_puzzle_texts(self) -> None:
        """
        Updates all cubes in the puzzle.
        """
        cube_number: PuzzleCubeNumber
        for cube_number in PuzzleCubeNumber:
            self.update_cube_texts(cube_number)

    def remove_cube_texts(self, cube_number: PuzzleCubeNumber) -> None:
        """
        Removes the texts associated with the labels of a cube from the scene.
        Args:
            cube_number: the cube number.
        """
        texts: VisibleCubeTexts = self.cube_to_visible_texts[cube_number]
        visible_plane: FacePlane
        for visible_plane in VISIBLE_PLANES:
            text: Text = texts.get_label(visible_plane)
            self.scene.remove(text)

    def remove_puzzle_texts(self) -> None:
        """
        Removes all cubes in the puzzle.
        """
        cube_number: PuzzleCubeNumber
        for cube_number in PuzzleCubeNumber:
            self.remove_cube_texts(cube_number)

    def rotate_plane_to_label_mapping(self, cube_number: PuzzleCubeNumber, cube_rotation_axis: Vector3D) -> None:
        """
        Rotates the plane-to-label mapping for a cube and rotation vector.

        Args:
            cube_number: the cube number.
            cube_rotation_axis: the cube rotation axis.
        """

        # rotate the cube's plane-to-label mapping
        plane_to_label_mapping: PlaneToLabelMapping = self.cube_to_mapping[cube_number]
        plane_to_label_mapping = rotate_by_vector(cube_rotation_axis, plane_to_label_mapping)
        self.cube_to_mapping[cube_number] = plane_to_label_mapping
