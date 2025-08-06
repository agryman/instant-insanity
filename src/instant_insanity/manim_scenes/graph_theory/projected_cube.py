"""
This scene displays a projected cube.
The cube is first constructed in 3D model space where it may be
rotated, translated, unfolded, exploded, or otherwise animated.
The result is a set of 3D, convex, planar polygons.
This set is then projected onto the 2D scene space.
Next, the polygons are sorted into the correct depth order
so that when they are drawn, those in front will be drawn
after those behind.
Finally, the polygons are converted into Manim Polygons
and added to the scene.
"""
import math
from typing import Any, Callable, Iterable, TypeAlias
from abc import ABC, abstractmethod

import numpy as np
from scipy.spatial.transform import Rotation as R
from manim import *

from instant_insanity.core.config import STANDARD_CONFIG, ALTERNATE_CONFIG
from instant_insanity.core.cube import FaceName, FACE_NAME_TO_VERTICES, FACE_NAME_TO_UNIT_NORMAL, RBF, RTF, LTF, LBF
from instant_insanity.core.depth_sort import DepthSort
from instant_insanity.core.projection import Projection, PerspectiveProjection, OrthographicProjection
from instant_insanity.core.puzzle import PuzzleCubeSpec, PuzzleCube, FaceColour, WINNING_MOVES_PUZZLE
from instant_insanity.core.rotation_about_axis import rotation_matrix_about_line, apply_linear_transform
from instant_insanity.manim_scenes.coloured_cube import TEST_PUZZLE_CUBE_SPEC, MANIM_COLOUR_MAP

class TrackedVGroup(VGroup):
    """
    This class is a VGroup with a ValueTracker.

    Attributes:
        tracker: the ValueTracker
        sorted_name_keys: the list of polygon names in depth-sorted order
    """
    tracker: ValueTracker
    sorted_name_keys: list[str]

    def __init__(self, sorted_name_keys: list[str], *vmobjects: list[VMobject], **kwargs: Any) -> None:
        super().__init__(*vmobjects, **kwargs)
        self.sorted_name_keys = sorted_name_keys
        self.tracker = ValueTracker(0.0)


TrackedVGroupUpdater: TypeAlias = Callable[[TrackedVGroup], object]


def transform_vertices(rotation, translation, vertices) -> np.ndarray:
    """
    Transform the vertices by applying a rotation followed by a translation.

    Let R be a rotation, let T be a translation, and let V be a vertex.
    The transformed vertex is R(V) + T.

    Args:
        rotation: a rotation 3-vector.
        translation: a translation 3-vector.
        vertices: a matrix of n 3-vectors.

    Returns:
        the matrix of n transformed 3-vectors.
    """
    rot = R.from_rotvec(rotation)
    return rot.apply(vertices) + translation


class CubeAnimation(ABC):
    """
    This class models a cube animation.
    The frames of the animation are parameterized by the real number alpha
    which ranges from 0 to 1 inclusive.

    Attributes:
        cube_spec: a cube face colour specification
        projection: a projection from model space to scene space
        puzzle_cube: the puzzle cube defined by the cube specification
        depth_sorter: the polygon depth sorter for the projection
    """
    cube_spec: PuzzleCubeSpec
    projection: Projection
    puzzle_cube: PuzzleCube
    depth_sorter: DepthSort

    def __init__(self,
                 cube_spec: PuzzleCubeSpec,
                 projection: Projection) -> None:
        """
        Args:
            projection: the perspective projection
            cube_spec: the cube face colour specification
        """
        self.cube_spec = cube_spec
        self.projection = projection
        self.puzzle_cube = PuzzleCube(cube_spec)
        self.depth_sorter = DepthSort(projection)

    @abstractmethod
    def mk_face_vertices(self, name: FaceName, alpha: float = 0.0) -> np.ndarray:
        """
        Makes the NumPy array of face vertices corresponding to animation parameter alpha.

        Args:
            name: the face name
            alpha: the animation parameter

        Returns:
            the NumPy array of face vertices
        """
        pass

    def mk_polygons(self, alpha: float) -> tuple[list[str], list[Polygon]]:
        """
        Make the cube corresponding the value of alpha in the animation.

        Args:
            alpha: the frame parameter which ranges from 0 to 1

        Returns:
            (sorted_name_keys, polygon_list) where both lists are in the depth-sorted order.
        """
        # create a dict of the transformed vertices
        transformed_vertices_dict: dict[str, np.ndarray] = {}
        name: FaceName
        name_key: str
        for name in FaceName:
            transformed_vertices: np.ndarray = self.mk_face_vertices(name, alpha)
            name_key = str(name.value)
            transformed_vertices_dict[name_key] = transformed_vertices

        # project the transformed vertices onto the scene and depth-sort them
        sorted_name_keys: list[str]
        scene_vertices_dict: dict[str, np.ndarray]
        sorted_name_keys, scene_vertices_dict = self.depth_sorter.depth_sort(transformed_vertices_dict)

        # create a Manim Polygon for each projected face of the cube
        polygon_list: list[Polygon] = []
        for name_key in sorted_name_keys:
            # create a Manim Polygon
            scene_vertices: np.ndarray = scene_vertices_dict[name_key]
            name = FaceName(name_key)
            colour_name: FaceColour = self.puzzle_cube.faces[name]
            colour: ManimColor = MANIM_COLOUR_MAP[colour_name]
            polygon: Polygon = Polygon(
                *scene_vertices,
                fill_color=colour,
                fill_opacity=1.0,
                stroke_color=BLACK,
                stroke_width=1.0
            )
            polygon_list.append(polygon)

        return sorted_name_keys, polygon_list

    def mk_updater(self) -> TrackedVGroupUpdater:
        """
        Make a nontime-based updater function for the animation.

        Returns:
            An updater for the animation.
        """

        def updater(tracked_vgroup: TrackedVGroup) -> TrackedVGroup:
            """
            Updates the polygons in the TrackedVGroup to its current alpha parameter.

            Args:
                tracked_vgroup: a TrackedVGroup of Polygons for this animation.

            Returns:
                the TrackedVGroup.
            """
            if not isinstance(tracked_vgroup, TrackedVGroup):
                raise ValueError('expected a TrackedVGroup')
            tracked_vgroup.remove(*tracked_vgroup.submobjects)
            tracker: ValueTracker = tracked_vgroup.tracker
            alpha: float = tracker.get_value()
            sorted_name_keys: list[str]
            polygon_list: list[Polygon]
            sorted_name_keys, polygon_list = self.mk_polygons(alpha)
            tracked_vgroup.sorted_name_keys = sorted_name_keys
            tracked_vgroup.add(*polygon_list)
            return tracked_vgroup

        return updater


class CubeRigidMotion(CubeAnimation):
    """
    The class animates a rigid motion of a cube.
    The rigid motion is defined by a rotation followed by a translation.

    Attributes:
        rotation: the rotation vector.
        translation: the translation vector.
    """

    rotation: np.ndarray
    translation: np.ndarray

    def __init__(self,
                 cube_spec: PuzzleCubeSpec,
                 projection: Projection,
                 rotation: np.ndarray,
                 translation: np.ndarray,
                 ) -> None:
        super().__init__(cube_spec, projection)
        self.rotation = rotation
        self.translation = translation

    def mk_face_vertices(self, name: FaceName, alpha: float = 0.0) -> np.ndarray:
        """
        Makes the NumPy array of face vertices corresponding to animation parameter alpha.

        Args:
            name: the face name
            alpha: the animation parameter

        Returns:
            the NumPy array of face vertices
        """
        alpha_rotation: np.ndarray = alpha * self.rotation
        alpha_translation: np.ndarray = alpha * self.translation
        model_vertices: np.ndarray = FACE_NAME_TO_VERTICES[name]
        transformed_vertices: np.ndarray = transform_vertices(alpha_rotation, alpha_translation, model_vertices)

        return transformed_vertices


class CubeExplosion(CubeAnimation):
    """
    This class animates an exploded view of a cube.
    The cube faces move outward without changing their size.

    Attributes:
        expansion_factor: the final size multiplier > 1.
    """

    expansion_factor: float

    def __init__(self,
                 cube_spec: PuzzleCubeSpec,
                 projection: Projection,
                 expansion_factor: float
                 ) -> None:
        if expansion_factor <= 1.0:
            raise ValueError(f'expansion_factor must be > 1.0. actual: {expansion_factor}')
        super().__init__(cube_spec, projection)
        self.expansion_factor = expansion_factor

    def mk_face_vertices(self, name: FaceName, alpha: float = 0.0) -> np.ndarray:
        """
        Makes the NumPy array of face vertices corresponding to animation parameter alpha.

        The faces rotate to become perpendicular to the z-axis.
        Front/Back faces are already perpendicular to the z-axis so no rotation.
        Right/Left faces rotate about the y-axis by plus/minus 90 degrees.
        Top/Bottom faces rotate about the x-axis by plus/minus 90 degrees.

        The faces move outward in the direction of their normals.

        Args:
            name: the face name
            alpha: the animation parameter

        Returns:
            the NumPy array of face vertices
        """

        origin: np.ndarray = np.zeros(3, dtype=np.float64)
        unit_i: np.ndarray = np.array([1, 0, 0], dtype=np.float64)
        unit_j: np.ndarray = np.array([0, 1, 0], dtype=np.float64)
        unit_k: np.ndarray = np.array([0, 0, 1], dtype=np.float64)
        quarter_turn: float = np.pi / 2.0

        # compute the point p, unit vector u, and angle theta that define a rotation about a line
        p: np.ndarray = origin
        u: np.ndarray = unit_k
        theta_max: float = 0.0
        z_max: float = -(3.0 + self.expansion_factor) / 2.0
        face_normal: np.ndarray = FACE_NAME_TO_UNIT_NORMAL[name]
        translation_max: np.ndarray = z_max * unit_k + (self.expansion_factor - 1.0) * face_normal

        match name:
            case FaceName.RIGHT:
                p = RBF
                u = unit_j
                theta_max = -quarter_turn
            case FaceName.LEFT:
                p = LBF
                u = unit_j
                theta_max = quarter_turn
            case FaceName.TOP:
                p = LTF
                u = unit_i
                theta_max = quarter_turn
            case FaceName.BOTTOM:
                p = LBF
                u = unit_i
                theta_max = -quarter_turn
            case FaceName.FRONT:
                translation_max = origin
            case FaceName.BACK:
                translation_max = -(self.expansion_factor - 1.0) * unit_k

        theta: float = alpha * theta_max
        rot_mat: np.ndarray = rotation_matrix_about_line(p, u, theta)
        model_vertices: np.ndarray = FACE_NAME_TO_VERTICES[name]
        rotated_vertices: np.ndarray = apply_linear_transform(rot_mat, model_vertices)

        translation: np.ndarray = alpha * translation_max
        transformed_vertices: np.ndarray = rotated_vertices + translation

        return transformed_vertices


class ProjectedCube(Scene):
    def construct(self):
        projection: Projection
        camera_z: float = 2.0

        # create a perspective projection
        viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
        projection = PerspectiveProjection(camera_z, viewpoint)

        # create an orthographic projection
        # u: np.ndarray = np.array([0.5, 0.5, 4], dtype=np.float64)
        # u = u / np.linalg.norm(u)
        # projection = OrthographicProjection(camera_z, u)

        # use the colours from the test cube
        cube_spec: PuzzleCubeSpec = WINNING_MOVES_PUZZLE[0]

        # rotation: np.ndarray = np.array([1.0, 0.0, 0.0], dtype=np.float64) * 2.0 * np.pi
        # translation: np.ndarray = np.array([-2, 3, -4], dtype=np.float64)
        # cube_animation: CubeAnimation = CubeRigidMotion(cube_spec, projection, rotation, translation)

        expansion_factor: float = 2.0
        cube_animation: CubeAnimation = CubeExplosion(cube_spec, projection, expansion_factor)

        # we are going to create new list of polygon mobjects during each frame of the animation
        # so put them in a TrackedVGroup which will be updated for each frame
        sorted_name_keys: list[str]
        polygon_list: list[Polygon]
        sorted_name_keys, polygon_list= cube_animation.mk_polygons(0.0)

        # the tracker parameterizes the animation
        tracked_vgroup: TrackedVGroup = TrackedVGroup(sorted_name_keys, *polygon_list)
        self.add(tracked_vgroup)
        self.wait(1.0)

        tracked_vgroup.remove(*tracked_vgroup.submobjects)
        updater: TrackedVGroupUpdater = cube_animation.mk_updater()
        tracked_vgroup.add_updater(updater)
        tracker: ValueTracker = tracked_vgroup.tracker
        self.play(tracker.animate.set_value(1.0), run_time=4.0)
        tracked_vgroup.remove_updater(updater)

        self.wait(1.0)

        # animate movement of exploded cube to the left
        self.play(tracked_vgroup.animate.shift(4 * LEFT + DOWN), run_time=2.0)
        self.wait(4.0)

        # fade-in the vertices of the opposite-face graph

        # morph the front-back faces to dots and connect them with a graph edge
        # move the dots onto the graph, with the graph edge connected, label as x

        # repeat this for the left-right faces and the top-bottom faces, labelling as y and z

with tempconfig(ALTERNATE_CONFIG):
    scene = ProjectedCube()
    scene.render()
