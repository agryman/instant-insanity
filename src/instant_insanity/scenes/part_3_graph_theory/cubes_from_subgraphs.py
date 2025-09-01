"""
This module animates the conversion of the subgraphs into a solution of the puzzle.
The scene starts with the two subgraphs on the bottom half the of the frame and nothing
in the top half. The state of the scene is determined by the puzzle and the solution number.
Recall that Carteblanche's puzzle has two solutions.
"""
from manim import Scene, tempconfig, LEFT, DOWN, RIGHT, Tex, BLACK, FadeIn

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FacePlane
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import Puzzle, WINNING_MOVES_PUZZLE, PuzzleCubeNumber, AxisLabel, PuzzleSpec, \
    WINNING_MOVES_PUZZLE_SPEC
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, EdgeToSubgraphMapping, mk_edge_directions
from instant_insanity.mobjects.puzzle_3d import Puzzle3D
from instant_insanity.mobjects.stealth_tip import CubeEdgeTip
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.part_3_graph_theory.construct_graph import ConstructGraph
from instant_insanity.solvers.graph_solver import GraphSolver, Grid, GridValue


class CubesFromSubgraphs(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        puzzle: Puzzle =  WINNING_MOVES_PUZZLE
        front_graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, 4 * LEFT + 1.5 * DOWN)
        top_graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, 4 * RIGHT + 1.5 * DOWN)

        subgraphs: dict[FacePlane, OppositeFaceGraph] = {
            FacePlane.FRONT: front_graph,
            FacePlane.TOP: top_graph,
        }

        front_text: Tex = Tex("front-back", color=BLACK, font_size=36)
        top_text: Tex = Tex("top-bottom", color=BLACK, font_size=36)

        front_text.next_to(front_graph, DOWN, buff=0.5)
        top_text.next_to(top_graph, DOWN, buff=0.5)

        self.add(front_graph, top_graph, front_text, top_text)

        graph_solver: GraphSolver = GraphSolver(puzzle)
        graph_solver.solve()
        solution: Grid = graph_solver.solutions[0]

        # compute the edges in the solution of each subgraph.
        for face_name, graph in subgraphs.items():
            edge_to_subgraph: EdgeToSubgraphMapping = graph.edge_to_subgraph.copy()
            for cube_number in PuzzleCubeNumber:
                grid_value: GridValue = solution[(face_name, cube_number)]
                assert isinstance(grid_value, AxisLabel)
                axis_label: AxisLabel = grid_value
                edge_to_subgraph[(cube_number, axis_label)] = True
            graph.set_subgraph(edge_to_subgraph)

        voiceover_text_1: str = '''We have found the front-back and top-bottom subgraphs.
        In order to interpret these subgraphs as defining the cube orientations, we need
        to give each edge a direction which we'll interpret as saying the edge points from the front face
        to the back face in the front-back subgraph, and from the top face to the bottom face
        in the top-bottom subgraph.

        Furthermore, the edge directions must be consistent with each other so that
        each node has exactly one edge leaving it and exactly one edge entering it.
        For the front-back subgraph, this means that each colour appears
        exactly once on the front row and exactly once on the back row.
        For the top-bottom subgraph, this means that each colour appears
        exactly once on the top row and exactly once on the bottom row.
        In other words, once we have given the edges consistent directions then we
        have solved the puzzle.

        The procedure for assigning consistent edge directions is simple.
        Recall that each each has degree two which means that either two distinct edges
        are incident on it, or that the node has a loop edge.
        This means that once we give an edge a direction, it forces the directions of the other
        edges that are incident on it.

        Start with cube 1 and give it a direction. 
        Then follow the edge around the subgraph, giving each edge your direction of travel.
        If there are any edges that you haven't traversed yet, pick one, give it an arbitrary
        direction and continue following the path until you return to your current starting point.
        Repeat this step until you have traversed all the edges.
        Here is the result for our subgraphs.
        '''

        self.wait(4)

        # assign directions to the edges of the subgraphs
        # TODO: fade in the tips following the directed path
        subgraph: OppositeFaceGraph
        for subgraph in (front_graph, top_graph):
            cube_edge_tips: CubeEdgeTip = mk_edge_directions(subgraph)
            for edge_tip in cube_edge_tips.values():
                self.add(edge_tip.tip)

        self.wait(4)

        #TODO: add the edge direction arrows
        
        voiceover_text_2: str = '''The final step of the process is to create the solution to the puzzle
        by rotating the cubes to match these subgraphs.
         
        Here's the puzzle with its cubes in their starting positions.
        Note that this position is not a solution because...
        
        We need to rotate the cubes to match the subgraphs.
        We'll match the front-back subgraph first and then the top-bottom subgraph.
        For each subgraph, we'll do the matching one cube at a time.
        
        Let's start. Look at edge 1 in the front-back subgraph. It says that the front face
        of cube 1 is <insert colour> and its back face is <insert colour>. These line on
        its <insert axis label> axis.
        Rotate cube 1 to make that axis occupy the front-back position with the
        outgoing node the front and the incoming node the back.
        '''

        projection: Projection = mk_standard_orthographic_projection()

        # create and display the 3D puzzle
        puzzle3d: Puzzle3D = ConstructGraph.mk_puzzle3d(puzzle, projection)
        self.add(puzzle3d)
        self.wait(4)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = CubesFromSubgraphs()
        scene.render()
