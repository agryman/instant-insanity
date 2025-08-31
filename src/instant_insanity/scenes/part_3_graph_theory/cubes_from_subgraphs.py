"""
This module animates the conversion of the subgraphs into a solution of the puzzle.
The scene starts with the two subgraphs on the bottom half the of the frame and nothing
in the top half. The state of the scene is determined by the puzzle and the solution number.
Recall that Carteblanche's puzzle has two solutions.
"""
from manim import Scene, tempconfig, LEFT, DOWN, RIGHT, Tex, BLACK

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FaceName
from instant_insanity.core.puzzle import Puzzle, WINNING_MOVES_PUZZLE, PuzzleCubeNumber, AxisLabel
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, EdgeToSubgraphMapping
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.solvers.graph_solver import GraphSolver, Grid, GridValue


class CubesFromSubgraphs(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        puzzle: Puzzle =  WINNING_MOVES_PUZZLE
        front_graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, 4 * LEFT + 1.5 * DOWN)
        top_graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, 4 * RIGHT + 1.5 * DOWN)

        subgraphs: dict[FaceName, OppositeFaceGraph] = {
            FaceName.FRONT: front_graph,
            FaceName.TOP: top_graph,
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

        self.wait()

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = CubesFromSubgraphs()
        scene.render()
