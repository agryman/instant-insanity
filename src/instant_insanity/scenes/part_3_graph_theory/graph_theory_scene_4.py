"""
This module animates the search for the two subgraphs of the opposite-face graph of a puzzle.
"""

from typing import Sequence

from manim import tempconfig, UP, DOWN, LEFT, RIGHT, Tex, Dot, FadeIn, FadeOut, Mobject, Animation, AnimationGroup
from manim.typing import Vector3D, Point3D
from manim.utils.color.X11 import BLACK
from manim_voiceover import VoiceoverScene

from instant_insanity.core.cube import FacePlane
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.puzzle import Puzzle, PuzzleCubeNumber, AxisLabel, CubeAxis, WINNING_MOVES_PUZZLE
from instant_insanity.mobjects.labelled_edge import LabelledEdge
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, EdgeToSubgraphMapping, mk_edge_directions
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
    start_centre: Point3D
    end_centre: Point3D
    total_graph: OppositeFaceGraph

    def subscene_1a_discuss_opposite_face_graph(self) -> None:
        if self.skip(self.subscene_1a_discuss_opposite_face_graph):
            return

        voiceover: str = """
        We've converted the puzzle into its corresponding opposite-face graph. 
        Now we'll use it to solve the puzzle.
        Let's focus on it.
        """
        self.say(voiceover)

    def subscene_1b_discuss_opposite_face_graph(self) -> None:
        if self.skip(self.subscene_1b_discuss_opposite_face_graph):
            return

        voiceover: str = """
        The reason that we created the graph is that it makes solving the puzzle easy.
        The solution proceeds in two stages.
        First, we'll solve the front-back side, and then we'll solve the top-bottom side.
        This strategy works because once we've fixed the front and back faces of a cube we can still rotate it
        about its x-axis without changing the colours of the front and back faces.

        TO DO: show a cube rotating about its x-axis.
        """
        self.say(voiceover)

        voiceover = """
        Suppose we are given an orientation for each cube such that 
        the front and back sides of the row each contain all four colours.
        This gets us halfway to a solution of the puzzle.
        Here's where the opposite-face graph comes in. 
        The front-back orientation of a cube corresponds to an edge in the opposite-face graph that connects the
        colours of the front and back faces.
        This leads us to the graph theory concept of subgraphs.
         """
        self.say(voiceover)

    def subscene_2_discuss_subgraphs(self) -> None:
        if self.skip(self.subscene_2_discuss_subgraphs):
            return

        topic: Mobject = self.mk_topic("subgraph")
        discussion: str = """
        In graph theory, a subgraph of a given graph G is a subset of the nodes and edges of G that themselves
        form a graph.
        TO DO: show an example subgraph of the opposite-face graph.
        """
        self.play(FadeOut(self.total_graph))
        self.discuss_mobject(topic, discussion)
        self.play(FadeIn(self.total_graph))

    def subscene_3_discuss_front_back_subgraph(self) -> None:
        if self.skip(self.subscene_3_discuss_front_back_subgraph):
            return

        voiceover: str = """
        We'll refer to the subgraph that corresponds to a front-back solution as a front-back subgraph.
        A front-back solution defines a front-back orientation for each cube.
        Therefore, the front-back subgraph must contain exactly one edge for each of the four cubes.
        Furthermore, each colour must appear exactly once on the front side and once on the back side.
        This can happen in two ways, namely the colour appears on the front and back faces of the same cube
        or the colour appears on the front face of one cube and on the back face of another distinct cube.
        If the colour appears on the same cube then the subgraph has a loop at the node for the colour.
        Otherwise, the colour appears on two distinct cubes and therefore has two distinct edges that connect it,
        one edge for each of the two cubes.

        TO DO: Point out that edges 1z and 2y are loops.

        Counting the number of edges incident on a node leads us to the graph theory concept of node degrees.
        """
        self.say(voiceover)

    def subscene_4_discuss_node_degrees(self) -> None:
        if self.skip(self.subscene_4_discuss_node_degrees):
            return

        self.play(FadeOut(self.total_graph))
        topic: Mobject = self.mk_topic("in-degree, out-degree, total degree")
        discussion = """
        We often need to talk about the number of edges that are incident on a node.
        This number is called the total degree of the node, or simply its degree.
        In a directed graph, the number of edges that point out of a node is called its out-degree
        and the number of edges that point into a node is called its in-degree.
        The sum of the in-degree and the out-degree equals the total degree.
        """
        self.discuss_mobject(topic, discussion)

        # example directed graph
        image: Mobject = self.get_image("example-directed-graph.png", GRAPH_THEORY_LATEX)
        discussion = """
        Here's our toy directed graph again.
        """
        self.discuss_mobject(image, discussion)

        # example-degree-table.png
        image = self.get_image("example-degree-table.png", GRAPH_THEORY_LATEX)
        discussion = """
        We can summarize the degree information in a table with one row for each node.
        Here's the degree table for our toy directed graph.

        TO DO: put the graph and table on the screen side-by-side.
        Show graph first. Shrink it and move it to the left.
        Fade in the degree table on the right.
        Then do the same for the opposite-face graph and its table.
        """
        self.discuss_mobject(image, discussion)
        self.play(FadeIn(self.total_graph))

    def subscene_5_discuss_solving_the_puzzle(self) -> None:
        if self.skip(self.subscene_5_discuss_solving_the_puzzle):
            return

        voiceover: str = """
                Our next step is to solve the front-back and top-bottom sides.
                Solving a pair of opposite sides requires us to select one opposite-face pair from each cube
                such that no colour is repeated along each side. 
                We therefore need to find a subgraph that has exactly one edge for each cube
                and each node has degree two.
                This leads us to the graph theory concept of 2-factors.
                """
        self.say(voiceover)

    def subscene_6_discuss_2_factors(self) -> None:
        if self.skip(self.subscene_6_discuss_2_factors):
            return
        topic: Mobject = self.mk_topic("spanning subgraphs, 2-factors")
        discussion: str = """
        A spanning subgraph is a subgraph that contains all the nodes of a graph.
        A 2-factor is a spanning subgraph such that each node has degree 2.

        TO DO: show a 2-factor of the opposite-face graph.
        """
        self.play(FadeOut(self.total_graph))
        self.discuss_mobject(topic, discussion)
        self.play(FadeIn(self.total_graph))


    def subscene_7_discuss_finding_2_factors(self) -> None:
        if self.skip(self.subscene_7_discuss_finding_2_factors):
            return

        voiceover: str = """
        A pair of 2-factors is said to be independent if they have no edges in common.
        Our task now is to find two independent 2-factors of the full opposite-face graph,
        one for the front-back side and another for the top-bottom side.

        TO DO: Ask the viewer to see if they can see a 2-factor.
        Highlight the nodes and edges briefly as they are mentioned.
        Move the edges and back them out when we hit a dead end.
        
        Look at the 1z loop. Suppose it is in a 2-factor.
        Now consider the blue loop 2y. This fixes the colours red and blue and cubes 1 and 2.
        We therefore need to add white and green for cubes 3 and 4. There are no
        green or white loops so we need to use a pair of edges that connect green and white.
        But there is no such edge for cube 3. Therefore our choice of the blue loop for cube 2
        leads to a dead end when we use the red loop on cube one.
        So if we use the red loop at cube one then we cannot use any other loops and so
        we must connect the blue, green and white nodes with edges that form a triangle.
        But there is no edge that connects blue and green.
        Therefore when we try to use the red loop, we hit a dead end.
        This proves that the 1z red loop cannot be part of any solution.

        But there are only three edges for cube 1 so we must use edges 1x and 1y in the solution.
        Let's arbitrarily put 1x in the front-back subgraph and 1y in the top-bottom subgraph.

        Let's focus on the front-back subgraph which now must contain edge 1x. 
        Suppose the edges form a square.
        The combination 1x, 2x, 3y, 4x forms a 2-factor. 

        Can we find an independent 2-factor for the top-bottom subgraph?
        It must contain the edge 1y.
        The combination 1y, 2z, 3z, 4z forms and independent 2-factor.

        We have therefore solved the puzzle by applying visual reasoning to the opposite-face graph.
        Let's animate this solution.
        """
        self.say(voiceover)

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
                  run_time=1.0)
        self.remove(moving_edge, moving_start_dot, moving_end_dot)
        target_graph.set_subgraph_edge(cube_axis, True)

        self.wait()

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        # add the total graph at the initial position from the end of previous scene
        self.puzzle = WINNING_MOVES_PUZZLE
        self.start_centre = 4 * RIGHT + DOWN
        self.end_centre = 2 * UP
        self.total_graph = OppositeFaceGraph(self.puzzle, self.start_centre)
        full_subgraph: EdgeToSubgraphMapping = self.total_graph.mk_subgraph_for_flag(True)
        self.total_graph.set_subgraph(full_subgraph)
        self.add(self.total_graph)

        self.subscene_1a_discuss_opposite_face_graph()

        # move the full graph from start_centre to end_centre
        self.play(self.total_graph.animate.shift(self.end_centre - self.start_centre))

        self.subscene_1b_discuss_opposite_face_graph()

        self.subscene_2_discuss_subgraphs()

        self.subscene_3_discuss_front_back_subgraph()

        self.subscene_4_discuss_node_degrees()

        self.subscene_5_discuss_solving_the_puzzle()

        self.subscene_6_discuss_2_factors()

        self.subscene_7_discuss_finding_2_factors()

        self.subscene_8_animate_finding_2_factors()

        front_graph: OppositeFaceGraph = OppositeFaceGraph(self.puzzle, 4 * LEFT + 1.5 * DOWN)
        top_graph: OppositeFaceGraph = OppositeFaceGraph(self.puzzle, 4 * RIGHT + 1.5 * DOWN)

        front_text: Tex = Tex("front-back", color=BLACK, font_size=36)
        top_text: Tex = Tex("top-bottom", color=BLACK, font_size=36)

        front_text.next_to(front_graph, DOWN, buff=0.5)
        top_text.next_to(top_graph, DOWN, buff=0.5)

        animations: list[Animation] = [FadeIn(front_graph), FadeIn(front_text), FadeIn(top_graph), FadeIn(top_text)]
        self.play(AnimationGroup(animations), lag_ratio=0.5)

        graph_solver: GraphSolver = GraphSolver(self.puzzle)
        graph_solver.solve()

        self.move_solution(graph_solver, 0, self.total_graph, front_graph, top_graph)

        self.subscene_8_animate_finding_2_factors()

        self.subscene_9_discuss_assigning_directions()

        # TODO: fade in the tips following the directed path
        subgraph: OppositeFaceGraph
        for subgraph in (front_graph, top_graph):
            cube_edge_tips: CubeEdgeTip = mk_edge_directions(subgraph)
            for edge_tip in cube_edge_tips.values():
                self.play(FadeIn(edge_tip.tip), run_time=0.5)

        self.subscene_10_discuss_solution_symmetries()

        self.subscene_11_convert_subgraphs_to_solution()

        # fade out the total graph in preparation for entry to the next scene CubesFromSubgraphs
        self.play(FadeOut(self.total_graph))

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            self.subscene_11_convert_subgraphs_to_solution,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene4()
        scene.render()
