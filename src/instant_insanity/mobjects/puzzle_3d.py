"""
This module implements the Puzzle3D class which is a Polygon3D that consists
of all 24 faces of the 4 puzzle cubes.
"""
from manim.typing import Point3D, Vector3D
from manim import RIGHT, ManimColor, ORIGIN

from instant_insanity.core.geometry_types import PolygonKeyToVertexPathMapping, Point3D_Array
from instant_insanity.core.cube import FacePlane, FACE_PLANE_TO_VERTEX_PATH
from instant_insanity.core.projection import Projection
from instant_insanity.core.puzzle import Puzzle, PuzzleCubeNumber, PuzzleCube, FaceColour, FaceLabel, \
    INITIAL_FACE_PLANE_TO_LABEL
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
        i: int
        cube_number: PuzzleCubeNumber
        for i, cube_number in enumerate(PuzzleCubeNumber):
            cube_centre_i: Point3D = puzzle_centre + (i - 2.5) * cube_delta
            face_plane: FacePlane
            vertex_path: Point3D_Array
            for face_plane, vertex_path in FACE_PLANE_TO_VERTEX_PATH.items():
                face_label: FaceLabel = INITIAL_FACE_PLANE_TO_LABEL[face_plane]
                polygon_name: Puzzle3DPolygonName = (cube_number, face_label)
                name_to_model_path_0[polygon_name] = vertex_path + cube_centre_i

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
