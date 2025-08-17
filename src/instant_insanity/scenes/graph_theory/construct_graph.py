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

import numpy as np

from manim import (tempconfig, Mobject, ValueTracker, Polygon, Dot, Scene, LEFT, RIGHT, FadeIn, ReplacementTransform,
                   always_redraw)

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FaceName
from instant_insanity.core.force_ccw import force_ccw
from instant_insanity.core.geometry_types import PolygonId
from instant_insanity.core.projection import Projection, PerspectiveProjection
from instant_insanity.core.puzzle import (PuzzleSpec, Puzzle, PuzzleCubeSpec, WINNING_MOVES_PUZZLE_SPEC,
                                          PuzzleCubeNumber, PuzzleCube, CubeAxis, AxisLabel, AXIS_TO_FACE_NAME_PAIR)
from instant_insanity.animators.cube_animators import CubeAnimator, CubeExplosionAnimator
from instant_insanity.animators.tracked_vgroup_animator import Updater
from instant_insanity.mobjects.labelled_edge import LabelledEdge
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, FaceData, mk_face_data
from instant_insanity.mobjects.three_d_puzzle_cube import ThreeDPuzzleCube
from instant_insanity.scenes.coordinate_grid import GridMixin


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
        front_id: PolygonId = ThreeDPuzzleCube.name_to_id(FaceName.FRONT)
        front_face: Polygon = cube.id_to_scene_polygon[front_id]
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

    def animate_explode_cube(self, cube: ThreeDPuzzleCube) -> None:
        # animate cube rigid motion
        # rotation: np.ndarray = ORIGIN
        # translation: np.ndarray = 7 * LEFT #+ DOWN
        # animator: CubeAnimator = CubeRigidMotionAnimator(cube, rotation, translation)

        # animate cube explosion
        cube.remove(*cube.submobjects)
        expansion_factor: float = 2.0
        animator: CubeAnimator = CubeExplosionAnimator(cube, expansion_factor)
        animator.play(self, alpha=1.0, run_time=4.0)

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
            end: FaceData) -> None:
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
