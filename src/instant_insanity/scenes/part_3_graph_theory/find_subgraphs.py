"""
This module animates the search for the two subgraphs of the opposite-face graph of a puzzle.
"""

from manim import Scene, tempconfig, UP, DOWN, LEFT, RIGHT, Tex, Dot, StealthTip, CubicBezier, FadeIn, FadeOut
from manim.typing import Vector3D
from manim.utils.color.X11 import BLACK

from instant_insanity.core.cube import FaceName
from instant_insanity.core.puzzle import Puzzle, PuzzleCubeNumber, AxisLabel, CubeAxis, WINNING_MOVES_PUZZLE
from instant_insanity.mobjects.labelled_edge import LabelledEdge
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, EdgeToSubgraphMapping, EdgeToMobjectMapping
from instant_insanity.mobjects.quadrant import NodePair, Quadrant
from instant_insanity.mobjects.stealth_tip import mk_stealth_tip_from_cubic_bezier, EdgeTip, CubeEdgeTip
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.solvers.graph_solver import GraphSolver, Grid

class FindSubgraphs(GridMixin, Scene):
    def construct(self):
        puzzle: Puzzle =  WINNING_MOVES_PUZZLE

        # add three graphs

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

        graph_solver: GraphSolver = GraphSolver(puzzle)
        graph_solver.solve()

        self.move_solution(graph_solver, 0, total_graph, front_graph, top_graph)

        subgraph: OppositeFaceGraph
        for subgraph in (front_graph, top_graph):
            cube_edge_tips: CubeEdgeTip = self.mk_edge_directions(subgraph)
            for edge_tip in cube_edge_tips.values():
                self.play(FadeIn(edge_tip.tip), run_time=0.5)

        # fade out the total graph in preparation for entry to the next scene CubesFromSubgraphs

        self.play(FadeOut(total_graph))

        self.wait(4)

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

    @staticmethod
    def mk_edge_directions(subgraph: OppositeFaceGraph) -> CubeEdgeTip:
        """
        Pick directions for the edges of the 2-factor subgraph.
        The subgraph has one edge per cube so pick directions in that order.
        Each edge is either forward or backward with respect to the start and end points
        of its Bézier curve. Indicate the direction by drawing a stealth arrow tip on the edge.

        Args:
            subgraph: the 2-factor subgraph.

        Returns:
            a dict that maps cube numbers to edge tips.
        """

        # get the edges of the subgraph
        cube_axis: CubeAxis
        labelled_edge: LabelledEdge
        subgraph_edges: EdgeToMobjectMapping = {
            cube_axis: labelled_edge
            for cube_axis, labelled_edge in subgraph.edge_to_mobject.items()
            if subgraph.edge_to_subgraph[cube_axis]
        }
        # there MUST be exactly four edges in the subgraph
        assert len(subgraph_edges) == 4

        # get the cube numbers of the subgraph
        subgraph_cubes: set[PuzzleCubeNumber] = {
            cube_number for cube_number, axis_label in subgraph_edges.keys()
        }
        # there MUST be exactly four cubes in the subgraph
        assert len(subgraph_cubes) == 4

        # get the start and end nodes for each cube
        cube_start_end: dict[PuzzleCubeNumber, NodePair] = {
            cube_number: labelled_edge.node_pair
            for (cube_number, _), labelled_edge in subgraph_edges.items()
        }

        # compute the total degree of each node
        node: Quadrant
        node_degrees: dict[Quadrant, int] = {node: 0 for node in Quadrant}
        for node_pair in cube_start_end.values():
            for node in node_pair:
                node_degrees[node] += 1

        # every node MUST have total degree 2
        for node in Quadrant:
            assert node_degrees[node] == 2

        # assign a direction to the edges
        # each edge MUST come out of either its start or end node, which could be the same
        # therefore, it is sufficient to specify which node the edge comes out of

        cube_out: dict[PuzzleCubeNumber, Quadrant] = dict()
        # always set the out node for cube 1 to its start node
        o1: Quadrant = cube_start_end[PuzzleCubeNumber.ONE][0]
        cube_out[PuzzleCubeNumber.ONE] = o1

        # generate all the combinations and break as soon as we find one that works
        solved: bool = False
        o2: Quadrant
        for o2 in cube_start_end[PuzzleCubeNumber.TWO]:
            cube_out[PuzzleCubeNumber.TWO] = o2
            o3: Quadrant
            for o3 in cube_start_end[PuzzleCubeNumber.THREE]:
                cube_out[PuzzleCubeNumber.THREE] = o3
                o4: Quadrant
                for o4 in cube_start_end[PuzzleCubeNumber.FOUR]:
                    cube_out[PuzzleCubeNumber.FOUR] = o4
                    solved = len(set(cube_out.values())) == 4
                    if solved:
                        break # o4
                if solved:
                    break # o3
            if solved:
                break # o2

        # create the stealth tips for each edge
        cube_tips: dict[PuzzleCubeNumber, EdgeTip] = dict()
        for cube_axis, labelled_edge in subgraph_edges.items():
            cube_number, axis_label = cube_axis
            curve: CubicBezier = labelled_edge.curve
            forward: bool = cube_out[cube_number] == labelled_edge.node_pair[0]
            tip: StealthTip = mk_stealth_tip_from_cubic_bezier(curve,
                                                               forward=forward,
                                                               t_buff=0.2,
                                                               scale=1.0)
            cube_tips[cube_number] = EdgeTip(curve, forward, tip)

        return cube_tips

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = FindSubgraphs()
        scene.render()
