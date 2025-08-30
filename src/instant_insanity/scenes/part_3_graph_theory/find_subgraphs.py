"""
This module animates the search for the two subgraphs of the opposite-face graph of a puzzle.
"""

from manim import Scene, tempconfig, UP, DOWN, LEFT, RIGHT, Tex, Dot
from manim.typing import Point3D, Vector3D
from manim.utils.color.X11 import BLACK

from instant_insanity.core.cube import FaceName
from instant_insanity.core.puzzle import WINNING_MOVES_PUZZLE, Puzzle, PuzzleCubeNumber, AxisLabel, CubeAxis
from instant_insanity.mobjects.labelled_edge import LabelledEdge
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, EdgeToSubgraphMapping
from instant_insanity.mobjects.quadrant import NodePair, Quadrant
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.solvers.graph_solver import GraphSolver, Grid


class FindSubgraphs(GridMixin, Scene):
    def construct(self):
        # add three graphs
        puzzle: Puzzle = WINNING_MOVES_PUZZLE

        total_graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, 2 * UP)
        full_subgraph: EdgeToSubgraphMapping = total_graph.mk_subgraph_for_flag(True)
        total_graph.set_subgraph(full_subgraph)

        front_graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, 4 * LEFT + 1.5 * DOWN)
        top_graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, 4 * RIGHT + 1.5 * DOWN)

        front_text: Tex = Tex("front-back", color=BLACK, font_size=36)
        top_text: Tex = Tex("top-bottom", color=BLACK, font_size=36)

        front_text.next_to(front_graph, DOWN, buff=0.5)
        top_text.next_to(top_graph, DOWN, buff=0.5)

        self.add(total_graph, front_graph, top_graph, front_text, top_text)

        # test: move an edge from the total graph to the front graph
        # remove the edge from the top graph
        # move the edge to the front graph
        # add the edge to the front graph
        cube_number: PuzzleCubeNumber = PuzzleCubeNumber.ONE
        axis_label: AxisLabel = AxisLabel.X
        cube_axis: CubeAxis = (cube_number, axis_label)
        # self.move_edge((PuzzleCubeNumber.ONE, AxisLabel.X), total_graph, top_graph)
        # self.move_edge((PuzzleCubeNumber.TWO, AxisLabel.Y), total_graph, front_graph)
        # self.move_edge((PuzzleCubeNumber.ONE, AxisLabel.X), top_graph, front_graph)

        graph_solver: GraphSolver = GraphSolver(puzzle)
        graph_solver.solve()

        self.move_solution(graph_solver, 0, total_graph, front_graph, top_graph)

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

        grid: Grid  = graph_solver.solutions[solution_index]
        grid_key: tuple[FaceName, PuzzleCubeNumber]
        grid_value: AxisLabel | None
        for grid_key, grid_value in grid.items():
            face_name: FaceName = grid_key[0]
            cube_number: PuzzleCubeNumber = grid_key[1]

            assert grid_value is not None
            assert isinstance(grid_value, AxisLabel)
            axis_label: AxisLabel = grid_value

            target_graph: OppositeFaceGraph = front_graph if face_name == FaceName.FRONT else top_graph
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

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = FindSubgraphs()
        scene.render()
