"""
This module animates the search for the two subgraphs of the opposite-face graph of a puzzle.
"""

from typing import Sequence

from manim import tempconfig, DOWN, LEFT, RIGHT, Tex, Dot, FadeIn, FadeOut, Mobject, Animation, AnimationGroup, Indicate
from manim.typing import Vector3D, Point3D
from manim.utils.color.X11 import BLACK
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

GRAPH_THEORY_LATEX: str = "graph_theory.latex"

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

    def subscene_1_discuss_opposite_face_graph(self) -> None:
        if self.skip(self.subscene_1_discuss_opposite_face_graph):
            return

        voiceover: str = """
        We'll now explain how to use the opposite-face graph to solve the puzzle.
        
        Our solution strategy is to first solve the front-back sides and
        then solve the top-bottom sides while preserving the front-back sides.
        """
        self.say(voiceover)

    def subscene_2_discuss_starting_arrangement(self) -> None:
        if self.skip(self.subscene_2_discuss_starting_arrangement):
            return

        self.say("""
        A subgraph of a graph is a subset of its nodes and edges that themselves define a graph.
        We'll build up the front-back and top-bottom solutions in subgraphs of the opposite-face graph.
        
        A spanning subgraph is a subgraph that contains all the nodes of the graph.
        The front-back and top-bottom subgraphs are spanning subgraphs since they contain all four colour nodes.
        
        Any arrangement of the cubes defines a front-back subgraph and a top-bottom subgraph.
        Let's see what this looks like for the starting arrangement of the puzzle.
        """)

        self.say("""
        The front face of each cube in the starting arrangement is labelled ex.
        """)
        self.puzzle_face_labeller.indicate_face_labels(self, FacePlane.FRONT)

        self.say("""
        So move all the ex edges from the opposite-face graph to the front-back subgraph.
        """)
        for cube in PuzzleCubeNumber:
            self.move_edge((cube, AxisLabel.X), self.total_graph, self.front_graph, run_time=0.5)

        self.say("""
        Similarly, The top face of each cube in the starting arrangement is labelled zed.
        """)
        self.puzzle_face_labeller.indicate_face_labels(self, FacePlane.TOP)

        self.say("""
        So move all the zed edges from the opposite-face graph to the top-bottom subgraph.
        """)
        for cube in PuzzleCubeNumber:
            self.move_edge((cube, AxisLabel.Z), self.total_graph, self.top_graph, run_time=0.5)

        self.say("""
        We know that the starting arrangment is not a solution and this fact
        shows up clearly in the subgraphs.

        The degree of a node is the number of edges that are incident on it.
        A loop contributes 2 to the degree.
        """)

        self.say("""
        In a solution, each colour must appear once on the front side
        and once on the back side.
        This means that each node in the front-back subgraph
        must have degree two.

        A spanning subgraph in which each node has degree two is called a 2-factor of the graph.
        The front-back subgraph of a solution must be a 2-factor of the opposite-face graph.

        But this is not the case for the starting arrangement of the puzzle. 

        Look at the red node.
        """)

        red_node: Dot = self.front_graph.get_node_by_colour(FaceColour.RED)
        red_colour: str = str(MANIM_COLOUR_MAP[FaceColour.RED])
        scale_factor: float = 1.5
        self.play(Indicate(red_node, color=red_colour), scale_factor=scale_factor)

        self.say("""
        It has degree 3.
        
        Look at the blue node.
        """)

        blue_node: Dot = self.front_graph.get_node_by_colour(FaceColour.BLUE)
        blue_colour: str = str(MANIM_COLOUR_MAP[FaceColour.BLUE])
        self.play(Indicate(blue_node, color=blue_colour), scale_factor=scale_factor)

        self.say("""
        It has degree 1.

        Similarly, the top-bottom subgraph of a solution must be a 2-factor of the opposite-face graph.
        But this is not the case for the starting arrangement since again the red node has degree 3
        """)
        red_node = self.top_graph.get_node_by_colour(FaceColour.RED)
        self.play(Indicate(red_node, color=red_colour), scale_factor=scale_factor)

        self.say("""
        and the blue node has degree 1.
        """)
        blue_node = self.top_graph.get_node_by_colour(FaceColour.BLUE)
        self.play(Indicate(blue_node, color=blue_colour), scale_factor=scale_factor)

        self.say("""
        Two subgraphs are said to be independent if they have no edges in common.
        In a solution, every edge of the opposite-face graph must be either 
        an edge of the front-back subgraph, 
        an edge of the top-bottom subgraph, 
        or not be part of the solution.
        This means that the front-back and top-bottom subgraphs of a solution must be independent.
        In fact, the two subgraphs must be independent 2-factors of the opposite-face graph.

        Now we know what the two subgraphs for a solution look like.
        Let's restore the opposite-face graph and try to find a pair of independent 2-factors
        of the opposite-face graph.
        """)

        # restore the opposite-face graph in reverse order, i.e. undo top then undo front
        for cube_axis, source_graph in zip([AxisLabel.Z, AxisLabel.X], [self.top_graph, self.front_graph]):
            for cube in PuzzleCubeNumber:
                self.move_edge((cube, cube_axis), source_graph, self.total_graph, run_time=0.25)

    def subscene_7_discuss_finding_2_factors(self) -> None:
        if self.skip(self.subscene_7_discuss_finding_2_factors):
            return

        voiceover: str = """
        Converting the puzzle into the opposite-face graph doesn't automatically solve the puzzle.
        It just dramatically reduces the search space.
        We still have to apply our powers of visual reasoning to find a solution.
        """
        self.say(voiceover)

        voiceover = """
        Let's start with the front-back subgraph and see if the 1 zed loop is part of the solution.
        Let's tentatively move it into the subgraph.
        """
        self.say(voiceover)
        self.move_edge((PuzzleCubeNumber.ONE, AxisLabel.Z), self.total_graph, self.front_graph, run_time=1.0)

        voiceover = """
        The front-back subgraph now has an edge from cube 1 
        so we can ignore the 1 ex and 1 wy edges in the opposite-face graph.
        Let's hide them temporarily. 
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.ONE, AxisLabel.X), False)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.ONE, AxisLabel.Y), False)

        voiceover = """
        The red node already has degree 2 so we can't use edges from cubes 2, 3, or 4 that touch red.
        Let's temporarily hide edges 3 zed, 2 ex, 3 ex, and 4 ex. 
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.Z), False)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.X), False)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.X), False)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.FOUR, AxisLabel.X), False)

        voiceover = """
        Now let's see if edge 2 wy can be part of the solution.
        Tentatively move it into the front-back subgraph.
        """
        self.say(voiceover)
        self.move_edge((PuzzleCubeNumber.TWO, AxisLabel.Y), self.total_graph, self.front_graph, run_time=1.0)

        voiceover = """
        Now we have edges from cubes 1 and 2 so we can't use the 2 zed edge.
        Also, the blue node already has degree 2 so we can't use the 3 wy or 4 zed edges.
        Temporarily hide edges 2 zed, 3 wy, and 4 zed.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.Z), False)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.Y), False)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.FOUR, AxisLabel.Z), False)

        voiceover = """
        Now we've hit a dead end because we have no available edges from cube 3.
        We have to backtrack to the point where we added edge 2 wy and try a different edge from cube 2.
        """
        self.say(voiceover)


        self.wait(5.0)

        voiceover = """
        The red node now has degree 2 so we cannot add another edge that touches a red node.
        The opposite-face graph now has 5 edges that touch red, namely 
        Let's hide those.
        """

        # voiceover = """
        # Look at the 1z loop. Suppose it is in a 2-factor.
        # Now consider the blue loop 2y. This fixes the colours red and blue and cubes 1 and 2.
        # We therefore need to add white and green for cubes 3 and 4. There are no
        # green or white loops so we need to use a pair of edges that connect green and white.
        # But there is no such edge for cube 3. Therefore our choice of the blue loop for cube 2
        # leads to a dead end when we use the red loop on cube one.
        # So if we use the red loop at cube one then we cannot use any other loops and so
        # we must connect the blue, green and white nodes with edges that form a triangle.
        # But there is no edge that connects blue and green.
        # Therefore when we try to use the red loop, we hit a dead end.
        # This proves that the 1z red loop cannot be part of any solution.
        # """
        # self.say(voiceover)
        #
        # voiceover = """
        # But there are only three edges for cube 1 so we must use edges 1x and 1y in the solution.
        # Let's arbitrarily put 1x in the front-back subgraph and 1y in the top-bottom subgraph.
        # """
        # self.say(voiceover)
        #
        # voiceover = """
        # Let's focus on the front-back subgraph which now must contain edge 1x.
        # Suppose the edges form a square.
        # The combination 1x, 2x, 3y, 4x forms a 2-factor.
        # """
        # self.say(voiceover)
        #
        # voiceover = """
        # Can we find an independent 2-factor for the top-bottom subgraph?
        # It must contain the edge 1y.
        # The combination 1y, 2z, 3z, 4z forms and independent 2-factor.
        # """
        # self.say(voiceover)
        #
        # voiceover = """
        # We have therefore solved the puzzle by applying visual reasoning to the opposite-face graph.
        # Let's animate this solution.
        # """
        # self.say(voiceover)

    def subscene_8_animate_finding_2_factors(self) -> None:
        if self.skip(self.subscene_8_animate_finding_2_factors):
            return

        voiceover = """
        We'll start by drawing their nodes and then add their edges.
        Above we proved that the 1z loop on red cannot be part of any solution.
        Therefore, the solution must use the 1x and 1y edges.
        We arbitrarily put the 1x edge in the front-back subgraph which forces
        the 1y edge to go into the top-bottom subgraph.
        We then observed that the solution 2-factors must form squares.
        """
        self.say(voiceover)


    def subscene_9_discuss_assigning_directions(self) -> None:
        if self.skip(self.subscene_9_discuss_assigning_directions):
            return

        voiceover = """
        Our next task is to orient the cubes. The 2-factors
        tell us which pair of opposite faces appear on the front and back
        sides and which appear on the top and bottom sides. 
        We need to give each edge a direction.
        The arrows in the front-back 2-factor point from front to back.
        The arrows in the top-bottom 2-factor point from top to bottom.
        The actual direction is arbitrary except that all the directions
        must be consistent with each other.
        Each node must have one edge coming into it and 
        one edge going out of it. 
        This rule ensures that no colour is repeated on any of the sides.
        TO DO: improve the continuity of fading in the tips
        TO DO: For example, in the front-back 2-factor the edge for cube 1
        connects etc.
        
        Here is one way to do this.
        """
        self.say(voiceover)

    def subscene_10_discuss_solution_symmetries(self) -> None:
        if self.skip(self.subscene_10_discuss_solution_symmetries):
            return

        voiceover: str = """
        A pair of valid independent directed 2-factors has several symmetries
        in the sense that we can modify the 2-factors in certain ways that
        define distinct, but essentially equivalent solutions.
        We can interchange the front-back 2-factor with 
        the top-bottom 2-factor.
        We can reverse the directions of the front-back 2-factor.
        We can reverse the directions of the top-bottom 2-factor.
        We therefor have three independent 2-fold symmetries of the 2-factors, 
        giving a total of eight distinct, but essentially equivalent, solutions. 
        TO DO: do the math and maybe animate the eight solutions.
        """
        self.say(voiceover)

    def subscene_11_convert_subgraphs_to_solution(self) -> None:
        if self.skip(self.subscene_11_convert_subgraphs_to_solution):
            return

        voiceover: str = """
        We now have found two independent 2-factors of the full opposite-face graph
        and given them directions.
        Our final step is to convert this information into cube orientations which,
        by construction, solve the puzzle. Ingenious, isn't it!
        """
        self.say(voiceover)

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
                  run_time: float = 1.0) -> None:
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

        self.wait()

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        # add the total graph at the initial position from the end of previous scene
        self.puzzle = WINNING_MOVES_PUZZLE
        self.start_centre = 4 * RIGHT + DOWN
        self.end_centre = 1.5 * DOWN

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

        # TO DO: use the class that models the pair of labelled subgraphs
        front_graph: OppositeFaceGraph = OppositeFaceGraph(self.puzzle, 4 * LEFT + self.end_centre)
        top_graph: OppositeFaceGraph = OppositeFaceGraph(self.puzzle, 4 * RIGHT + self.end_centre)
        self.front_graph = front_graph
        self.top_graph = top_graph

        front_text: Tex = Tex("front-back", color=BLACK, font_size=36)
        top_text: Tex = Tex("top-bottom", color=BLACK, font_size=36)
        self.front_text = front_text
        self.top_text = top_text

        front_text.next_to(front_graph, DOWN, buff=0.5)
        top_text.next_to(top_graph, DOWN, buff=0.5)

        animations: list[Animation] = [FadeIn(front_graph), FadeIn(front_text), FadeIn(top_graph), FadeIn(top_text)]
        self.play(AnimationGroup(animations), lag_ratio=0.5)

        self.subscene_2_discuss_starting_arrangement()

        self.subscene_7_discuss_finding_2_factors()

        self.subscene_8_animate_finding_2_factors()

        # graph_solver: GraphSolver = GraphSolver(self.puzzle)
        # graph_solver.solve()
        # self.move_solution(graph_solver, 0, self.total_graph, front_graph, top_graph)
        #
        # self.subscene_8_animate_finding_2_factors()
        #
        # self.subscene_9_discuss_assigning_directions()
        #
        # # TODO: fade in the tips following the directed path
        # subgraph: OppositeFaceGraph
        # for subgraph in (front_graph, top_graph):
        #     cube_edge_tips: CubeEdgeTip = mk_edge_directions(subgraph)
        #     for edge_tip in cube_edge_tips.values():
        #         self.play(FadeIn(edge_tip.tip), run_time=0.5)

        self.subscene_10_discuss_solution_symmetries()

        self.subscene_11_convert_subgraphs_to_solution()

        # fade out the total graph in preparation for entry to the next scene CubesFromSubgraphs
        self.play(FadeOut(self.total_graph))

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            # self.subscene_1_discuss_opposite_face_graph,
            # self.subscene_2_discuss_starting_arrangement,
            self.subscene_7_discuss_finding_2_factors,
            # self.subscene_8_animate_finding_2_factors,
            # self.subscene_9_discuss_assigning_directions,
            # self.subscene_10_discuss_solution_symmetries,
            # self.subscene_11_convert_subgraphs_to_solution,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene4()
        scene.render()
