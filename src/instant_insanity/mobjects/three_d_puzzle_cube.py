from manim import ManimColor, WHITE, BLACK, Polygon, LineJointType

from instant_insanity.core.cube import FaceName, FACE_NAME_TO_VERTEX_PATH
from instant_insanity.core.geometry_types import PolygonIdToVertexPathMapping, PolygonId, VertexPath
from instant_insanity.core.projection import Projection
from instant_insanity.core.puzzle import PuzzleCubeSpec, PuzzleCube, FaceColour
from instant_insanity.scenes.coloured_cube import MANIM_COLOUR_MAP
from instant_insanity.mobjects.three_d_polygons import ThreeDPolygons

class ThreeDPuzzleCube(ThreeDPolygons):
    polygon_settings: dict = {
        'fill_color': WHITE,
        'fill_opacity': 1.0,
        'stroke_color': BLACK,
        'stroke_opacity': 1.0,
        'stroke_width': 2.0,
        'joint_type': LineJointType.ROUND,
    }
    cube_spec: PuzzleCubeSpec
    puzzle_cube: PuzzleCube

    def __init__(self,
                 projection: Projection,
                 cube_spec: PuzzleCubeSpec,
                 **kwargs) -> None:
        """
        Args:
            projection: the projection.
            cube_spec: the puzzle cube specification.
        """
        self.cube_spec = cube_spec
        self.puzzle_cube = PuzzleCube(cube_spec)
        id_to_model_path_0: PolygonIdToVertexPathMapping = ThreeDPuzzleCube.mk_id_to_model_path_0()

        super().__init__(projection, id_to_model_path_0, **kwargs)

    @staticmethod
    def name_to_id(face_name: FaceName) -> PolygonId:
        """
        Converts a face name to a polygon id.
        Args:
            face_name: the face name.

        Returns:
            the polygon id.
        """
        face_name_str: str = str(face_name.value)
        return PolygonId(face_name_str)

    @staticmethod
    def id_to_name(polygon_id: PolygonId) -> FaceName:
        """
        Converts a polygon id to a face name.

        Args:
            polygon_id: the polygon id.

        Returns:
            the face name.
        """
        return FaceName(polygon_id)

    @staticmethod
    def mk_id_to_model_path_0() -> PolygonIdToVertexPathMapping:
        """
        Makes the initial model space vertex paths.
        Returns:
            the initial model space vertex paths.
        """
        face_name: FaceName
        vertex_path: VertexPath
        id_to_model_path_0: PolygonIdToVertexPathMapping = {
            ThreeDPuzzleCube.name_to_id(face_name): vertex_path
            for face_name, vertex_path in FACE_NAME_TO_VERTEX_PATH.items()
        }
        return id_to_model_path_0

    def get_colour_name(self, face_name: FaceName) -> FaceColour:
        """
        Returns the colour name for the given face colour.
        Args:
            face_name: the face name.

        Returns:
            the colour name for the given face name.
        """
        colour_name: FaceColour = self.puzzle_cube.name_to_colour[face_name]
        return colour_name

    def get_manim_colour(self, face_name: FaceName) -> ManimColor:
        """
        Returns the colour of the given face.
        Args:
            face_name: The name of the face.

        Returns:
            The Manim colour of the given face.
        """
        colour_name: FaceColour = self.get_colour_name(face_name)
        colour: ManimColor = MANIM_COLOUR_MAP[colour_name]
        return colour

    def update_polygons(self,
                        id_to_model_path: PolygonIdToVertexPathMapping,
                        **polygon_settings) -> None:
        """
        Makes the scene space polygons from the model space vertices and adds them to the group.

        Project the model space vertices onto scene space and then depth-sort them.
        Convert the projected vertices to Polygon objects and store them in a new OrderedDict.
        Add the polygons to the base VGroup in the depth-sorted order.

        Args:
            id_to_model_path: the dict of model space vertex paths of the faces.
        """
        super().update_polygons(id_to_model_path, **self.polygon_settings)

        # update the fill colour for each face
        polygon_id: PolygonId
        polygon: Polygon
        for polygon_id, polygon in self.id_to_scene_polygon.items():
            face_name: FaceName = self.id_to_name(polygon_id)
            colour: ManimColor = self.get_manim_colour(face_name)
            polygon.set_fill(colour)
