from typing import OrderedDict
import numpy as np

from manim import Polygon, ManimColor, BLACK, GREEN, BLUE, Scene, Animation, ORIGIN, LEFT, tempconfig, Vector

from instant_insanity.core.geometry_types import (Vertex, VertexPath, PolygonId, PolygonIdToVertexPathMapping,
                                                  SortedPolygonIdToVertexPathMapping, SortedPolygonIdToPolygonMapping)
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FaceName, FACE_NAME_TO_VERTEX_PATH
from instant_insanity.core.depth_sort import DepthSort
from instant_insanity.core.projection import Projection, PerspectiveProjection
from instant_insanity.core.puzzle import PuzzleCubeSpec, PuzzleCube, FaceColour
from instant_insanity.core.transformation import transform_vertex_path
from instant_insanity.manim_scenes.coloured_cube import TEST_PUZZLE_CUBE_SPEC, MANIM_COLOUR_MAP
from instant_insanity.manim_scenes.graph_theory.three_d_polygons import TrackedVGroup, ThreeDPolygons
from instant_insanity.manim_scenes.coordinate_grid import GridMixin


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
    name_to_initial_model_path: dict[FaceName, VertexPath]
    name_to_scene_polygon: OrderedDict[FaceName, Polygon]

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

        self.name_to_initial_model_path = FACE_NAME_TO_VERTEX_PATH.copy()
        self.mk_polygons(self.name_to_initial_model_path)

    @staticmethod
    def name_to_id(face_name: FaceName) -> PolygonId:
        return PolygonId(face_name.value)

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

    def mk_polygons(self, name_to_model_path: dict[FaceName, VertexPath]) -> None:
        """
        Makes the scene space polygons from the model space vertices and adds them to the group.

        The model space vertices are projected onto scene space and then depth-sorted.
        The projected vertices are converted to Polygon objects and stored in a new OrderedDict.
        The polygons are added to the VGroup in the depth-sorted order.

        Args:
            name_to_model_path: the dict of model space vertex paths of the faces
        """

        # convert the FaceName keys of model_vertices to str.
        name: FaceName
        model_path: VertexPath
        id_to_model_path: PolygonIdToVertexPathMapping = {
            ThreeDPuzzleCube.name_to_id(name) : model_path
            for name, model_path in name_to_model_path.items()
        }

        # project the transformed vertices onto the scene and depth-sort them
        id_to_scene_path: SortedPolygonIdToVertexPathMapping = self.depth_sorter.depth_sort(id_to_model_path)

        # we are going to create new Polygons so remove any that are present in the group
        self.remove(*self.submobjects)

        # store the new Polygons in an OrderedDict
        name_to_scene_polygon: OrderedDict[FaceName, Polygon] = OrderedDict()

        # create and add a new Manim Polygon for each projected face of the cube
        polygon_id: PolygonId
        for polygon_id in id_to_scene_path.keys():
            # create a Manim Polygon
            name = ThreeDPuzzleCube.id_to_name(polygon_id)
            colour: ManimColor = self.get_manim_colour(name)
            polygon: Polygon = Polygon(
                *id_to_scene_path[polygon_id],
                fill_color=colour,
                fill_opacity=1.0,
                stroke_color=BLACK,
                stroke_width=1.0
            )
            self.add(polygon)
            name_to_scene_polygon[name] = polygon

        self.name_to_scene_polygon = name_to_scene_polygon


class CubeRigidMotionAnimation(Animation):
    """
    This class animates a rigid motion of a 3D puzzle cube.

    Attributes:
        rotation: the rotation vector.
        translation: the translation vector.
    """

    rotation: Vector
    translation: Vector

    def __init__(self,
                 cube: ThreeDPuzzleCube,
                 rotation: Vector,
                 translation: Vector,
                 **kwargs) -> None:
        super().__init__(cube, **kwargs)
        self.rotation = rotation
        self.translation = translation

    def interpolate_mobject(self, alpha: float) -> None:
        assert isinstance(self.mobject, ThreeDPuzzleCube)
        cube: ThreeDPuzzleCube = self.mobject
        alpha_rotation: Vector = alpha * self.rotation
        alpha_translation: Vector = alpha * self.translation
        name_to_model_vertex_path: dict[FaceName, VertexPath] = {
            name: transform_vertex_path(alpha_rotation,
                                        alpha_translation,
                                        cube.name_to_initial_model_path[name])
            for name in FaceName
        }
        cube.mk_polygons(name_to_model_vertex_path)


class TestThreeDPuzzleCube(GridMixin, Scene):
    def construct(self):

        # this grid confirms that the (x,y) coordinates are faithfully mapped to the frame
        self.add_grid(True)

        # these dots confirm that the z-component of points is ignored
        # diagonal = RIGHT + UP - OUT
        # red_dot = Dot(1.0 * diagonal, color=RED)
        # blue_dot = Dot(2.0 * diagonal, color=BLUE)
        # green_dot = Dot(3.0 * diagonal, color=GREEN)
        # self.add(red_dot, blue_dot, green_dot)

        # these hard-coded values are for camera_z = 2 and viewpoint = (0, 0, 6)
        # actual_right_after: np.ndarray = np.array([
        #     [-4.8, 0.8, -1.57480157],
        #     [-3.42857143, 0.57142857, -3.97440793],
        #     [-3.42857143, -0.57142857, -3.97440793],
        #     [-4.8, -0.8, -1.57480157]])
        #
        # polygon : Polygon = Polygon(*actual_right_after, color=RED)
        # self.add(polygon)
        # self.wait(4.0)


        # create a projection
        camera_z: float = 8.0
        viewpoint: np.ndarray = np.array([5, 5, 20], dtype=np.float64)
        projection: Projection = PerspectiveProjection(viewpoint, camera_z=camera_z)

        # use the colours from the test cube
        cube_spec: PuzzleCubeSpec = TEST_PUZZLE_CUBE_SPEC
        three_d_puzzle_cube: ThreeDPuzzleCube = ThreeDPuzzleCube(projection, cube_spec)

        # grab the initial front and right faces
        initial_front_polygon: Polygon = three_d_puzzle_cube.name_to_scene_polygon[FaceName.FRONT]
        initial_front_vertices: np.ndarray = initial_front_polygon.get_vertices()
        initial_front_polygon_outline: Polygon = Polygon(*initial_front_vertices, color=BLUE)
        self.add(initial_front_polygon_outline)

        initial_right_polygon: Polygon = three_d_puzzle_cube.name_to_scene_polygon[FaceName.RIGHT]
        initial_right_vertices: np.ndarray = initial_right_polygon.get_vertices()
        initial_right_polygon_outline: Polygon = Polygon(*initial_right_vertices, color=GREEN)
        self.add(initial_right_polygon_outline)

        # set up the rigid motion animation
        rotation: Vector = ORIGIN
        translation: Vector = 7 * LEFT  # + DOWN
        animation: CubeRigidMotionAnimation = CubeRigidMotionAnimation(three_d_puzzle_cube, rotation, translation)

        # move the cube to the animation midpoint
        animation.interpolate_mobject(0.5)

        # grab the midpoint front and right faces
        mid_front_polygon: Polygon = three_d_puzzle_cube.name_to_scene_polygon[FaceName.FRONT]
        mid_front_vertices: np.ndarray = mid_front_polygon.get_vertices()
        mid_front_polygon_outline: Polygon = Polygon(*mid_front_vertices, color=BLUE)
        self.add(mid_front_polygon_outline)

        mid_right_polygon: Polygon = three_d_puzzle_cube.name_to_scene_polygon[FaceName.RIGHT]
        mid_right_vertices: np.ndarray = mid_right_polygon.get_vertices()
        mid_right_polygon_outline: Polygon = Polygon(*mid_right_vertices, color=GREEN)
        self.add(mid_right_polygon_outline)

        # move the cube to the animation final point
        animation.interpolate_mobject(1.0)

        # grab the final front and right faces
        final_front_polygon: Polygon = three_d_puzzle_cube.name_to_scene_polygon[FaceName.FRONT]
        final_front_vertices: np.ndarray = final_front_polygon.get_vertices()
        final_front_polygon_outline: Polygon = Polygon(*final_front_vertices, color=BLUE)
        self.add(final_front_polygon_outline)

        final_right_polygon: Polygon = three_d_puzzle_cube.name_to_scene_polygon[FaceName.RIGHT]
        final_right_vertices: np.ndarray = final_right_polygon.get_vertices()
        final_right_polygon_outline: Polygon = Polygon(*final_right_vertices, color=GREEN)
        self.add(final_right_polygon_outline)

        self.wait(1.0)

        # move the cube to the animation start
        animation.interpolate_mobject(0.0)
        self.add(three_d_puzzle_cube)
        self.wait(1.0)

        #self.remove(three_d_puzzle_cube)
        three_d_puzzle_cube.remove(*three_d_puzzle_cube.submobjects)
        self.wait(1.0)

        # animate movement of the cube to the left
        self.play(animation, run_time=3.0)
        self.wait(1.0)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = TestThreeDPuzzleCube()
        scene.render()
