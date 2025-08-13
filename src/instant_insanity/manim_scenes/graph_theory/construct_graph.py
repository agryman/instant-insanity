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
from dataclasses import dataclass

from manim import *

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FaceName, FACE_NAME_TO_VERTICES, FACE_NAME_TO_UNIT_NORMAL, RBF, LTF, LBF
from instant_insanity.core.projection import Projection, PerspectiveProjection
from instant_insanity.core.puzzle import (Puzzle, PuzzleCubeSpec, FaceColour, WINNING_MOVES_PUZZLE_SPEC,
                                          PuzzleCubeNumber, PuzzleCube, CubeAxis, AxisLabel)
from instant_insanity.core.transformation import rotation_matrix_about_line, apply_linear_transform, transform_vertices
from instant_insanity.manim_scenes.coordinate_grid import add_coordinate_grid
from instant_insanity.manim_scenes.graph_theory.labelled_edge import LabelledEdge, mk_cubic_bezier
from instant_insanity.manim_scenes.graph_theory.opposite_face_graph import OppositeFaceGraph
from instant_insanity.manim_scenes.graph_theory.coloured_node import mk_dot
from instant_insanity.manim_scenes.graph_theory.quadrant import Quadrant
from instant_insanity.manim_scenes.graph_theory.three_d_puzzle_cube import ThreeDPuzzleCube

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

@dataclass
class FaceData:
    colour: FaceColour
    quadrant: Quadrant
    polygon: Polygon
    dot: Dot

class ConstructGraph(Scene):
    """
    This scene animates the construction of the opposite-face graph of a puzzle.
    Each cube of the puzzle is exploded into opposite-face pairs.
    Each opposite-face pair is morphed into an edge and added to the graph.

    Attributes:
        puzzle: the puzzle being transformed into its opposite-face graph.
        cube_number: the number of the cube currently being animated.
        cube: the 3D projection of the cube currently being animated.
        axis_label: the label of the axis of the cube currently being animated.
        cube_axis: the axis of the cube currently being animated.
        graph: the opposite-face graph being constructed.
    """
    puzzle: Puzzle
    cube_number: PuzzleCubeNumber | None
    cube: ThreeDPuzzleCube | None
    axis_label: AxisLabel | None
    cube_axis: CubeAxis | None
    graph: OppositeFaceGraph | None

    def setup(self):
        self.puzzle = Puzzle(WINNING_MOVES_PUZZLE_SPEC)
        self.cube_number = None
        self.cube = None
        self.axis_label = None
        self.cube_axis = None
        self.graph = None

    def add_grid(self, show: bool) -> None:
        """
        Adds a coordinate grid to aid in designing the scene.

        Args:
            show: whether to show the grid.
        """
        if show:
            add_coordinate_grid(self)

    def add_cube(self, cube_number: PuzzleCubeNumber = PuzzleCubeNumber.ONE) -> None:
        """
        Adds a puzzle cube to the scene.
        """
        # create a projection
        camera_z: float = 2.0
        viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
        # camera_z: float = 8.0
        # viewpoint: np.ndarray = np.array([5, 5, 20], dtype=np.float64)
        projection: Projection = PerspectiveProjection(viewpoint, camera_z=camera_z)

        # create the cube object
        puzzle_cube: PuzzleCube = self.puzzle.number_to_cube[cube_number]
        cube_spec: PuzzleCubeSpec = puzzle_cube.cube_spec
        cube: ThreeDPuzzleCube = ThreeDPuzzleCube(projection, cube_spec)

        # find the scene coordinates of the centre of the front face
        front_face: Polygon = cube.polygon_dict[FaceName.FRONT]
        centre: np.ndarray = front_face.get_center()
        scene_x: float = float(centre[0])
        scene_y: float = float(centre[1])

        # recreate the cube centered in the scene
        projection = PerspectiveProjection(viewpoint, scene_x=scene_x, scene_y=scene_y, camera_z=camera_z)
        cube = ThreeDPuzzleCube(projection, cube_spec)

        self.cube_number = cube_number
        self.cube = cube
        self.add(cube)

    def animate_cube_explosion(self) -> None:
        # animate cube rigid motion
        # rotation: np.ndarray = ORIGIN
        # translation: np.ndarray = 7 * LEFT #+ DOWN
        # animator: CubeAnimator = CubeRigidMotionAnimator(cube, rotation, translation)

        # animate cube explosion
        expansion_factor: float = 2.0
        animator: CubeAnimator = CubeExplosionAnimator(self.cube, expansion_factor)

        self.cube.remove(*self.cube.submobjects)
        updater: Updater = animator.mk_updater()
        self.cube.add_updater(updater)
        tracker: ValueTracker = self.cube.tracker
        alpha_1: float = 1.0
        self.play(tracker.animate.set_value(alpha_1), run_time=4.0)
        self.cube.remove_updater(updater)

    def get_face_data(self, name: FaceName) -> FaceData:
        colour: FaceColour = self.cube.get_colour_name(name)
        quadrant: Quadrant = self.graph.colour_to_node[colour]
        polygon: Polygon = self.cube.polygon_dict[name]
        vertices: np.ndarray = polygon.get_vertices()
        centroid: np.ndarray = np.mean(vertices, axis=0)
        dot: Dot = mk_dot(colour, centroid)
        return FaceData(colour, quadrant, polygon, dot)

    def construct(self):
        self.add_grid(False)

        self.add_cube(PuzzleCubeNumber.ONE)
        self.wait()

        self.animate_cube_explosion()

        # animate movement of exploded cube to the left
        cube_shift: np.ndarray = 3 * LEFT
        self.play(self.cube.animate.shift(cube_shift), run_time=1.0)

        # fade-in the nodes of the empty opposite-face graph
        self.graph = OppositeFaceGraph(self.puzzle, 3 * RIGHT)
        self.play(FadeIn(self.graph))

        # create same-coloured dots at the centroids of the face polygons
        # face_name: FaceName
        # polygon: Polygon
        # face_name_to_dot: dict[FaceName, Dot] = {}
        # for face_name, polygon in self.cube.polygon_dict.items():
        #     vertices: np.ndarray = polygon.get_vertices()
        #     centroid: np.ndarray = np.mean(vertices, axis=0)
        #     colour: FaceColour = self.cube.get_colour_name(face_name)
        #     dot: Dot = mk_dot(colour, centroid)
        #     face_name_to_dot[face_name] = dot

        # morph the front-back faces to the corresponding dots
        front: FaceData = self.get_face_data(FaceName.FRONT)
        back: FaceData = self.get_face_data(FaceName.BACK)

        # compute the start and end nodes to match the order in the graph
        start: FaceData
        end: FaceData
        if front.quadrant <= back.quadrant:
            start, end = front, back
        else:
            start, end = back, front

        self.play(Transform(start.polygon, start.dot),
                  Transform(end.polygon, end.dot), run_time=2.0)

        # connect the start-end dots with a graph edge
        # Compute boundary points
        vec: np.ndarray = end.polygon.get_center() - start.polygon.get_center()
        vec[2] = 0.0
        unit_vec: np.ndarray = vec / np.linalg.norm(vec)

        # rather than move the dots and update the line, move the line and update the dots
        radius: float = 0.0 #start.dot.radius
        start_point: np.ndarray = start.polygon.get_center() + unit_vec * radius
        end_point: np.ndarray = end.polygon.get_center() - unit_vec * radius
        length: float = float(np.linalg.norm(end_point - start_point))
        delta: np.ndarray = (length / 3.0) * unit_vec
        start_handle: np.ndarray = start_point + delta
        end_handle: np.ndarray = end_point - delta
        curve: CubicBezier = mk_cubic_bezier(start_point,
                                             start_handle,
                                             end_handle,
                                             end_point)
        self.remove(start.polygon, end.polygon)
        self.add(curve, start.polygon, end.polygon)
        self.play(FadeIn(curve))

        # rather than move the dots and update the line, move the line and update the dots
        start_moving_dot = always_redraw(lambda: mk_dot(start.colour, curve.get_start()))
        end_moving_dot = always_redraw(lambda: mk_dot(end.colour, curve.get_end()))
        self.remove(start.polygon, end.polygon)
        self.add(start_moving_dot, end_moving_dot)

        axis_label: AxisLabel = AxisLabel.X
        cube_axis: CubeAxis = (self.cube_number, axis_label)
        target_labelled_edge: LabelledEdge = self.graph.edge_to_mobject[cube_axis]
        target_curve: CubicBezier = target_labelled_edge.curve
        self.play(Transform(curve, target_curve), run_time=2.0)
        # remove the moving curve and dots
        self.remove(curve, start_moving_dot, end_moving_dot)
        # add the edge to the subgraph
        self.graph.set_subgraph_edge(cube_axis, True)
        self.wait()

        # repeat this for the left-right faces and the top-bottom faces, labelling as y and z


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = ConstructGraph()
        scene.render()
