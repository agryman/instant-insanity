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
from collections import OrderedDict

import numpy as np

from manim import (tempconfig, Mobject, ValueTracker, Polygon, Dot, LEFT, RIGHT, FadeIn,
                   always_redraw, Create, DOWN, ORIGIN)
from manim.typing import Point3D, Vector3D, Point3D_Array
from manim_voiceover import VoiceoverScene

from instant_insanity.animators.animorph import Animorph
from instant_insanity.animators.polygon_to_dot_animator import PolygonToDotAnimorph
from instant_insanity.animators.polygons_3d_animator import RigidMotionPolygons3DAnimorph
from instant_insanity.animators.puzzle_3d_animators import Puzzle3DAnimorph, Puzzle3DCubeExplosionAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FacePlane
from instant_insanity.core.geometry_types import SortedPolygonKeyToPolygonMapping
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import (
    Projection,
    PerspectiveProjection,
    OrthographicProjection,
    mk_standard_orthographic_projection,
)
from instant_insanity.core.puzzle import (PuzzleSpec, Puzzle, PuzzleCubeSpec, WINNING_MOVES_PUZZLE_SPEC,
                                          PuzzleCubeNumber, PuzzleCube, CubeAxis, AxisLabel,
                                          AXIS_TO_FACE_LABEL_PAIR, FaceLabelPair, FaceLabel,
                                          INITIAL_FACE_PLANE_TO_LABEL)
from instant_insanity.animators.cube_animators import CubeAnimorph, CubeExplosionAnimorph
from instant_insanity.mobjects.labelled_edge import LabelledEdge, PointPair
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, FaceData, mk_face_data_from_cube, \
    mk_face_data_from_puzzle
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, Puzzle3DPolygonName, mk_standard_puzzle3d
from instant_insanity.mobjects.puzzle_cube_3d import PuzzleCube3D
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.subscene import SubsceneMixin


class GraphTheoryScene3(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    """
    This scene animates the construction of the opposite-face graph of a puzzle.
    Each cube of the puzzle is exploded into opposite-face pairs.
    Each opposite-face pair is morphed into an edge and added to the graph.
    """

    @staticmethod
    def mk_orthographic_projection() -> OrthographicProjection:
        return mk_standard_orthographic_projection()

    @staticmethod
    def mk_perspective_projection() -> PerspectiveProjection:
        camera_z: float = 2.0
        viewpoint: Point3D = np.array([2, 2, 6], dtype=np.float64)
        projection: PerspectiveProjection = PerspectiveProjection(viewpoint,
                                                       scene_x=-1.0,
                                                       scene_y=0.0,
                                                       camera_z=camera_z)
        return projection


    @staticmethod
    def mk_cube3d(cube_spec: PuzzleCubeSpec, projection: Projection) -> PuzzleCube3D:
        """
        Makes a puzzle cube.

        Args:
            cube_spec (PuzzleCubeSpec): The puzzle cube specification.
            projection (Projection): The projection of the puzzle cube.

        Returns:
            the 3D puzzle cube.
        """
        cube_centre: Point3D = 1 * LEFT + 6 * DOWN
        cube3d: PuzzleCube3D = PuzzleCube3D(projection, cube_spec, cube_centre)

        return cube3d

    @staticmethod
    def mk_puzzle3d(puzzle: Puzzle, projection: Projection) -> Puzzle3D:
        """
        Makes a puzzle in the top half of the scene.

        Args:
            puzzle: the puzzle.
            projection: the projection.

        Returns:
            the 3D puzzle.
        """
        puzzle_spec: PuzzleSpec = puzzle.puzzle_spec

        return mk_standard_puzzle3d(puzzle_spec, projection)

    @staticmethod
    def detach_axis_from_cube(cube3d: PuzzleCube3D,
                              axis_label: AxisLabel,
                              graph: OppositeFaceGraph) -> tuple[FaceData, FaceData]:
        """
        This method detaches the pair of faces defined by the axis from the cube,
        sets their polygon z-index to reflect the depth-sorted order,
        and puts them into a FaceData pair.

        Args:
            cube3d: the cube.
            axis_label: the axis.
            graph: the opposite-face graph.

        Returns:
            the (start, end) face data pair.
        """
        # compute the face labels of the axis
        face_pair: FaceLabelPair = AXIS_TO_FACE_LABEL_PAIR[axis_label]
        axis_face_labels: set[FaceLabel] = set(face_pair)

        # get the polygons of the axis in depth-sorted order
        key_to_scene_polygon: SortedPolygonKeyToPolygonMapping[FaceLabel] = cube3d.key_to_scene_polygon
        key_to_axis_polygon: SortedPolygonKeyToPolygonMapping[FaceLabel] = OrderedDict()
        face_key: FaceLabel
        polygon: Polygon
        z_index: int = 1
        for face_key in key_to_scene_polygon.keys():
            if face_key in axis_face_labels:
                polygon = key_to_scene_polygon[face_key]
                polygon.set_z_index(z_index)
                z_index += 1
                key_to_axis_polygon[face_key] = polygon

        # hide the axis faces from the cube
        visible_polygon_keys: set[FaceLabel] = cube3d.visible_polygon_keys
        updated_visible_polygon_keys: set[FaceLabel] = visible_polygon_keys - axis_face_labels
        cube3d.set_visible_polygon_keys(updated_visible_polygon_keys)

        # make the face data pair
        data_list: list[FaceData] = []
        for face_label in face_pair:
            polygon = key_to_axis_polygon[face_label]
            data: FaceData = mk_face_data_from_cube(graph, cube3d, face_label, polygon)
            data_list.append(data)

        # sort the start and end nodes to match the order in the graph
        first: FaceData = data_list[0]
        second: FaceData = data_list[1]
        if first.quadrant <= second.quadrant:
            return first, second
        else:
            return second, first

    @staticmethod
    def detach_axis_from_puzzle(puzzle3d: Puzzle3D,
                                cube_axis: CubeAxis,
                                graph: OppositeFaceGraph) -> tuple[FaceData, FaceData]:
        """
        This method detaches the pair of faces defined by the cube axis from the puzzle
        sets their polygon z-index to reflect the depth-sorted order,
        and puts them into a FaceData pair.

        Args:
            puzzle3d: the puzzle.
            cube_axis: the cube axis.
            graph: the opposite-face graph.

        Returns:
            the (start, end) face data pair.
        """
        cube_number: PuzzleCubeNumber
        axis_label: AxisLabel
        cube_number, axis_label = cube_axis

        # compute the face names of the axis
        face_pair: FaceLabelPair = AXIS_TO_FACE_LABEL_PAIR[axis_label]
        axis_face_names: set[Puzzle3DPolygonName] = {(cube_number, face_label) for face_label in face_pair}

        # get the polygons of the axis in depth-sorted order
        key_to_scene_polygon: SortedPolygonKeyToPolygonMapping[Puzzle3DPolygonName] = puzzle3d.key_to_scene_polygon
        key_to_axis_polygon: SortedPolygonKeyToPolygonMapping[Puzzle3DPolygonName] = OrderedDict()
        polygon: Polygon
        z_index: int = 1
        for face_name in key_to_scene_polygon.keys():
            if face_name in axis_face_names:
                polygon = key_to_scene_polygon[face_name]
                polygon.set_z_index(z_index)
                z_index += 1
                key_to_axis_polygon[face_name] = polygon

        # hide the axis faces from the puzzle
        visible_polygon_keys: set[Puzzle3DPolygonName] = puzzle3d.visible_polygon_keys
        updated_visible_polygon_keys: set[Puzzle3DPolygonName] = visible_polygon_keys - axis_face_names
        puzzle3d.set_visible_polygon_keys(updated_visible_polygon_keys)

        # make the face data pair
        data_list: list[FaceData] = []
        for face_label in face_pair:
            polygon_name: Puzzle3DPolygonName = (cube_number, face_label)
            polygon = key_to_axis_polygon[polygon_name]
            data: FaceData = mk_face_data_from_puzzle(graph, puzzle3d, cube_number, face_label, polygon)
            data_list.append(data)

        # sort the start and end nodes to match the order in the graph
        first: FaceData = data_list[0]
        second: FaceData = data_list[1]
        if first.quadrant <= second.quadrant:
            return first, second
        else:
            return second, first

    def animate_explode_puzzle_cube(self, puzzle3d: Puzzle3D, cube_number: PuzzleCubeNumber) -> None:
        expansion_factor: float = 2.0
        animorph: Puzzle3DAnimorph = Puzzle3DCubeExplosionAnimorph(puzzle3d, expansion_factor, cube_number)
        puzzle3d.conceal_polygons()
        animorph.play(self, alpha=1.0, run_time=1.0)

    def animate_shift_cube(self, cube3d: PuzzleCube3D) -> None:
        # animate movement of exploded cube to the left
        cube_shift: Vector3D = 3 * LEFT
        self.play(cube3d.animate.shift(cube_shift), run_time=1.0)

    def morph_opposite_faces_to_dots(self,
                                     start: FaceData,
                                     end: FaceData) -> None:
        # morph the pair of opposite faces from polygons to dots

        start_animorph: PolygonToDotAnimorph = PolygonToDotAnimorph(start.polygon, start.dot)
        end_animorph: PolygonToDotAnimorph = PolygonToDotAnimorph(end.polygon, end.dot)

        alpha_tracker: ValueTracker = ValueTracker(0.0)
        start.polygon.add_updater(lambda m: start_animorph.morph_to(alpha_tracker.get_value()))
        end.polygon.add_updater(lambda m: end_animorph.morph_to(alpha_tracker.get_value()))
        self.play(alpha_tracker.animate.set_value(1.0))
        start.polygon.clear_updaters()
        end.polygon.clear_updaters()

        self.remove(start.polygon, end.polygon)

    def fade_in_opposite_face_edge(
            self,
            graph: OppositeFaceGraph,
            cube_axis: CubeAxis,
            start: FaceData,
            end: FaceData) -> None:
        # connect the start-end dots with a graph edge
        start_point_0: Point3D = start.dot.get_center()
        end_point_0: Point3D = end.dot.get_center()
        point_pair_0: PointPair = (start_point_0, end_point_0)

        start_dot_1: Dot = graph.node_to_mobject[start.quadrant]
        end_dot_1: Dot = graph.node_to_mobject[end.quadrant]

        start_point_1: Point3D = start_dot_1.get_center()
        end_point_1: Point3D = end_dot_1.get_center()
        point_pair_1: PointPair = (start_point_1, end_point_1)

        edge: LabelledEdge = graph.copy_edge_from_to(cube_axis, point_pair_0, point_pair_1, point_pair_0)

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

        start_point_0: Point3D = start.dot.get_center().copy()
        end_point_0: Point3D = end.dot.get_center().copy()
        point_pair_0: PointPair = (start_point_0, end_point_0)

        start_dot_1: Dot = graph.node_to_mobject[start.quadrant]
        end_dot_1: Dot = graph.node_to_mobject[end.quadrant]

        start_point_1: Point3D = start_dot_1.get_center()
        end_point_1: Point3D = end_dot_1.get_center()
        point_pair_1: PointPair = (start_point_1, end_point_1)

        # move the dots to the graph and always redraw the moving edge to connect their centres
        moving_edge: Mobject = always_redraw(
            lambda:
            graph.copy_edge_from_to(
                cube_axis,
                point_pair_0,
                point_pair_1,
                (start.dot.get_center(), end.dot.get_center()))
        )

        # draw the dots on top of the moving edge
        self.add(moving_edge, start.dot, end.dot)

        self.play(
            start.dot.animate.move_to(start_dot_1),
            end.dot.animate.move_to(end_dot_1),
            run_time=1.0
        )
        self.remove(moving_edge, start.dot, end.dot)

    def animate_construct_opposite_face_edge(
            self,
            graph: OppositeFaceGraph,
            cube_axis: CubeAxis,
            start: FaceData,
            end: FaceData) -> None:

        # the face polygons have been detached from the puzzle cube so added them to the scene
        self.add(start.polygon, end.polygon)

        self.morph_opposite_faces_to_dots(start, end)
        self.fade_in_opposite_face_edge(graph, cube_axis, start, end)
        self.move_opposite_face_edge_to_graph(graph, cube_axis, start, end)

        # add the edge to the subgraph
        graph.set_subgraph_edge(cube_axis, True)

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        projection: Projection = GraphTheoryScene3.mk_orthographic_projection()

        # create and display the 3D puzzle
        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        puzzle: Puzzle = Puzzle(puzzle_spec)
        puzzle3d: Puzzle3D = GraphTheoryScene3.mk_puzzle3d(puzzle, projection)
        self.add(puzzle3d)

        voiceover_1: str = '''
        Here's our puzzle.
        Let's construct its opposite-face graph.
        '''
        self.say(voiceover_1)

        voiceover_2a: str = '''
        Start by drawing its nodes.
        '''
        self.say(voiceover_2a)

        graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, 4 * RIGHT + DOWN)
        self.play(Create(graph))

        voiceover_2b: str = '''
        The graph has no edges yet. 
        We'll add them
        by morphing each cube into its three pairs of opposite faces
        and then converting each pair into an edge.
        Each cube will therefore contribute three edges by this process
        giving a total of 12 edges.
        '''
        self.say(voiceover_2b)
        self.wait(0.5)

        cube_number: PuzzleCubeNumber
        cube: PuzzleCube
        face_label: FaceLabel
        axis_label: AxisLabel
        cube_axis: CubeAxis
        start: FaceData
        end: FaceData
        rotation: Vector3D
        translation: Vector3D
        animorph: Animorph
        moveable_polygon_ids: set[Puzzle3DPolygonName]

        for cube_number in PuzzleCubeNumber:

            # move the cube to the work area
            moveable_polygon_keys: set[Puzzle3DPolygonName] = {
                (cube_number, face_label) for face_label in FaceLabel
            }

            # move the centre of the front face to the target
            front_target: Point3D = 6.0 * DOWN + 3.0 * LEFT
            front_label: FaceLabel = INITIAL_FACE_PLANE_TO_LABEL[FacePlane.FRONT]
            front_name: Puzzle3DPolygonName = (cube_number, front_label)
            front_path: Point3D_Array = puzzle3d.key_to_model_path[front_name]
            front_centre: Point3D = np.mean(front_path, 0)
            translation = front_target - front_centre

            rotation = ORIGIN

            animorph = RigidMotionPolygons3DAnimorph[Puzzle3DPolygonName](puzzle3d, rotation, translation, moveable_polygon_keys)

            voiceover_4: str = f'Convert cube {cube_number}.'
            if cube_number == PuzzleCubeNumber.FOUR:
                voiceover_4 = f'Finally, convert cube {cube_number}.'

            with self.voiceover(text=voiceover_4) as _:
                puzzle3d.conceal_polygons()
                animorph.play(self, run_time=0.5)

            puzzle3d.checkpoint()

            self.animate_explode_puzzle_cube(puzzle3d, cube_number)

            for axis_label in AxisLabel:
                cube_axis = (cube_number, axis_label)
                start, end = self.detach_axis_from_puzzle(puzzle3d, cube_axis, graph)
                self.animate_construct_opposite_face_edge(graph, cube_axis, start, end)

            puzzle3d.hide_cube(cube_number)

        voiceover_8: str = 'The opposite-face graph is now complete.'
        self.say(voiceover_8)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene3()
        scene.render()
