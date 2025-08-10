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
from typing import Callable, TypeAlias
from abc import ABC, abstractmethod

from manim import *

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FaceName, FACE_NAME_TO_VERTICES, FACE_NAME_TO_UNIT_NORMAL, RBF, LTF, LBF
from instant_insanity.core.depth_sort import DepthSort
from instant_insanity.core.projection import Projection, PerspectiveProjection
from instant_insanity.core.puzzle import PuzzleCubeSpec, PuzzleCube, FaceColour, WINNING_MOVES_PUZZLE
from instant_insanity.core.transformation import rotation_matrix_about_line, apply_linear_transform, transform_vertices
from instant_insanity.manim_scenes.coloured_cube import MANIM_COLOUR_MAP
from instant_insanity.manim_scenes.coordinate_grid import add_coordinate_grid
from instant_insanity.manim_scenes.graph_theory.opposite_face_graph import OppositeFaceGraph, WINNING_MOVES_NODE_LAYOUT
from instant_insanity.manim_scenes.graph_theory.three_d_puzzle_cube import ThreeDPuzzleCube, TrackedVGroup

Updater: TypeAlias = Callable[[Mobject], object]


class CubeAnimator(ABC):
    """
    This is the abstract base class for cube animators.

    Attributes:
        cube: the cube to animate
    """
    cube: ThreeDPuzzleCube

    def __init__(self, cube: ThreeDPuzzleCube):
        self.cube = cube

    @abstractmethod
    def interpolate(self, alpha: float) -> None:
        pass

    def mk_updater(self) -> Updater:
        """
        Make a nontime-based updater function for the animation.

        Returns:
            An updater for the animation.
        """

        def updater(mobj: Mobject) -> object:
            """
            Updates the cube to its current alpha parameter.

            Args:
                mobj: the cube that is being animated.

            Returns:
                the cube.
            """
            if not isinstance(mobj, ThreeDPuzzleCube):
                raise ValueError('expected a ThreeDPuzzleCube')
            cube: ThreeDPuzzleCube = mobj
            cube.remove(*cube.submobjects)
            tracker: ValueTracker = cube.tracker
            alpha: float = tracker.get_value()
            self.interpolate(alpha)
            return cube

        return updater


class CubeRigidMotionAnimator(CubeAnimator):
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
                 cube: ThreeDPuzzleCube,
                 rotation: np.ndarray,
                 translation: np.ndarray,
                 ) -> None:
        super().__init__(cube)
        self.rotation = rotation
        self.translation = translation

    def interpolate(self, alpha: float) -> None:
        alpha_rotation: np.ndarray = alpha * self.rotation
        alpha_translation: np.ndarray = alpha * self.translation
        initial_vertices: dict[FaceName, np.ndarray] = self.cube.initial_model_vertices
        transformed_vertices: dict[FaceName, np.ndarray] = {
            name: transform_vertices(alpha_rotation, alpha_translation, initial_vertices[name])
            for name in FaceName
        }
        self.cube.mk_polygons(transformed_vertices)


class CubeExplosionAnimator(CubeAnimator):
    def __init__(self, cube: ThreeDPuzzleCube, expansion_factor: float) -> None:
        super().__init__(cube)
        self.expansion_factor = expansion_factor

    def interpolate_face(self, name: FaceName, alpha: float = 0.0) -> np.ndarray:
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

    def interpolate(self, alpha: float) -> None:
        transformed_vertices = {
            name: self.interpolate_face(name, alpha)
            for name in FaceName
        }
        self.cube.mk_polygons(transformed_vertices)


class ConstructGraph(Scene):
    def construct(self):
        add_coordinate_grid(self)

        # create a projection
        camera_z: float = 2.0
        viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
        # camera_z: float = 8.0
        # viewpoint: np.ndarray = np.array([5, 5, 20], dtype=np.float64)
        projection: Projection = PerspectiveProjection(camera_z, viewpoint)

        # create the cube object
        cube_spec: PuzzleCubeSpec = WINNING_MOVES_PUZZLE[0]
        cube: ThreeDPuzzleCube = ThreeDPuzzleCube(projection, cube_spec)
        self.add(cube)
        self.wait(1.0)
        # self.remove(cube)
        # self.wait(1.0)

        # animate cube rigid motion
        # rotation: np.ndarray = ORIGIN
        # translation: np.ndarray = 7 * LEFT #+ DOWN
        # animator: CubeAnimator = CubeRigidMotionAnimator(cube, rotation, translation)

        # animate cube explosion
        expansion_factor: float = 2.0
        animator: CubeAnimator = CubeExplosionAnimator(cube, expansion_factor)

        cube.remove(*cube.submobjects)
        updater: Updater = animator.mk_updater()
        cube.add_updater(updater)
        tracker: ValueTracker = cube.tracker
        alpha_1: float = 1.0
        self.play(tracker.animate.set_value(alpha_1), run_time=4.0)
        cube.remove_updater(updater)
        self.wait(1.0)

        # animate movement of exploded cube to the left
        cube_shift: np.ndarray = 4 * LEFT + DOWN
        self.play(cube.animate.shift(cube_shift), run_time=1.0)
        self.wait(1.0)

        # fade-in the nodes of the opposite-face graph
        graph: VGroup = OppositeFaceGraph(3 * RIGHT, WINNING_MOVES_NODE_LAYOUT)
        self.play(FadeIn(graph))
        self.wait(1.0)

        # create same-coloured dots at the centroids of the face polygons
        name: FaceName
        polygon: Polygon
        dot_dict: dict[FaceName, Dot] = {}
        for name, polygon in cube.polygon_dict.items():
            vertices: np.ndarray = polygon.get_vertices()
            centroid: np.ndarray = np.mean(vertices, axis=0)
            colour: FaceColour = cube.get_colour_name(name)
            dot: Dot = graph.mk_dot(colour, centroid)
            dot_dict[name] = dot

        # TODO:
        # morph the front-back faces to dots
        front_polygon: Polygon = cube.polygon_dict[FaceName.FRONT]
        front_dot: Dot = dot_dict[FaceName.FRONT]
        radius: float = front_dot.radius
        back_polygon: Polygon = cube.polygon_dict[FaceName.BACK]
        back_dot: Dot = dot_dict[FaceName.BACK]
        self.play(Transform(front_polygon, front_dot), Transform(back_polygon, back_dot), run_time=2.0)

        # Fade in the line
        # Compute boundary points
        vec = back_polygon.get_center() - front_polygon.get_center()
        vec[2] = 0.0
        unit_vec = vec / np.linalg.norm(vec)

        start_point = front_polygon.get_center() + unit_vec * radius
        end_point = back_polygon.get_center() - unit_vec * radius

        # Line connecting edges of the dots
        line = Line(start_point, end_point, color=BLACK)
        self.play(FadeIn(line))
        self.wait(4.0)

        # connect the front-back dots with a graph edge
        # move the dots onto the graph, with the graph edge connected, label as x

        # repeat this for the left-right faces and the top-bottom faces, labelling as y and z


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = ConstructGraph()
        scene.render()
