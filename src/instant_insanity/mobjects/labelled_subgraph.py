"""
This class models a labelled subgraph of the opposite-face graph.
"""
from manim import Tex, BLACK, LEFT, RIGHT, DOWN, Scene, Text, Indicate
from manim.typing import Point3D, Vector3D

from instant_insanity.core.cube import FacePlane
from instant_insanity.core.puzzle import Puzzle, PuzzleCubeNumber, AxisLabel
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, EdgeToSubgraphMapping, mk_edge_directions
from instant_insanity.mobjects.stealth_tip import CubeEdgeTip
from instant_insanity.solvers.graph_solver import GraphSolver, Grid, GridValue

ARROW_LATEX: str = r" $\rightarrow$ "

FROM_PLANE_DICT: dict[FacePlane, tuple[FacePlane, Vector3D]] = {
    FacePlane.FRONT: (FacePlane.BACK, LEFT),
    FacePlane.TOP: (FacePlane.BOTTOM, RIGHT)
}


class LabelledSubgraph:
    puzzle: Puzzle
    centre: Point3D
    from_plane: FacePlane
    to_plane: FacePlane
    label_tex: Tex
    subgraph: OppositeFaceGraph

    def __init__(self, puzzle: Puzzle, from_plane: FacePlane):
        assert from_plane in FROM_PLANE_DICT.keys()

        to_plane: FacePlane
        direction: Vector3D
        to_plane, direction = FROM_PLANE_DICT[from_plane]

        centre: Point3D = 4.5 * direction + 1.0 * DOWN
        subgraph: OppositeFaceGraph = OppositeFaceGraph(puzzle, centre)

        label_str: str = from_plane.value + ARROW_LATEX + to_plane.value
        label_tex: Tex = Tex(label_str, color=BLACK, font_size=36)
        label_tex.next_to(subgraph, DOWN, buff=0.75)

        self.puzzle = puzzle
        self.centre = centre
        self.from_plane = from_plane
        self.to_plane = to_plane
        self.label_tex = label_tex
        self.subgraph = subgraph

    def get_edge_label(self, cube: PuzzleCubeNumber, axis: AxisLabel) -> Text:
        subgraph: OppositeFaceGraph = self.subgraph
        return subgraph.get_edge_label(cube, axis)

    def add_to_scene(self, scene: Scene) -> None:
        """
        Add the subgraph to the scene.

        Args:
            scene: The scene.
        """
        scene.add(self.subgraph, self.label_tex)

    def add_solution_edges(self, solution: Grid) -> None:
        """
        Add the subgraph edges that belong to the solution.

        Args:
            solution: The solution grid.
        """
        edge_to_subgraph: EdgeToSubgraphMapping = self.subgraph.edge_to_subgraph.copy()
        for cube_number in PuzzleCubeNumber:
            grid_value: GridValue = solution[(self.from_plane, cube_number)]

            assert isinstance(grid_value, AxisLabel)
            axis_label: AxisLabel = grid_value

            edge_to_subgraph[(cube_number, axis_label)] = True
        self.subgraph.set_subgraph(edge_to_subgraph)

    def add_edge_directions(self, scene: Scene) -> None:
        """
        Add the edge directions to the subgraphs.

        Args:
            scene: The scene.
        """
        cube_edge_tips: CubeEdgeTip = mk_edge_directions(self.subgraph)
        for edge_tip in cube_edge_tips.values():
            scene.add(edge_tip.tip)

class LabelledSubgraphPair:
    puzzle: Puzzle
    plane_to_subgraph: dict[FacePlane, LabelledSubgraph]

    def __init__(self, puzzle: Puzzle):
        plane_to_subgraph: dict[FacePlane, LabelledSubgraph] = {
            from_plane: LabelledSubgraph(puzzle, from_plane)
            for from_plane in FROM_PLANE_DICT.keys()
        }
        self.puzzle = puzzle
        self.plane_to_subgraph = plane_to_subgraph

    def get_subgraph_label(self, plane: FacePlane) -> Tex:
        labelled_subgraph: LabelledSubgraph = self.plane_to_subgraph[plane]
        return labelled_subgraph.label_tex

    def indicate_label(self, scene: Scene, plane: FacePlane) -> None:
        label: Tex = self.get_subgraph_label(plane)
        scene.play(Indicate(label, scale_factor=1.5, color=BLACK))

    def get_edge_label(self, plane: FacePlane, cube: PuzzleCubeNumber, axis: AxisLabel) -> Text:
        subgraph: LabelledSubgraph = self.plane_to_subgraph[plane]
        return subgraph.get_edge_label(cube, axis)

    def add_to_scene(self, scene: Scene) -> None:
        """
        Add the edge directions to the subgraphs.
        Args:
            scene: The scene.
        """
        subgraph: LabelledSubgraph
        for subgraph in self.plane_to_subgraph.values():
            subgraph.add_to_scene(scene)

    def add_solution_edges(self) -> None:
        """
        Add the subgraph edges that belong to the first solution to the labelled subgraph pair.
        """

        # solve the puzzle
        graph_solver: GraphSolver = GraphSolver(self.puzzle)
        graph_solver.solve()

        # get the first solution - there might be more than one
        solution: Grid = graph_solver.solutions[0]

        for subgraph in self.plane_to_subgraph.values():
            subgraph.add_solution_edges(solution)

    def add_edge_directions(self, scene: Scene) -> None:
        """
        Add the edge directions to the subgraphs.

        Args:
            scene: The scene.
        """
        subgraph: LabelledSubgraph
        for subgraph in self.plane_to_subgraph.values():
            subgraph.add_edge_directions(scene)
