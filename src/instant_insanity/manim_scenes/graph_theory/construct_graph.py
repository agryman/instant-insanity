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

import numpy as np

from manim import (tempconfig, Mobject, ValueTracker, Polygon, Dot, Scene, LEFT, RIGHT, FadeIn, ReplacementTransform,
                   always_redraw, DOWN)

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FaceName, FACE_NAME_TO_VERTEX_PATH, FACE_NAME_TO_UNIT_NORMAL, RBF, LTF, LBF
from instant_insanity.core.force_ccw import force_ccw
from instant_insanity.core.geometry_types import VertexPath, Vector, Vertex
from instant_insanity.core.projection import Projection, PerspectiveProjection
from instant_insanity.core.puzzle import (PuzzleSpec, Puzzle, PuzzleCubeSpec, FaceColour, WINNING_MOVES_PUZZLE_SPEC,
                                          PuzzleCubeNumber, PuzzleCube, CubeAxis, AxisLabel, AXIS_TO_FACE_NAME_PAIR)
from instant_insanity.core.transformation import rotation_matrix_about_line, apply_linear_transform, transform_vertex_path
from instant_insanity.manim_scenes.coordinate_grid import GridMixin
from instant_insanity.manim_scenes.graph_theory.labelled_edge import LabelledEdge
from instant_insanity.manim_scenes.graph_theory.opposite_face_graph import OppositeFaceGraph
from instant_insanity.manim_scenes.graph_theory.quadrant import Quadrant
from instant_insanity.manim_scenes.graph_theory.three_d_polygons import TrackedVGroup, ThreeDPolygons
from instant_insanity.manim_scenes.graph_theory.three_d_puzzle_cube import ThreeDPuzzleCube

Updater: TypeAlias = Callable[[TrackedVGroup], TrackedVGroup]

class TrackedVGroupAnimator(ABC):
    tracked_vgroup: TrackedVGroup

    def __init__(self, tracked_vgroup: Mobject) -> None:
        if not isinstance(tracked_vgroup, TrackedVGroup):
            raise TypeError(f'tracked_vgroup must be of type TrackedVGroup but got {type(tracked_vgroup)}')

        assert isinstance(tracked_vgroup, TrackedVGroup)
        self.tracked_vgroup = tracked_vgroup

    def mk_updater(self) -> Updater:
        """
        Make a nontime-based updater function for the animation.

        Returns:
            An updater for the animation.
        """

        def updater(tracked_vgroup: TrackedVGroup) -> TrackedVGroup:
            """
            Updates the TrackedVGroup instance to its current alpha parameter.

            Args:
                tracked_vgroup: the TrackedVGroup that is being animated.

            Returns:
                the TrackedVGroup.
            """
            tracked_vgroup.remove(*tracked_vgroup.submobjects)
            tracker: ValueTracker = tracked_vgroup.tracker
            alpha: float = tracker.get_value()
            self.interpolate(alpha)
            return tracked_vgroup

        return updater

    @abstractmethod
    def interpolate(self, alpha: float) -> None:
        pass


class ThreeDPolygonsAnimator(TrackedVGroupAnimator, ABC):
    """
    This is the abstract base class for `ThreeDPolygons` animators.
    """
    def __init__(self, three_d_polygons: Mobject) -> None:
        if not isinstance(three_d_polygons, ThreeDPolygons):
            raise TypeError(f'three_d_polygons must be of type ThreeDPolygons but got {type(three_d_polygons)}')
        super().__init__(three_d_polygons)


class CubeAnimator(TrackedVGroupAnimator, ABC):
    """
    This is the abstract base class for `ThreeDPuzzleCube` animators.
    """

    def __init__(self, cube: Mobject):
        if not isinstance(cube, ThreeDPuzzleCube):
            raise TypeError(f'cube must be of type ThreeDPuzzleCube but got {type(cube)}')
        super().__init__(cube)


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
        assert isinstance(self.tracked_vgroup, ThreeDPuzzleCube)
        cube: ThreeDPuzzleCube = self.tracked_vgroup
        alpha_rotation: np.ndarray = alpha * self.rotation
        alpha_translation: np.ndarray = alpha * self.translation
        name_to_initial_model_path: dict[FaceName, VertexPath] = cube.name_to_initial_model_path
        transformed_vertices: dict[FaceName, np.ndarray] = {
            name: transform_vertex_path(alpha_rotation, alpha_translation, name_to_initial_model_path[name])
            for name in FaceName
        }
        cube.mk_polygons(transformed_vertices)

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

        origin: Vertex = np.zeros(3, dtype=np.float64)
        unit_i: Vector = np.array([1, 0, 0], dtype=np.float64)
        unit_j: Vector = np.array([0, 1, 0], dtype=np.float64)
        unit_k: Vector = np.array([0, 0, 1], dtype=np.float64)
        quarter_turn: float = np.pi / 2.0

        # compute the point p, unit vector u, and angle theta that define a rotation about a line
        p: Vertex = origin
        u: Vector = unit_k
        theta_max: float = 0.0
        z_max: float = -(3.0 + self.expansion_factor) / 2.0
        face_normal: Vector = FACE_NAME_TO_UNIT_NORMAL[name]
        translation_max: Vector = z_max * unit_k + (self.expansion_factor - 1.0) * face_normal

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
        model_vertex_path: VertexPath = FACE_NAME_TO_VERTEX_PATH[name]
        rotated_vertex_path: VertexPath = apply_linear_transform(rot_mat, model_vertex_path)

        translation: Vector = alpha * translation_max
        transformed_vertex_path: np.ndarray = rotated_vertex_path + translation

        return transformed_vertex_path

    def interpolate(self, alpha: float) -> None:
        assert isinstance(self.tracked_vgroup, ThreeDPuzzleCube)
        cube: ThreeDPuzzleCube = self.tracked_vgroup

        name_to_transformed_vertex_path = {
            name: self.interpolate_face(name, alpha)
            for name in FaceName
        }

        cube.mk_polygons(name_to_transformed_vertex_path)

@dataclass
class FaceData:
    colour: FaceColour
    quadrant: Quadrant
    polygon: Polygon
    dot: Dot

def mk_face_data(graph: OppositeFaceGraph, cube: ThreeDPuzzleCube, name: FaceName) -> FaceData:
    colour: FaceColour = cube.get_colour_name(name)
    quadrant: Quadrant = graph.colour_to_node[colour]
    polygon: Polygon = cube.name_to_scene_polygon[name]
    vertices: np.ndarray = polygon.get_vertices()
    centroid: np.ndarray = np.mean(vertices, axis=0)
    dot: Dot = graph.mk_node_at(quadrant, centroid)
    return FaceData(colour, quadrant, polygon, dot)


class ConstructGraph(GridMixin, Scene):
    """
    This scene animates the construction of the opposite-face graph of a puzzle.
    Each cube of the puzzle is exploded into opposite-face pairs.
    Each opposite-face pair is morphed into an edge and added to the graph.
    """

    @staticmethod
    def mk_cube(cube_spec: PuzzleCubeSpec) -> ThreeDPuzzleCube:
        """
        Makes a puzzle cube.
        """
        # create a projection
        camera_z: float = 2.0
        viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)

        # Alternatively:
        # camera_z: float = 8.0
        # viewpoint: np.ndarray = np.array([5, 5, 20], dtype=np.float64)

        projection: Projection = PerspectiveProjection(viewpoint, camera_z=camera_z)

        # create the cube object
        cube: ThreeDPuzzleCube = ThreeDPuzzleCube(projection, cube_spec)

        # find the scene coordinates of the centre of the front face
        front_face: Polygon = cube.name_to_scene_polygon[FaceName.FRONT]
        centre: np.ndarray = front_face.get_center()
        scene_x: float = float(centre[0])
        scene_y: float = float(centre[1])

        # recreate the cube centered in the scene
        projection = PerspectiveProjection(viewpoint, scene_x=scene_x, scene_y=scene_y, camera_z=camera_z)
        cube = ThreeDPuzzleCube(projection, cube_spec)

        return cube

    @staticmethod
    def mk_start_end(graph: OppositeFaceGraph,
                     cube: ThreeDPuzzleCube,
                     axis_label: AxisLabel) -> tuple[FaceData, FaceData]:
        face_pair: tuple[FaceName, FaceName] = AXIS_TO_FACE_NAME_PAIR[axis_label]
        first: FaceData = mk_face_data(graph, cube, face_pair[0])
        second: FaceData = mk_face_data(graph, cube, face_pair[1])

        # sort the start and end nodes to match the order in the graph
        if first.quadrant <= second.quadrant:
            return first, second
        else:
            return second, first

    def play_cube_animation(self, cube: ThreeDPuzzleCube, animator: CubeAnimator, run_time=1.0) -> None:
        pass

    def animate_explode_cube(self, cube: ThreeDPuzzleCube) -> None:
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
        self.play(tracker.animate.set_value(1.0), run_time=4.0)
        cube.remove_updater(updater)

    def animate_shift_cube(self, cube: ThreeDPuzzleCube) -> None:
        # animate movement of exploded cube to the left
        cube_shift: np.ndarray = 3 * LEFT
        self.play(cube.animate.shift(cube_shift), run_time=1.0)

    def morph_opposite_faces_to_dots(self,
                                     start: FaceData,
                                     end: FaceData) -> None:
        # morph the pair of opposite faces from polygons to dots

        # force the polygons to have ccw orientation so the morphing to dots is smooth
        force_ccw(start.polygon)
        force_ccw(end.polygon)

        # morph the polygons to dots
        self.play(ReplacementTransform(start.polygon, start.dot),
                  ReplacementTransform(end.polygon, end.dot), run_time=2.0)


    def fade_in_opposite_face_edge(
            self,
            graph: OppositeFaceGraph,
            cube_axis: CubeAxis,
            start: FaceData,
            end: FaceData) -> None:
        # connect the start-end dots with a graph edge
        start_point: np.ndarray = start.dot.get_center()
        end_point: np.ndarray = end.dot.get_center()
        edge: LabelledEdge = graph.copy_edge_to(cube_axis, start_point, end_point)

        self.remove(start.dot, end.dot)
        self.add(edge, start.dot, end.dot)
        self.play(FadeIn(edge))
        self.remove(edge, start.dot, end.dot)

    def move_opposite_face_edge_to_graph(
            self,
            graph: OppositeFaceGraph,
            cube_axis: CubeAxis,
            start: FaceData,
            end: FaceData) -> None:

        # move the dots to the graph and always redraw the moving edge to connect their centres
        moving_edge: Mobject = always_redraw(
            lambda:
            graph.copy_edge_to(
                cube_axis,
                start.dot.get_center(),
                end.dot.get_center()
            )
        )

        # draw the dots on top of the moving edge
        self.add(moving_edge, start.dot, end.dot)

        target_start_dot: Dot = graph.node_to_mobject[start.quadrant]
        target_end_dot: Dot = graph.node_to_mobject[end.quadrant]
        self.play(
            start.dot.animate.move_to(target_start_dot),
            end.dot.animate.move_to(target_end_dot),
            run_time=2.0,
        )
        self.remove(moving_edge, start.dot, end.dot)

    def animate_construct_opposite_face_edge(
            self,
            graph: OppositeFaceGraph,
            cube_axis: CubeAxis,
            start: FaceData,
            end:FaceData) -> None:
        self.morph_opposite_faces_to_dots(start, end)
        self.fade_in_opposite_face_edge(graph, cube_axis, start, end)
        self.move_opposite_face_edge_to_graph(graph, cube_axis, start, end)

        # add the edge to the subgraph
        graph.set_subgraph_edge(cube_axis, True)

    def construct(self):
        self.add_grid(True)

        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        puzzle: Puzzle = Puzzle(puzzle_spec)

        # TODO: add the 3d puzzle to the scene
        # TODO: the 3d puzzle should make all the cubes and expose them in an array of cubes

        graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, 4 * RIGHT)
        self.play(FadeIn(graph))

        cube_number: PuzzleCubeNumber
        for cube_number in PuzzleCubeNumber:
            # if cube_number > PuzzleCubeNumber.ONE:
            #     break
            puzzle_cube: PuzzleCube = puzzle.number_to_cube[cube_number]
            cube_spec: PuzzleCubeSpec = puzzle_cube.cube_spec
            cube: ThreeDPuzzleCube = self.mk_cube(cube_spec)

            self.play(FadeIn(cube))
            self.wait()

            self.animate_explode_cube(cube)
            self.animate_shift_cube(cube)

            axis_label: AxisLabel
            cube_axis: CubeAxis
            for axis_label in AxisLabel:
                cube_axis = (cube_number, axis_label)
                start: FaceData
                end: FaceData
                start, end = self.mk_start_end(graph, cube, axis_label)
                self.animate_construct_opposite_face_edge(graph, cube_axis, start, end)

        self.wait(4.0)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = ConstructGraph()
        scene.render()
