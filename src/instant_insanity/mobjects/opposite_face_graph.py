from dataclasses import dataclass

import numpy as np

from manim import Dot, VGroup, Polygon, CubicBezier, StealthTip
from manim.typing import Point3D, Point3D_Array

from instant_insanity.core.cube import FacePlane
from instant_insanity.core.object_count import ObjectToCountMapping
from instant_insanity.core.puzzle import FaceColour, Puzzle, FaceColourPair, PuzzleCube, \
    INITIAL_AXIS_TO_FACE_PLANE_PAIR, \
    CARTEBLANCHE_PUZZLE, WINNING_MOVES_PUZZLE, CubeAxis, PuzzleCubeNumber, AxisLabel, FaceLabel, AXIS_TO_FACE_LABEL_PAIR
from instant_insanity.mobjects.coloured_node import mk_dot
from instant_insanity.mobjects.labelled_edge import LabelledEdge, PointPair
from instant_insanity.mobjects.puzzle_3d import Puzzle3D
from instant_insanity.mobjects.quadrant import Quadrant, QUADRANT_TO_POSITION, NodePair, mk_standard_node_pair
from instant_insanity.mobjects.puzzle_cube_3d import PuzzleCube3D
from instant_insanity.mobjects.stealth_tip import CubeEdgeTip, EdgeTip, mk_stealth_tip_from_cubic_bezier

# each node is identified by its quadrant and has a unique colour
# there is a one-to-one mapping between nodes and colours
type ColourToNodeMapping = dict[FaceColour, Quadrant]
type NodeToColourMapping = dict[Quadrant, FaceColour]


def mk_colour_to_node(puzzle: Puzzle) -> ColourToNodeMapping:
    """
    Make the mapping of face colours to quadrants.
    The colours are sorted and then assigned to the quadrants to minimize diagonal crossovers.

    Args:
        puzzle: the puzzle

    Returns:
        a mapping of the face colours to quadrants as a dict.

    """
    # make the set of strictly increasing colour pairs
    colours: set[FaceColour] = puzzle.mk_colours()
    sorted_colours: list[FaceColour] = sorted(colours)
    colour_pairs: set[FaceColourPair] = {
        (colour_1, colour_2)
        for colour_1 in sorted_colours
        for colour_2 in sorted_colours
        if colour_1 < colour_2
    }

    # initialize the pair counts to 0
    colour_pair_to_count: dict[FaceColourPair, int] = {
        key: 0 for key in colour_pairs
    }

    # add the pair counts for the puzzle
    cube: PuzzleCube
    for cube in puzzle.number_to_cube.values():
        # add the pair counts for the cube
        face_label_1: FaceLabel
        face_label_2: FaceLabel
        for (face_label_1, face_label_2) in AXIS_TO_FACE_LABEL_PAIR.values():
            # add the counts for the axis
            colour_1: FaceColour = cube.face_label_to_colour[face_label_1]
            colour_2: FaceColour = cube.face_label_to_colour[face_label_2]
            # ignore loops
            if colour_1 == colour_2:
                continue
            colour_min: FaceColour = min(colour_1, colour_2)
            colour_max: FaceColour = max(colour_1, colour_2)
            colour_pair_to_count[(colour_min, colour_max)] += 1

    # always assign sorted_colours[0] to quadrant I
    # compute the crossover counts when sorted_colours[i] is in quadrant III for i in 1, 2, 3

    # define short variable names for the sorted colours
    c0: FaceColour
    c1: FaceColour
    c2: FaceColour
    c3: FaceColour
    c0, c1, c2, c3 = tuple(sorted_colours)

    # define short variable names for the edge counts
    c01: int = colour_pair_to_count[(c0, c1)]
    c02: int = colour_pair_to_count[(c0, c2)]
    c03: int = colour_pair_to_count[(c0, c3)]
    c12: int = colour_pair_to_count[(c1, c2)]
    c13: int = colour_pair_to_count[(c1, c3)]
    c23: int = colour_pair_to_count[(c2, c3)]

    # define short variable names for the crossover counts
    cc1: int = c01 * c23
    cc2: int = c02 * c13
    cc3: int = c03 * c12

    # use the layout that has the minimum crossover count
    cc_min: int = min(cc1, cc2, cc3)
    node_layout: ColourToNodeMapping
    if cc1 == cc_min:
        node_layout = {
            c0: Quadrant.I,
            c1: Quadrant.III,
            c2: Quadrant.II,
            c3: Quadrant.IV
        }
    elif cc2 == cc_min:
        node_layout = {
            c0: Quadrant.I,
            c2: Quadrant.III,
            c1: Quadrant.II,
            c3: Quadrant.IV
        }
    else:
        assert cc3 == cc_min
        node_layout = {
            c0: Quadrant.I,
            c3: Quadrant.III,
            c1: Quadrant.II,
            c2: Quadrant.IV
        }

    return node_layout


CARTEBLANCHE_NODE_MAPPING: ColourToNodeMapping = mk_colour_to_node(CARTEBLANCHE_PUZZLE)
WINNING_MOVES_NODE_MAPPING: ColourToNodeMapping = mk_colour_to_node(WINNING_MOVES_PUZZLE)
type NodeToMobjectMapping = dict[Quadrant, Dot]
type EdgeToMobjectMapping = dict[CubeAxis, LabelledEdge]
type EdgeToSubgraphMapping = dict[CubeAxis, bool]


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
    centre: Point3D
    puzzle: Puzzle
    colours: set[FaceColour]
    colour_to_node: ColourToNodeMapping
    node_to_colour: NodeToColourMapping
    node_pair_to_count: ObjectToCountMapping
    node_to_mobject: NodeToMobjectMapping
    edge_to_mobject: EdgeToMobjectMapping
    edge_to_subgraph: EdgeToSubgraphMapping

    def __init__(self, puzzle: Puzzle, centre: Point3D) -> None:
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

    def mk_node_at(self, quadrant: Quadrant, point: Point3D) -> Dot:
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
            position: Point3D = QUADRANT_TO_POSITION[quadrant]
            point: Point3D = position + self.centre
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
            start_point: Point3D = self.node_to_mobject[start_quadrant].get_center()
            end_point: Point3D = self.node_to_mobject[end_quadrant].get_center()
            point_pair: PointPair = (start_point, end_point)
            self.edge_to_mobject[cube_axis] = LabelledEdge(node_pair,
                                                           text,
                                                           sequence_number,
                                                           point_pair,
                                                           point_pair,
                                                           point_pair,
                                                           moving=False)

    def copy_edge_from_to(self,
                          cube_axis: CubeAxis,
                          point_pair_0: PointPair,
                          point_pair_1: PointPair,
                          point_pair_alpha: PointPair) -> LabelledEdge:
        edge: LabelledEdge = self.edge_to_mobject[cube_axis]
        return edge.copy_from_to(point_pair_0, point_pair_1, point_pair_alpha)


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


@dataclass
class FaceData:
    colour: FaceColour
    quadrant: Quadrant
    polygon: Polygon
    dot: Dot

def mk_face_data_from_cube(graph: OppositeFaceGraph,
                           cube: PuzzleCube3D,
                           face_label: FaceLabel,
                           polygon: Polygon) -> FaceData:
    colour: FaceColour = cube.get_colour_name(face_label)
    return mk_face_data(graph, colour, polygon)

def mk_face_data_from_puzzle(graph: OppositeFaceGraph,
                             puzzle3d: Puzzle3D,
                             cube_number: PuzzleCubeNumber,
                             face_label: FaceLabel,
                             polygon: Polygon) -> FaceData:
    colour: FaceColour = puzzle3d.get_colour_name(cube_number, face_label)
    return mk_face_data(graph, colour, polygon)

def mk_face_data(graph: OppositeFaceGraph, colour: FaceColour, polygon: Polygon) -> FaceData:
    quadrant: Quadrant = graph.colour_to_node[colour]
    vertices: Point3D_Array = polygon.get_vertices()
    centroid: Point3D = np.mean(vertices, axis=0)
    dot: Dot = graph.mk_node_at(quadrant, centroid)
    return FaceData(colour, quadrant, polygon, dot)

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
