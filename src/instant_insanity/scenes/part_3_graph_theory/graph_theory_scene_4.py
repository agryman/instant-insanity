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

        The degree of a node is the number of edges that are connected to it.
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

        Now we know what the two subgraphs for a solution should look like.
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
        Converting the puzzle into the opposite-face graph doesn't automatically solve it for us.
        We still need to search it for a solution.
        However, using the opposite-face graph dramatically reduces the search space and it helps us use 
        our powers of visual reasoning to find a solution.
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
        The red node already has degree 2 so we can't add edges that touch red.
        Let's temporarily hide edges 2 ex, 3 ex, 3 zed, and 4 ex. 
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
        Now the front-back subgraph has an edge from cube 2 so we can't use edge 2 zed. 
        Temporarily hide it.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.Z), False)

        voiceover = """
        The blue node already has degree 2 so we can't use the 3 wy or 4 zed edges
        since they touch blue.
        Temporarily hide them.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.Y), False)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.FOUR, AxisLabel.Z), False)


        voiceover = """
        Now we've hit a dead end because the front-back subgraph still needs an edge from cube 3 but none are available.
        We have to backtrack to the point where we added edge 2 wy and try a different edge from cube 2.
        Show the edges we just hid and move edge 2 wy back to the opposite-face graph.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.Z), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.Y), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.FOUR, AxisLabel.Z), True)
        self.move_edge((PuzzleCubeNumber.TWO, AxisLabel.Y), self.front_graph, self.total_graph, run_time=1.0)

        voiceover = """
        We just showed that using edge 2 wy leads to a dead end, so temporarily hide it.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.Y), False)

        voiceover = """
        We need edges from cubes 2, 3, and 4. 
        The only available edges from cubes 2 and 3 are 2 zed and 3 wy so we are forced to use them. 
        Move them into the front-back subgraph.
        """
        self.say(voiceover)
        self.move_edge((PuzzleCubeNumber.TWO, AxisLabel.Z), self.total_graph, self.front_graph, run_time=1.0)
        self.move_edge((PuzzleCubeNumber.THREE, AxisLabel.Y), self.total_graph, self.front_graph, run_time=1.0)

        voiceover = """
        To complete the front-back subgraph we need an edge from cube 4 that connects green and blue.
        However, no such edge is available so we've hit another dead end.
        Backtrack to the point where we added edge 1 zed.
        """
        self.say(voiceover)
        self.move_edge((PuzzleCubeNumber.TWO, AxisLabel.Z), self.front_graph, self.total_graph, run_time=1.0)
        self.move_edge((PuzzleCubeNumber.THREE, AxisLabel.Y), self.front_graph, self.total_graph, run_time=1.0)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.Y), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.Z), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.X), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.X), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.FOUR, AxisLabel.X), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.ONE, AxisLabel.X), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.ONE, AxisLabel.Y), True)
        self.move_edge((PuzzleCubeNumber.ONE, AxisLabel.Z), self.front_graph, self.total_graph, run_time=1.0)

        voiceover = """
        It looks like we're back to square one, but we have discovered one valuable piece of new information.
        We proved that using edge 1 zed leads to a dead end, so it can't be part of the solution.
        Hide it.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.ONE, AxisLabel.Z), False)

        voiceover = """
        Now there are only two available edges from cube 1, namely 1 ex and 1 wy.
        One of those must go into the front-back subgraph and the other must go into the top-bottom subgraph.
        The choice of which goes where is arbitrary but 
        let's move 1 ex into the front-back subgraph and 1 wy into the top-bottom subgraph
        since that matches the starting orientation of cube 1.
        """
        self.say(voiceover)
        self.move_edge((PuzzleCubeNumber.ONE, AxisLabel.X), self.total_graph, self.front_graph, run_time=1.0)
        self.move_edge((PuzzleCubeNumber.ONE, AxisLabel.Y), self.total_graph, self.top_graph, run_time=1.0)

        voiceover = """
        This choice reduces the number of rotations we will have to do 
        to turn the starting arrangement into the solution.

        Let's see if 2 wy can be part of the front-back subgraph.
        Tentatively move it there.
        """
        self.say(voiceover)
        self.move_edge((PuzzleCubeNumber.TWO, AxisLabel.Y), self.total_graph, self.front_graph, run_time=1.0)

        voiceover = """
        Now the front-back subgraph contains an edge from cube 2 so edges 2 ex and 2 zed cannot be part of it.
        Temporarily hide them.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.X), False)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.Z), False)

        voiceover = """
        The blue node of the front-back subgraph has degree two so no other edges that touch blue
        can be part of it.
        Temporarily hide edges 3 wy, 4 ex, and 4 zed.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.Y), False)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.FOUR, AxisLabel.X), False)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.FOUR, AxisLabel.Z), False)

        voiceover = """
        The front-back subgraph needs edges from cubes 3 and 4.
        The only edge available from cube 4 is 4 wy so move it.
        """
        self.say(voiceover)
        self.move_edge((PuzzleCubeNumber.FOUR, AxisLabel.Y), self.total_graph, self.front_graph, run_time=1.0)

        voiceover = """
        To complete the front-back subgraph we need a loop on the red node.
        However, no such edge is available so we've hit another dead end.
        Therefore edge 2 wy cannot be part of the front-back subgraph.
        Backtrack to the point before we moved it into the front-back subgraph.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.Y), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.FOUR, AxisLabel.X), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.FOUR, AxisLabel.Z), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.X), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.Z), True)
        self.move_edge((PuzzleCubeNumber.FOUR, AxisLabel.Y), self.front_graph, self.total_graph, run_time=1.0)
        self.move_edge((PuzzleCubeNumber.TWO, AxisLabel.Y), self.front_graph, self.total_graph, run_time=1.0)

        voiceover = """
        We just proved that edge 2 wy cannot be part of the front-back subgraph.
        
        The blue node in the top-bottom subgraph has degree one.
        Edge 2 wy is a loop so it cannot be part of the top-bottom subgraph
        since that would increase the degree of the blue node to three. 
        
        Therefore edge 2 wy cannot be part of the solution so hide it.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.Y), False)

        voiceover = """
        Let's see if edge 3 ex can be part of the front-back subgraph.
        Tentatively move it.
        """
        self.say(voiceover)
        self.move_edge((PuzzleCubeNumber.THREE, AxisLabel.X), self.total_graph, self.front_graph, run_time=1.0)

        voiceover = """
        The front-back subgraph now has an edge from cube 3 so temporarily hide edges 3 wy and 3 zed in
        the opposite-face graph.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.Y), False)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.Z), False)

        voiceover = """
        The white node in the front-back subgraph has degree two so no other edges that touch white
        can be part of it.
        Temporarily hide edges 2 zed, 4 wy, and 4 zed.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.Z), False)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.FOUR, AxisLabel.Y), False)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.FOUR, AxisLabel.Z), False)

        voiceover = """
        The front-back subgraph needs edges from cubes 2 and 4 but there are only one of each available.
        However, both of those touch red so adding them would increase the degree of the red node to three.
        We have hit another dead end.
        Backtrack to where we moved edge 3 ex.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.TWO, AxisLabel.Z), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.FOUR, AxisLabel.Y), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.FOUR, AxisLabel.Z), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.Y), True)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.Z), True)
        self.move_edge((PuzzleCubeNumber.THREE, AxisLabel.X), self.front_graph, self.total_graph, run_time=1.0)

        voiceover = """
        Adding edge 3 ex to the front-back subgraph leads to a dead end so hide it.
        """
        self.say(voiceover)
        self.total_graph.set_subgraph_edge((PuzzleCubeNumber.THREE, AxisLabel.X), False)

        voiceover = """
        The graphs are now simple enough for us to see the solution.
        Move edges 2 ex, 3 wy, and 4 ex to the front-back subgraph to complete it.
        """
        self.say(voiceover)
        self.move_edge((PuzzleCubeNumber.TWO, AxisLabel.X), self.total_graph, self.front_graph, run_time=1.0)
        self.move_edge((PuzzleCubeNumber.THREE, AxisLabel.Y), self.total_graph, self.front_graph, run_time=1.0)
        self.move_edge((PuzzleCubeNumber.FOUR, AxisLabel.X), self.total_graph, self.front_graph, run_time=1.0)

        voiceover = """
        Move edges 2 zed, 3 zed, and 4 zed to the top-bottom subgraph to complete it.
        """
        self.say(voiceover)
        self.move_edge((PuzzleCubeNumber.TWO, AxisLabel.Z), self.total_graph, self.top_graph, run_time=1.0)
        self.move_edge((PuzzleCubeNumber.THREE, AxisLabel.Z), self.total_graph, self.top_graph, run_time=1.0)
        self.move_edge((PuzzleCubeNumber.FOUR, AxisLabel.Z), self.total_graph, self.top_graph, run_time=1.0)

        voiceover = """
        The front-back and top-bottom subgraphs are now independent 2-factors of the opposite-face graph.
        We have therefore found the solution.
        It remains to convert this graphical solution into the arrangement of the four cubes that solves the puzzle.
        """

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

        self.subscene_2_discuss_starting_arrangement()

        self.subscene_7_discuss_finding_2_factors()

        # fade out the total graph in preparation for entry to GraphTheoryScene5
        self.play(FadeOut(self.total_graph))

        # the previous subscene creates the solution
        # graph_solver: GraphSolver = GraphSolver(self.puzzle)
        # graph_solver.solve()
        # self.move_solution(graph_solver, 0, self.total_graph, front_graph, top_graph)

        # TODO: improve the continuity of fading in the tips
        # TODO: For example, in the front-back 2-factor the edge for cube 1 connects etc.
        self.subscene_9_discuss_assigning_directions()

        # TODO: fade in the tips following the directed path
        subgraph: OppositeFaceGraph
        for subgraph in (front_graph, top_graph):
            cube_edge_tips: CubeEdgeTip = mk_edge_directions(subgraph)
            for edge_tip in cube_edge_tips.values():
                self.play(FadeIn(edge_tip.tip), run_time=0.5)

        self.subscene_11_convert_subgraphs_to_solution()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            # self.subscene_1_discuss_opposite_face_graph,
            # self.subscene_2_discuss_starting_arrangement,
            # self.subscene_7_discuss_finding_2_factors,
            # self.subscene_9_discuss_assigning_directions,
            # self.subscene_11_convert_subgraphs_to_solution,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene4()
        scene.render()
