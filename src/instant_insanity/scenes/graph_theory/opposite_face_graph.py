import numpy as np

from manim import tempconfig, Dot, VGroup, Scene, ORIGIN, LEFT, RIGHT, FadeIn

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.object_count import ObjectToCountMapping
from instant_insanity.core.puzzle import (Puzzle, FaceColour, PuzzleCubeNumber, AxisLabel,
                                          WINNING_MOVES_PUZZLE, CARTEBLANCHE_PUZZLE,
                                          CubeAxis, FaceColourPair)
from instant_insanity.mobjects.opposite_face_graph import ColourToNodeMapping, NodeToColourMapping, mk_colour_to_node, \
    NodeToMobjectMapping, EdgeToMobjectMapping, EdgeToSubgraphMapping
from instant_insanity.scenes.graph_theory.labelled_edge import LabelledEdge
from instant_insanity.scenes.graph_theory.coloured_node import mk_dot
from instant_insanity.scenes.graph_theory.quadrant import Quadrant, mk_standard_node_pair, NodePair, \
    QUADRANT_TO_POSITION

# each node is identified by its quadrant and has a unique colour
# there is a one-to-one mapping between nodes and colours


class OppositeFaceGraph(VGroup):
    """
    This class animates the opposite face graph of a puzzle.

    The graph has four nodes, one for each face colour.
    The node mobjects are stored in the node_dict.
    The key for each node is its Quadrant.

    The graph has zero or more edges.
    The edges mobjects are stored in the edge_dict.
    The key for each edge is CubeAxis, namely a pair that consists of its PuzzleCubeNumber and AxisLabel.
    For example, the edge key for the x-axis of cube 2
    is the pair (PuzzleCubeNumber.TWO, AxisLabel.X).

    There may be parallel edges between nodes so we need to draw each a little differently
    in order to visually distinguish them.
    We always reorder the nodes in ascending order of their quadrants.
    This is equivalent to regarding the nodes as a set.
    The set of nodes for an edge contains two elements for lines and one element for loops.

    We keep track of a sequence number for each edge between a given set of nodes.
    Each edge is drawn as a cubic spline with the same endpoints but differing control points
    that vary depending on the sequence number.

    The graph state includes the subset of edges that it contains.
    This state defines a subgraph which always contains all four nodes but only
    the indicated edges. Initially the subgraph contains no edges.

    Attributes:
        centre: the scene coordinates of the centre of the graph.
        puzzle: the puzzle.
        colours: the set of face colours in the puzzle.
        colour_to_node: the mapping of face colours to quadrants.
        node_to_colour: the mapping of quadrants to face colours.
        node_to_mobject: the mapping of quadrants to mobjects that draw the nodes.
        node_pair_to_count: the node-pair-to-count mapping.
        edge_to_mobject: the mapping of edge keys to mobjects that draw the edges.
        edge_to_subgraph: the mapping of edge keys to subgraph membership values
    """
    centre: np.ndarray
    puzzle: Puzzle
    colours: set[FaceColour]
    colour_to_node: ColourToNodeMapping
    node_to_colour: NodeToColourMapping
    node_pair_to_count: ObjectToCountMapping
    node_to_mobject: NodeToMobjectMapping
    edge_to_mobject: EdgeToMobjectMapping
    edge_to_subgraph: EdgeToSubgraphMapping

    def __init__(self, puzzle: Puzzle, centre: np.ndarray) -> None:
        """
        Creates a new opposite face graph with no edges.
        """
        super().__init__()
        self.centre = centre
        self.puzzle = puzzle
        self.colours = puzzle.mk_colours()
        self.colour_to_node = mk_colour_to_node(puzzle)

        # invert the colour to node mapping
        face_colour: FaceColour
        quadrant: Quadrant
        self.node_to_colour = {
            quadrant: face_colour for face_colour, quadrant in self.colour_to_node.items()
        }

        self.node_pair_to_count = ObjectToCountMapping()

        # initialize the nodes before the edges because the edges use the node centres
        self.init_node_to_mobject()
        self.init_edge_to_mobject()

        # the subgraph is initially empty
        empty_subgraph: EdgeToSubgraphMapping = self.mk_subgraph_for_flag(False)
        self.set_subgraph(empty_subgraph)

    def mk_node_at(self, quadrant: Quadrant, point: np.ndarray) -> Dot:
        """
        Creates a node for a given quadrant at a given point.
        Args:
            quadrant: the quadrant.
            point: the point.

        Returns:
            a new node object at the given point with the quadrant's colour.
        """
        face_colour: FaceColour = self.node_to_colour[quadrant]
        return mk_dot(face_colour, point)

    def init_node_to_mobject(self) -> None:
        """
        Initializes node_to_mobject.
        """
        self.node_to_mobject = {}
        quadrant: Quadrant
        for quadrant in Quadrant:
            position: np.ndarray = QUADRANT_TO_POSITION[quadrant]
            point: np.ndarray = position + self.centre
            self.node_to_mobject[quadrant] = self.mk_node_at(quadrant, point)

    def init_edge_to_mobject(self) -> None:
        """
        Initializes edge_to_mobject.
        """
        self.edge_to_mobject = {}

        cube_axis_to_face_colour_pair: dict[CubeAxis, FaceColourPair]
        cube_axis_to_face_colour_pair = self.puzzle.mk_cube_axis_to_face_colour_pair()

        cube_axis: CubeAxis
        face_colour_pair: FaceColourPair
        for cube_axis, face_colour_pair in cube_axis_to_face_colour_pair.items():
            number: PuzzleCubeNumber
            axis: AxisLabel
            number, axis = cube_axis
            text: str = f'{number.value}{axis.value}'

            colour1: FaceColour
            colour2: FaceColour
            colour1, colour2 = face_colour_pair

            quadrant1: Quadrant = self.colour_to_node[colour1]
            quadrant2: Quadrant = self.colour_to_node[colour2]
            node_pair: NodePair = mk_standard_node_pair(quadrant1, quadrant2)

            start_quadrant: Quadrant
            end_quadrant: Quadrant
            start_quadrant, end_quadrant = node_pair

            sequence_number: int = self.node_pair_to_count.post_increment(node_pair)
            start_point: np.ndarray = self.node_to_mobject[start_quadrant].get_center()
            end_point: np.ndarray = self.node_to_mobject[end_quadrant].get_center()
            self.edge_to_mobject[cube_axis] = LabelledEdge(node_pair,
                                                           text,
                                                           sequence_number,
                                                           start_point,
                                                           end_point)

    def copy_edge_to(self,
                     cube_axis: CubeAxis,
                     start_point: np.ndarray,
                     end_point: np.ndarray) -> LabelledEdge:
        """
        Copies the given labelled edge to a new start point and end point.
        Args:
            cube_axis: the cube axis of LabelledEdge to copy.
            start_point: the new start point.
            end_point: the new end point.

        Returns:
            the new labelled edge.
        """
        edge: LabelledEdge = self.edge_to_mobject[cube_axis]
        return edge.copy_to(start_point, end_point)


    def set_subgraph(self, subgraph: EdgeToSubgraphMapping) -> None:
        """
        Sets the subgraph of the graph.

        Args:
            subgraph: the edge-to-subgraph mapping.
        """

        self.edge_to_subgraph = subgraph.copy()

        # remove all the nodes and edges
        self.remove(*self.submobjects)

        # add the subgraph edges first so they are drawn before the nodes
        cube_axis: CubeAxis
        for cube_axis in subgraph.keys():
            if subgraph[cube_axis]:
                self.add(self.edge_to_mobject[cube_axis])

        # finally, add back all the nodes so they are drawn after the edges
        self.add(*self.node_to_mobject.values())

    def set_subgraph_edge(self, cube_axis: CubeAxis, flag: bool) -> None:
        """
        Sets the subgraph edge of the graph.
        Args:
            cube_axis: the edge
            flag: the subgraph membership flag
        """
        subgraph: EdgeToSubgraphMapping = self.edge_to_subgraph.copy()
        subgraph[cube_axis] = flag
        self.set_subgraph(subgraph)

    @staticmethod
    def mk_subgraph_for_flag(flag: bool) -> EdgeToSubgraphMapping:
        """
        Returns a subgraph for a boolean flag .
        Args:
            flag: True for the full subgraph, False for the empty subgraph.

        Returns:
            the subgraph for a boolean flag.
        """
        cube_number: PuzzleCubeNumber
        axis_label: AxisLabel
        keys: list[CubeAxis] = [(cube_number, axis_label)
                                for cube_number in PuzzleCubeNumber
                                for axis_label in AxisLabel]
        subgraph: EdgeToSubgraphMapping = dict.fromkeys(keys, flag)
        return subgraph

class OppositeFaceGraphs(Scene):
    def construct(self):
        # add_coordinate_grid(self)

        full_subgraph: EdgeToSubgraphMapping = OppositeFaceGraph.mk_subgraph_for_flag(True)

        cb_graph: OppositeFaceGraph = OppositeFaceGraph(CARTEBLANCHE_PUZZLE, ORIGIN + 3 * LEFT)
        cb_graph.set_subgraph(full_subgraph)
        self.add(cb_graph)
        self.play(FadeIn(cb_graph))

        wm_graph: OppositeFaceGraph = OppositeFaceGraph(WINNING_MOVES_PUZZLE, ORIGIN + 3 * RIGHT)
        wm_graph.set_subgraph(full_subgraph)
        self.add(wm_graph)
        self.play(FadeIn(wm_graph))

        self.wait()

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = OppositeFaceGraphs()
        scene.render()
