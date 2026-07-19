"""
This module animates the search for the two subgraphs of the opposite-face graph of a puzzle.
"""

from manim import Scene, tempconfig, UP, DOWN, LEFT, RIGHT, Tex, Dot, StealthTip, CubicBezier, FadeIn, FadeOut
from manim.typing import Vector3D, Point3D
from manim.utils.color.X11 import BLACK
from manim_voiceover import VoiceoverScene

from instant_insanity.core.cube import FacePlane
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.puzzle import Puzzle, PuzzleCubeNumber, AxisLabel, CubeAxis, WINNING_MOVES_PUZZLE
from instant_insanity.mobjects.labelled_edge import LabelledEdge
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, EdgeToSubgraphMapping, \
    EdgeToMobjectMapping, mk_edge_directions
from instant_insanity.mobjects.quadrant import NodePair, Quadrant
from instant_insanity.mobjects.stealth_tip import mk_stealth_tip_from_cubic_bezier, EdgeTip, CubeEdgeTip
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.solvers.graph_solver import GraphSolver, Grid

class GraphTheoryScene4(GridMixin, DiscussionMixin, VoiceoverScene):
    def move_solution(self,
                      graph_solver: GraphSolver,
                      solution_index: int,
                      total_graph: OppositeFaceGraph,
                      front_graph: OppositeFaceGraph,
                      top_graph) -> None:
        """
        Moves a solution into the subgraphs.
        Args:
            graph_solver: the solved graph
            solution_index: the solution index in the solutions list
            total_graph: the opposite face graph for the puzzle
            front_graph: the opposite face subgraph for the front-back faces
            top_graph: the opposite face subgraph for the top-bottom faces
        """
        assert solution_index < len(graph_solver.solutions)

        grid: Grid = graph_solver.solutions[solution_index]
        grid_key: tuple[FacePlane, PuzzleCubeNumber]
        grid_value: AxisLabel | None
        for grid_key, grid_value in grid.items():
            face_name: FacePlane = grid_key[0]
            cube_number: PuzzleCubeNumber = grid_key[1]

            assert grid_value is not None
            assert isinstance(grid_value, AxisLabel)
            axis_label: AxisLabel = grid_value

            target_graph: OppositeFaceGraph = front_graph if face_name == FacePlane.FRONT else top_graph
            self.move_edge((cube_number, axis_label), total_graph, target_graph)

    def move_edge(self,
                  cube_axis: CubeAxis,
                  source_graph: OppositeFaceGraph,
                  target_graph: OppositeFaceGraph) -> None:
        """
        Moves an edge from a source graph to a target graph.

        Args:
            cube_axis: the edge.
            source_graph: the source graph.
            target_graph: the target graph.
        """
        # the source subgraph MUST contain the edge
        assert source_graph.edge_to_subgraph[cube_axis]

        # the target subgraph MUST NOT contain the edge
        assert not target_graph.edge_to_subgraph[cube_axis]

        source_edge: LabelledEdge = source_graph.edge_to_mobject[cube_axis]
        target_edge: LabelledEdge = target_graph.edge_to_mobject[cube_axis]

        start_node: Quadrant
        end_node: Quadrant
        start_node, end_node = source_edge.node_pair

        # create the moving mobjects
        moving_edge: LabelledEdge = source_edge.copy()
        moving_start_dot: Dot = source_graph.node_to_mobject[start_node].copy()
        moving_end_dot: Dot = source_graph.node_to_mobject[end_node].copy()

        # move the edge
        delta: Vector3D = target_edge.get_center() - source_edge.get_center()
        source_graph.set_subgraph_edge(cube_axis, False)
        self.add(moving_edge, moving_start_dot, moving_end_dot)
        self.play(moving_edge.animate.shift(delta),
                  moving_start_dot.animate.shift(delta),
                  moving_end_dot.animate.shift(delta),
                  run_time=2)
        self.remove(moving_edge, moving_start_dot, moving_end_dot)
        target_graph.set_subgraph_edge(cube_axis, True)

        self.wait()

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        puzzle: Puzzle =  WINNING_MOVES_PUZZLE

        start_centre: Point3D = 4 * RIGHT + DOWN
        end_centre: Point3D = 2 * UP

        # add the total graph at the initial position from the end of previous scene

        total_graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, start_centre)
        full_subgraph: EdgeToSubgraphMapping = total_graph.mk_subgraph_for_flag(True)
        total_graph.set_subgraph(full_subgraph)

        self.add(total_graph)

        voiceover: str = """
        We've converted the puzzle into its corresponding opposite-face graph. 
        Our next step is to solve the puzzle using this graph.
        """
        self.say(voiceover)

        voiceover = """
        Recall that the reason the opposite-face graph makes it easier to solve the puzzle
        is that it lets us build up the solution in two stages.
        First, we'll solve the front and back faces.
        Then we'll solve the top and bottom faces.
        Note that once we've fixed the front and back faces we can still rotate the cubes
        about their x-axis. Recall that the x-axis of each cube points from its back face to its front face.
        Therefore, rotating a cube about its x-axis doesn't change the colours of its front and back faces.
        TO DO: show a cube rotating abouts its x-axis.
        """
        self.say(voiceover)

        self.wait()

        voiceover = """
        We're going to work on the opposite-face graph, so let's
        move it into a more central position.
        """
        self.say(voiceover)

        # move the full graph from start_centre to end_centre
        self.play(total_graph.animate.shift(end_centre - start_centre))
        # add the subgraphs

        voiceover = """
        Our next step is to solve the front-back and top-bottom faces.
        Solving a pair of opposite faces requires us to select one opposite-face pair from each cube
        such that no colour is repeated. The nodes of the graph represent colours and the edges
        represent opposite-face pairs. We therefore need to select four edges from the full
        opposite-face graph such that there is exactly one edge from each cube and exactly
        two edges touching each node where a loop counts as two edges.
        TO DO: define subgraph, node degree, and 2-factor.
        """

        voiceover = """
        Our task now is to find two independent 2-factors of the full opposite-face graph,
        one for the front-back faces and another for the top-bottom faces.
        Let's start by drawing their nodes.
        """
        self.say(voiceover)

        front_graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, 4 * LEFT + 1.5 * DOWN)
        top_graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, 4 * RIGHT + 1.5 * DOWN)

        front_text: Tex = Tex("front-back", color=BLACK, font_size=36)
        top_text: Tex = Tex("top-bottom", color=BLACK, font_size=36)

        front_text.next_to(front_graph, DOWN, buff=0.5)
        top_text.next_to(top_graph, DOWN, buff=0.5)

        self.add(total_graph, front_graph, top_graph, front_text, top_text)

        graph_solver: GraphSolver = GraphSolver(puzzle)
        graph_solver.solve()

        voiceover = """
        Now let's find the two independent 2-factors.
        It's arbitrary which 2-factor represents the front-back and top-bottom faces.
        If we interchange the 2-factors then we still have a solution.
        """
        self.say(voiceover)

        self.move_solution(graph_solver, 0, total_graph, front_graph, top_graph)

        voiceover = """
        Now we've found the two independent 2-factors.
        In order to turn these into orientations of the cubes we need to give each 2-factor a direction
        such that each node has in-degree one and out-degree one.
        The edge directions point from front to back and top to bottom.
        The edge direction is arbitrary. If we reverse directions we still have a solution.
        Altogether, if we start from a valid pair of 2-factors we can swap them or independently
        change their directions, giving a total of eight distinct but essentially equivalent
        solutions. TO DO: do the math and maybe animate the eight solutions.
        """
        self.say(voiceover)

        subgraph: OppositeFaceGraph
        for subgraph in (front_graph, top_graph):
            cube_edge_tips: CubeEdgeTip = mk_edge_directions(subgraph)
            for edge_tip in cube_edge_tips.values():
                self.play(FadeIn(edge_tip.tip), run_time=0.5)

        voiceover = """
        We now have found two independent 2-factors of the full opposite-face graph.
        Our final step is to convert this information into cube orientations which
        by construction solve the puzzle. Ingeneous, isn't it!
        """

        # fade out the total graph in preparation for entry to the next scene CubesFromSubgraphs

        self.play(FadeOut(total_graph))

        self.wait(4)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene4()
        scene.render()
