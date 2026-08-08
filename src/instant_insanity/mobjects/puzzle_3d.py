"""
This module implements the Puzzle3D class which is a Polygon3D that consists
of all 24 faces of the 4 puzzle cubes.
"""
import numpy as np

from manim.typing import Point3D, Vector3D
from manim import RIGHT, ManimColor, ORIGIN, IN, UP, DOWN

from instant_insanity.core.geometry_types import PolygonKeyToVertexPathMapping, Point3D_Array
from instant_insanity.core.cube import FacePlane, FACE_PLANE_TO_VERTEX_PATH
from instant_insanity.core.projection import Projection
from instant_insanity.core.puzzle import Puzzle, PuzzleCubeNumber, PuzzleCube, FaceColour, FaceLabel, \
    INITIAL_FACE_PLANE_TO_LABEL, PuzzleSpec
from instant_insanity.mobjects.polygons_3d import Polygons3D, DEFAULT_POLYGON_SETTINGS
from instant_insanity.mobjects.puzzle_cube_3d import PuzzleCube3D
from instant_insanity.mobjects.coloured_cube import MANIM_COLOUR_MAP

type CubeNumberToCubeMapping = dict[PuzzleCubeNumber, PuzzleCube3D]

# A polygon in this group is uniquely identified by the pair (cube_number, face_label).
type Puzzle3DPolygonName = tuple[PuzzleCubeNumber, FaceLabel]

DEFAULT_CUBE_SIDE_LENGTH: float = 2.0  # the side length of the standard cube
DEFAULT_BUFF: float = 0.1  # the horizontal space between cubes, MUST be positive to avoid collisions
DEFAULT_CUBE_DELTA: Vector3D = (DEFAULT_CUBE_SIDE_LENGTH + DEFAULT_BUFF) * RIGHT


class Puzzle3D(Polygons3D[Puzzle3DPolygonName]):

    """
    This class implements a 3D puzzle.
    The puzzle consists of four 3D puzzle cubes.
    The puzzle contains the flattened list of all the faces of the cubes.
    Since each cube has six faces, there are a total of 24 polygons in the puzzle.
    A face from one cube may obscure a face from another cube so the set of all faces
    must be depth-sorted as a whole.

    Attributes:
        puzzle: the Puzzle object.
        puzzle_centre: the centre of the puzzle.
        cube_delta: the change in centres between cubes.
    """
    puzzle: Puzzle
    puzzle_centre: Point3D
    cube_delta: Vector3D

    def __init__(self, projection: Projection,
                 puzzle: Puzzle,
                 puzzle_centre: Point3D = ORIGIN,
                 cube_delta: Vector3D = DEFAULT_CUBE_DELTA) -> None:
        self.puzzle = puzzle
        self.puzzle_centre = puzzle_centre
        self.cube_delta = cube_delta
        key_to_model_path_0: PolygonKeyToVertexPathMapping[Puzzle3DPolygonName] = Puzzle3D.mk_name_to_model_path_0(puzzle_centre, cube_delta)

        super().__init__(projection, key_to_model_path_0)

    @staticmethod
    def mk_cube_centre(cube_number: PuzzleCubeNumber, puzzle_centre: Point3D, cube_delta: Vector3D) -> Point3D:
        """
        This method makes the cube centre for a given cube number.
        The cubes are numbered from 1 to 4.
        The centre corresponds to cube number 2.5.
        The cubes are laid out in a line and centred on the given puzzle centre.
        The offset from cube to cube is the given cube delta vector.

        Args:
            cube_number: The puzzle cube number.
            puzzle_centre: The centre of the puzzle.
            cube_delta: The change in centres between cubes.

        Returns:
            the centre of the cube.
        """
        n: int = cube_number.value
        cube_centre: Point3D = puzzle_centre + (n - 2.5) * cube_delta

        return cube_centre

    @staticmethod
    def mk_name_to_model_path_0(puzzle_centre: Point3D,
                                cube_delta: Vector3D) -> PolygonKeyToVertexPathMapping[Puzzle3DPolygonName]:
        """
        Makes the initial model space vertex paths.

        Args:
            puzzle_centre: the centre of puzzle.
            cube_delta: the change in centres between cubes.

        Returns:
            the initial model space vertex paths.
        """
        # arrange the cubes horizontally from left to right with centres shifted by cube_delta

        name_to_model_path_0: PolygonKeyToVertexPathMapping[Puzzle3DPolygonName] = dict()
        cube_number: PuzzleCubeNumber
        for cube_number in PuzzleCubeNumber:
            cube_centre_n: Point3D = Puzzle3D.mk_cube_centre(cube_number, puzzle_centre, cube_delta)
            face_plane: FacePlane
            vertex_path: Point3D_Array
            for face_plane, vertex_path in FACE_PLANE_TO_VERTEX_PATH.items():
                face_label: FaceLabel = INITIAL_FACE_PLANE_TO_LABEL[face_plane]
                polygon_name: Puzzle3DPolygonName = (cube_number, face_label)
                name_to_model_path_0[polygon_name] = vertex_path + cube_centre_n

        return name_to_model_path_0

    def get_polygon_settings(self, polygon_name: Puzzle3DPolygonName) -> dict:
        """
        Gets a dict of settings the polygon.

        Args:
            polygon_name: a polygon name tuple (cube_number, face_label).

        Returns:
            a dict of settings the polygon.
        """
        cube_number: PuzzleCubeNumber
        face_label: FaceLabel
        cube_number, face_label = polygon_name
        puzzle_cube: PuzzleCube = self.puzzle.number_to_cube[cube_number]
        colour_name: FaceColour = puzzle_cube.face_label_to_colour[face_label]
        colour: ManimColor = MANIM_COLOUR_MAP[colour_name]
        polygon_settings: dict = DEFAULT_POLYGON_SETTINGS.copy()
        polygon_settings['fill_color'] = colour

        return polygon_settings

    def get_colour_name(self, cube_number: PuzzleCubeNumber, face_label: FaceLabel) -> FaceColour:
        puzzle: Puzzle = self.puzzle
        cube: PuzzleCube = puzzle.number_to_cube[cube_number]
        colour_name: FaceColour = cube.face_label_to_colour[face_label]
        return colour_name

    def hide_cube(self, cube_number: PuzzleCubeNumber) -> None:
        cube_names: set[Puzzle3DPolygonName] = {(cube_number, face_label)
                                                for face_label in FaceLabel}
        visible_polygon_keys: set[Puzzle3DPolygonName] = self.visible_polygon_keys - cube_names
        self.set_visible_polygon_keys(visible_polygon_keys)

    def get_face_min_max(self, cube_number: PuzzleCubeNumber, face_label: FaceLabel) -> tuple[Point3D, Point3D]:
        """
        This function returns the min and max of the vertex path of a cube face.

        Args:
            cube_number: the cube number.
            face_label: the face label.

        Returns:
            (min_vertex: Point3D, max_vertex: Point3D)
        """
        face_name: Puzzle3DPolygonName = (cube_number, face_label)
        path: Point3D_Array = self.key_to_model_path_0[face_name]
        path_min: Point3D = np.min(path, axis=0)
        path_max: Point3D = np.max(path, axis=0)

        return path_min, path_max

    def get_cube_width(self) -> float:
        """
        This function returns the width of the cube.
        Assume that all cubes have the same width and are arranged along the x-axis.

        Returns:
            width: the width of the cube.
        """
        cube_1_right_max: Point3D
        _, cube_1_right_max = self.get_face_min_max(PuzzleCubeNumber.ONE, FaceLabel.X)
        cube_1_right_max_x: float = cube_1_right_max[0]

        cube_1_left_min: Point3D
        cube_1_left_min, _ = self.get_face_min_max(PuzzleCubeNumber.ONE, FaceLabel.X_PRIME)
        cube_1_left_min_x: float = cube_1_left_min[0]

        assert cube_1_left_min_x < cube_1_right_max_x

        width: float = cube_1_right_max_x - cube_1_left_min_x
        return width


    def get_cube_gap(self) -> float:
        """
        This function returns the gap between two cubes.
        Assume that the puzzle is arranged in a row along the x-axis.

        Returns:
            gap: the gap between two cubes.
        """
        cube_1_right_max: Point3D
        _, cube_1_right_max = self.get_face_min_max(PuzzleCubeNumber.ONE, FaceLabel.X)
        cube_1_right_max_x: float = cube_1_right_max[0]

        cube_2_left_min: Point3D
        cube_2_left_min, _ = self.get_face_min_max(PuzzleCubeNumber.TWO, FaceLabel.X_PRIME)
        cube_2_left_min_x: float = cube_2_left_min[0]

        assert cube_1_right_max_x < cube_2_left_min_x

        gap: float = cube_2_left_min_x - cube_1_right_max_x

        return gap


def mk_standard_puzzle3d(puzzle_spec: PuzzleSpec, projection: Projection, centre: bool = False) -> Puzzle3D:
    """
    Makes a puzzle in the top half of the scene.

    Args:
        puzzle_spec: the puzzle spec.
        projection: the projection.
        centre: shift the puzzle down to the centre of the screen

    Returns:
        the 3D puzzle.
    """
    puzzle: Puzzle = Puzzle(puzzle_spec)
    buff: float = DEFAULT_CUBE_SIDE_LENGTH * 2.0 * (np.sqrt(2.0) - 1.0)
    puzzle_centre: Point3D = 2 * IN + 1.0 * RIGHT + 1.0 * UP
    if centre:
        puzzle_centre += 4.5 * DOWN
    cube_delta: Vector3D = (DEFAULT_CUBE_SIDE_LENGTH + buff) * RIGHT
    puzzle3d: Puzzle3D = Puzzle3D(projection, puzzle, puzzle_centre, cube_delta)

    return puzzle3d
