from manim import ManimColor, WHITE, BLACK, Polygon, LineJointType

from instant_insanity.core.cube import FaceName, FACE_NAME_TO_VERTEX_PATH
from instant_insanity.core.geometry_types import PolygonIdToVertexPathMapping, PolygonId, VertexPath, \
    SortedPolygonIdToPolygonMapping
from instant_insanity.core.projection import Projection
from instant_insanity.core.puzzle import PuzzleCubeSpec, PuzzleCube, FaceColour
from instant_insanity.scenes.coloured_cube import MANIM_COLOUR_MAP
from instant_insanity.mobjects.three_d_polygons import ThreeDPolygons


class ThreeDPuzzleCube(ThreeDPolygons):
    """
    This class is a VGroup that renders as a 3D puzzle cube in model space.
    The appearance of the cube is determined by a projection from model space to scene space.
    Its submobjects are mobjects that render as the faces of the cube.
    The submobjects are depth-sorted to produce the correct 3D appearance.
    The faces are Polygons.

    """
    cube_spec: PuzzleCubeSpec
    puzzle_cube: PuzzleCube

    def __init__(self,
                 projection: Projection,
                 cube_spec: PuzzleCubeSpec,
                 **kwargs) -> None:
        """
        Args:
            projection: the projection
            cube_spec: the puzzle cube specification
        """
        id_to_initial_model_path: PolygonIdToVertexPathMapping = ThreeDPuzzleCube.mk_id_to_initial_model_path()
        super().__init__(projection, id_to_initial_model_path, **kwargs)

        self.cube_spec = cube_spec
        self.puzzle_cube = PuzzleCube(cube_spec)
        self.mk_polygons(id_to_initial_model_path)

    @staticmethod
    def name_to_id(face_name: FaceName) -> PolygonId:
        face_name_str: str = str(face_name.value)
        return PolygonId(face_name_str)

    @staticmethod
    def id_to_name(polygon_id: PolygonId) -> FaceName:
        return FaceName(polygon_id)

    @staticmethod
    def mk_id_to_initial_model_path() -> PolygonIdToVertexPathMapping:
        face_name: FaceName
        vertex_path: VertexPath
        id_to_initial_model_path: PolygonIdToVertexPathMapping = {
            ThreeDPuzzleCube.name_to_id(face_name): vertex_path
            for face_name, vertex_path in FACE_NAME_TO_VERTEX_PATH.items()
        }
        return id_to_initial_model_path

    def get_colour_name(self, name: FaceName) -> FaceColour:
        """
        Returns the colour name for the given face colour.
        Args:
            name: the face name.

        Returns:
            the colour name for the given face name.
        """
        colour_name: FaceColour = self.puzzle_cube.name_to_colour[name]
        return colour_name

    def get_manim_colour(self, name: FaceName) -> ManimColor:
        """
        Returns the colour of the given face.
        Args:
            name: The name of the face.

        Returns:
            The Manim colour of the given face.
        """
        colour_name: FaceColour = self.get_colour_name(name)
        colour: ManimColor = MANIM_COLOUR_MAP[colour_name]
        return colour

    def mk_polygons(self, id_to_model_path: PolygonIdToVertexPathMapping) -> None:
        """
        Makes the scene space polygons from the model space vertices and adds them to the group.

        The model space vertices are projected onto scene space and then depth-sorted.
        The projected vertices are converted to Polygon objects and stored in a new OrderedDict.
        The polygons are added to the VGroup in the depth-sorted order.

        Args:
            id_to_model_path: the dict of model space vertex paths of the faces
        """

        # remove any existing polygons because we are going to create new ones
        self.remove(*self.submobjects)

        # create new polygons for the given model vertex paths and default style attributes
        default_polygon_style: dict = {
            'fill_color': WHITE,
            'fill_opacity': 1.0,
            'stroke_color': BLACK,
            'stroke_opacity': 1.0,
            'stroke_width': 2.0,
            'joint_type': LineJointType.ROUND,
        }
        self.update_polygons(id_to_model_path, **default_polygon_style)

        # update the fill colour for each face then add the polygon to the scene
        id_to_scene_polygon: SortedPolygonIdToPolygonMapping = self.id_to_scene_polygon
        polygon_id: PolygonId
        polygon: Polygon
        for polygon_id, polygon in id_to_scene_polygon.items():
            name: FaceName = ThreeDPuzzleCube.id_to_name(polygon_id)
            colour: ManimColor = self.get_manim_colour(name)
            polygon.set_fill(colour)
            self.add(polygon)
