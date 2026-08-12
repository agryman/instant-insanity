"""
This module animates the search for the two subgraphs of the opposite-face graph of a puzzle.
"""

from typing import Sequence

from manim import tempconfig, DOWN, LEFT, RIGHT, Tex, Dot, FadeIn, FadeOut, Animation, AnimationGroup, Indicate, BLACK, \
    LaggedStart, Text
from manim.typing import Vector3D, Point3D
from manim_voiceover import VoiceoverScene

from instant_insanity.core.cube import FacePlane
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import Puzzle, PuzzleCubeNumber, AxisLabel, CubeAxis, WINNING_MOVES_PUZZLE, \
    PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC, FaceColour
from instant_insanity.mobjects.coloured_cube import MANIM_COLOUR_MAP
from instant_insanity.mobjects.labelled_edge import LabelledEdge
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, EdgeToSubgraphMapping, mk_edge_directions
from instant_insanity.mobjects.puzzle_3d import mk_standard_puzzle3d, DEFAULT_BUFF, Puzzle3D
from instant_insanity.mobjects.puzzle_face_labeller import PuzzleFaceLabeller
from instant_insanity.mobjects.quadrant import Quadrant
from instant_insanity.mobjects.stealth_tip import CubeEdgeTip
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene
from instant_insanity.solvers.graph_solver import GraphSolver, Grid

class GraphTheoryScene4(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):

    puzzle: Puzzle
    puzzle3d: Puzzle3D
    puzzle_face_labeller: PuzzleFaceLabeller
    start_centre: Point3D
    end_centre: Point3D
    initial_gap: float
    min_gap: float
    total_graph: OppositeFaceGraph
    front_graph: OppositeFaceGraph
    top_graph: OppositeFaceGraph
    front_text: Tex
    top_text: Tex

    def move_solution(self,
                      graph_solver: GraphSolver,
                      solution_index: int,
                      total_graph: OppositeFaceGraph,
                      front_graph: OppositeFaceGraph,
                      top_graph: OppositeFaceGraph) -> None:
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
                  target_graph: OppositeFaceGraph,
                  run_time: float = 0.5) -> None:
        """
        Moves an edge from a source graph to a target graph.

        Args:
            cube_axis: the edge.
            source_graph: the source graph.
            target_graph: the target graph.
            run_time: the run time in seconds.
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
                  run_time=run_time)
        self.remove(moving_edge, moving_start_dot, moving_end_dot)
        target_graph.set_subgraph_edge(cube_axis, True)

    def subscene_1_discuss_opposite_face_graph(self) -> None:
        if self.skip(self.subscene_1_discuss_opposite_face_graph):
            return

        voiceover: str
        voiceover = """
        We'll now show how to use the opposite-face graph to solve the puzzle.
        """
        self.say(voiceover)

    def subscene_2_discuss_subgraphs(self) -> None:
        if self.skip(self.subscene_2_discuss_subgraphs):
            return

        voiceover: str
        voiceover = """        
        Suppose we are given an arrangement of the cubes.
        Its front and back sides consist of four pairs of opposite faces, one per cube.
        Similarly, for its top and bottoms sides.
        So the opposite-face graph lets us represent any arrangement by a pair of its subgraphs
        which we refer to as the front-back and top-bottom subgraphs.
        """
        self.say(voiceover)

    def subscene_3_discuss_starting_arrangement(self) -> None:
        if self.skip(self.subscene_3_discuss_starting_arrangement):
            return

        voiceover: str

        self.say("""
        A subgraph of a graph is a subset of its nodes and edges that themselves form a graph.
        Let's look at these subgraphs for our starting arrangement.
        The front face of each cube in the starting arrangement is labelled ex.
        """)
        self.puzzle_face_labeller.indicate_face_labels(self, FacePlane.FRONT)

        self.say("""
        Move the ex edges to the front-back subgraph.
        """)
        for cube in PuzzleCubeNumber:
            self.move_edge((cube, AxisLabel.X), self.total_graph, self.front_graph)

        self.say("""
        Similarly, The top face of each cube is labelled zed.
        """)
        self.puzzle_face_labeller.indicate_face_labels(self, FacePlane.TOP)

        self.say("""
        Move the zed edges.
        """)
        for cube in PuzzleCubeNumber:
            self.move_edge((cube, AxisLabel.Z), self.total_graph, self.top_graph)

        self.say("""
        In a solution, each colour must appear once on the front side and once on the back.
        This means that each node of the front-back subgraph must be touched by 2 edges where
        a loop counts as touching a node twice.

        The number of edges that touch a node is called its degree.
        Therefore, in a solution, every node in a subgraph must have degree 2.
        """)

        self.say("""
        We know that the starting arrangment is not a solution and this fact
        shows up clearly in the subgraphs.
        
        Look at the red and blue nodes in the front-back subgraph.
        """)

        red_node: Dot = self.front_graph.get_node_by_colour(FaceColour.RED)
        red_colour: str = str(MANIM_COLOUR_MAP[FaceColour.RED])
        scale_factor: float = 1.5
        blue_node: Dot = self.front_graph.get_node_by_colour(FaceColour.BLUE)
        blue_colour: str = str(MANIM_COLOUR_MAP[FaceColour.BLUE])
        run_time: float = 1.0
        delay: float = 0.3
        lag_ratio: float = delay / run_time
        # pass group=self.front_graph so that AnimationGroup doesn't wrap the nodes in a new Group.
        # Scene.add_mobjects_from_animations would add that new Group to the scene, and Scene.add
        # then restructures self.front_graph out of scene.mobjects, replacing it by its submobjects.
        # Its edges would then be rendered directly by the scene and set_subgraph could no longer hide them.
        self.play(
            LaggedStart(
                Indicate(red_node, color=red_colour, scale_factor=scale_factor),
                Indicate(blue_node, color=blue_colour, scale_factor=scale_factor),
                group=self.front_graph,
                lag_ratio=lag_ratio
            ),
            run_time=run_time
        )

        self.say("""
        The red node has degree 3 and the blue node has degree 1,
        confirming that the starting arrangement is not a solution.
        """)

        self.say("""
        Similarly, the red and blue nodes of the top-bottom subgraph do not have degree 2.
        """)
        red_node = self.top_graph.get_node_by_colour(FaceColour.RED)
        blue_node = self.top_graph.get_node_by_colour(FaceColour.BLUE)
        self.play(
            LaggedStart(
                Indicate(red_node, color=red_colour, scale_factor=scale_factor),
                Indicate(blue_node, color=blue_colour, scale_factor=scale_factor),
                group=self.top_graph,
                lag_ratio=lag_ratio
            ),
            run_time=run_time
        )

        self.say("""
        Now we can precisely state what a solution looks like in terms of graphs.
        
        A solution is a pair of subgraphs that represent the front-back and top-bottom sides of the arrangement.
        Each subgraph must have one edge from each cube and each node must have degree 2.
        Also, the subgraphs must not have any edges in common since every pair of opposite faces
        is either front-back, top-bottom, or left-right.
        
        Let's reset the opposite-face graph and try to find a solution.
        """)

        # restore the opposite-face graph in reverse order, i.e. undo top then undo front
        # for cube_axis, source_graph in zip([AxisLabel.Z, AxisLabel.X], [self.top_graph, self.front_graph]):
        #     for cube in PuzzleCubeNumber:
        #         self.move_edge((cube, cube_axis), source_graph, self.total_graph)
        for cube in PuzzleCubeNumber:
            self.move_edge((cube, AxisLabel.Z), self.top_graph, self.total_graph)
        for cube in PuzzleCubeNumber:
            self.move_edge((cube, AxisLabel.X), self.front_graph, self.total_graph)

    def subscene_4_discuss_finding_subgraphs(self) -> None:
        if self.skip(self.subscene_4_discuss_finding_subgraphs):
            return

        voiceover: str

        voiceover = """
        Our task now is to find front-back and top-bottom subgraphs that solve the puzzle.
        
        Let's apply our powers of visual reasoning.
        At first glance, it looks like we could form two subgraphs from the edges that connect adjacent nodes.
        Let's simplify the graph by temporarily hiding the diagonal edge 3 ex.
        """
        self.say(voiceover)
        # Indicate 3X, 1Z, 2Y
        label_3x: Text = self.total_graph.get_edge_label(PuzzleCubeNumber.THREE, AxisLabel.X)
        self.play(Indicate(label_3x, scale_factor=1.5, color=BLACK))
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.X), False)

        self.say("and the two loops, 1 zed")
        label_1z: Text = self.total_graph.get_edge_label(PuzzleCubeNumber.ONE, AxisLabel.Z)
        self.play(Indicate(label_1z, scale_factor=1.5, color=BLACK))
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.ONE, AxisLabel.Z), False)

        self.say("and 2 wy.")
        label_2x: Text = self.total_graph.get_edge_label(PuzzleCubeNumber.TWO, AxisLabel.Y)
        self.play(Indicate(label_2x, scale_factor=1.5, color=BLACK))
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.Y), False)

        voiceover = """
        Now 1 ex and 1 wy are the only remaining edges from cube 1, 
        so one must go into the front-back subgraph
        and the other into the top-bottom.
        Let's move 1 ex to the front-back subgraph and 1 wy to the top-bottom.
        """
        self.say(voiceover)
        self.move_edge((PuzzleCubeNumber.ONE, AxisLabel.X), self.total_graph, self.front_graph)
        self.move_edge((PuzzleCubeNumber.ONE, AxisLabel.Y), self.total_graph, self.top_graph)

        voiceover = """
        It looks like the edges 2 ex, 4 ex, and 3 wy will complete the front-back subgraph.
        Let's move them.
        """
        self.say(voiceover)
        self.move_edge((PuzzleCubeNumber.TWO, AxisLabel.X), self.total_graph, self.front_graph)
        self.move_edge((PuzzleCubeNumber.FOUR, AxisLabel.X), self.total_graph, self.front_graph)
        self.move_edge((PuzzleCubeNumber.THREE, AxisLabel.Y), self.total_graph, self.front_graph)

        voiceover = """
        Now we can complete the top-bottom subgraph using edges 2 zed, 3 zed, and 4 zed.
        Let's move them.
        """
        self.say(voiceover)
        self.move_edge((PuzzleCubeNumber.TWO, AxisLabel.Z), self.total_graph, self.top_graph)
        self.move_edge((PuzzleCubeNumber.THREE, AxisLabel.Z), self.total_graph, self.top_graph)
        self.move_edge((PuzzleCubeNumber.FOUR, AxisLabel.Z), self.total_graph, self.top_graph)

        voiceover = """
        We now have our two subgraphs that should solve the puzzle.
        The next step is to give a direction to each edge of the subgraphs so that each node has one incoming edge
        and one outgoing edge.
        """

        # The following code restores the state of the subscene to its entry condition.
        # It should not be executed in the final video.
        # self.wait(5.0)
        #
        # # undo to keep construct happy
        # self.say("Undoing all changes.")
        #
        # self.move_edge((PuzzleCubeNumber.TWO, AxisLabel.Z), self.top_graph, self.total_graph)
        # self.move_edge((PuzzleCubeNumber.THREE, AxisLabel.Z), self.top_graph, self.total_graph)
        # self.move_edge((PuzzleCubeNumber.FOUR, AxisLabel.Z), self.top_graph, self.total_graph)
        #
        # self.move_edge((PuzzleCubeNumber.TWO, AxisLabel.X), self.front_graph, self.total_graph)
        # self.move_edge((PuzzleCubeNumber.FOUR, AxisLabel.X), self.front_graph, self.total_graph)
        # self.move_edge((PuzzleCubeNumber.THREE, AxisLabel.Y), self.front_graph, self.total_graph)
        #
        # self.move_edge((PuzzleCubeNumber.ONE, AxisLabel.X), self.front_graph, self.total_graph)
        # self.move_edge((PuzzleCubeNumber.ONE, AxisLabel.Y), self.top_graph, self.total_graph)
        #
        # self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.X), True)
        # self.total_graph.set_subgraph_edge((PuzzleCubeNumber.ONE, AxisLabel.Z), True)
        # self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.Y), True)
        #
        # self.say("Are we back to the starting state?")
        #
        # self.wait(5.0)

    def subscene_9_discuss_assigning_directions(self) -> None:
        if self.skip(self.subscene_9_discuss_assigning_directions):
            return

        voiceover = """
        Our next task is to assign directions to edges of the subgraphs.

        The arrows in the front-back subgraph will point from front to back.
        The arrows in the top-bottom subgraph will point from top to bottom.
        Each node must have one edge coming into it and one edge going out of it
        to ensure that no colour is repeated on any of the sides.
        
        Here is one way to assign directions.
        """
        self.say(voiceover)

    def subscene_11_convert_subgraphs_to_solution(self) -> None:
        if self.skip(self.subscene_11_convert_subgraphs_to_solution):
            return

        voiceover: str = """
        We now have found front-back and top-bottom subgraphs the satisfy all the required conditions.
        Each subgraph contains one edge from each cube.
        No edge appears in both subgraphs.
        Each node has degree 2.
        Each node has one in-coming edge and one out-going edge.
        Our final step is to convert these subgraphs into cube orientations which,
        by construction, solve the puzzle. 
        
        Ingenious, isn't it!
        """
        self.say(voiceover)

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        # add the total graph at the initial position from the end of previous scene
        self.puzzle = WINNING_MOVES_PUZZLE
        self.start_centre = 4.0 * RIGHT + DOWN
        self.end_centre = 1.0 * DOWN

        self.total_graph = OppositeFaceGraph(self.puzzle, self.start_centre)
        full_subgraph: EdgeToSubgraphMapping = self.total_graph.mk_subgraph_for_flag(True)
        self.total_graph.set_subgraph(full_subgraph)
        self.add(self.total_graph)

        self.subscene_1_discuss_opposite_face_graph()

        # move the full graph from start_centre to end_centre
        self.play(self.total_graph.animate.shift(self.end_centre - self.start_centre))

        # create and display the 3D puzzle
        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        projection: Projection = mk_standard_orthographic_projection()

        self.puzzle3d = mk_standard_puzzle3d(puzzle_spec, projection)
        self.add(self.puzzle3d)

        self.initial_gap = self.puzzle3d.get_cube_gap()
        self.min_gap = DEFAULT_BUFF
        self.puzzle_face_labeller = PuzzleFaceLabeller(self, self.puzzle3d)

        # create the labels for the puzzle and add them to the scene
        self.puzzle_face_labeller.update_puzzle_texts()
        self.wait(1.0)

        self.subscene_2_discuss_subgraphs()

        # TO DO: use the class that models the pair of labelled subgraphs
        front_graph: OppositeFaceGraph = OppositeFaceGraph(self.puzzle, 4.5 * LEFT + self.end_centre)
        top_graph: OppositeFaceGraph = OppositeFaceGraph(self.puzzle, 4.5 * RIGHT + self.end_centre)
        self.front_graph = front_graph
        self.top_graph = top_graph

        front_text: Tex = Tex("front-back", color=BLACK, font_size=36)
        top_text: Tex = Tex("top-bottom", color=BLACK, font_size=36)
        self.front_text = front_text
        self.top_text = top_text

        front_text.next_to(front_graph, 2.0 * DOWN, buff=0.5)
        top_text.next_to(top_graph, 2.0 * DOWN, buff=0.5)

        animations: list[Animation] = [FadeIn(front_graph), FadeIn(front_text), FadeIn(top_graph), FadeIn(top_text)]
        self.play(AnimationGroup(animations), lag_ratio=0.5)

        self.subscene_3_discuss_starting_arrangement()

        self.subscene_4_discuss_finding_subgraphs()

        # the previous subscene creates the solution
        if self.skip(self.subscene_4_discuss_finding_subgraphs):
            graph_solver: GraphSolver = GraphSolver(self.puzzle)
            graph_solver.solve()
            self.move_solution(graph_solver, 0, self.total_graph, front_graph, top_graph)

        # fade out the total graph in preparation for entry to GraphTheoryScene5
        self.play(FadeOut(self.total_graph))

        self.subscene_9_discuss_assigning_directions()

        # assign directions to subgraph edges
        subgraph: OppositeFaceGraph
        for subgraph in (front_graph, top_graph):
            cube_edge_tips: CubeEdgeTip = mk_edge_directions(subgraph)
            for edge_tip in cube_edge_tips.values():
                self.play(FadeIn(edge_tip.tip), run_time=0.5)

        self.subscene_11_convert_subgraphs_to_solution()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            self.subscene_1_discuss_opposite_face_graph,
            self.subscene_2_discuss_subgraphs,
            self.subscene_3_discuss_starting_arrangement,
            self.subscene_4_discuss_finding_subgraphs,
            self.subscene_9_discuss_assigning_directions,
            self.subscene_11_convert_subgraphs_to_solution,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene4()
        scene.render()
