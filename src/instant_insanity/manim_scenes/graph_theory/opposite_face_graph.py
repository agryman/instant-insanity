from typing import TypeAlias
from enum import StrEnum
from manim import *
from mypyc.primitives.generic_ops import next_op
from svgelements import Curve

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FaceName
from instant_insanity.core.puzzle import (Puzzle, FaceColour, PuzzleCubeNumber, AxisLabel,
                                          WINNING_MOVES_PUZZLE, CARTEBLANCHE_PUZZLE,
                                          CubeAxis, FaceColourPair,
                                          AXIS_TO_FACE_NAME_PAIR, PuzzleCube)
from instant_insanity.manim_scenes.coloured_cube import MANIM_COLOUR_MAP
from instant_insanity.manim_scenes.coordinate_grid import add_coordinate_grid


class ObjectToCountMapping:
    """
    This class keeps tracks of counts on any set of objects.

    Attributes:
        object_to_count: the mapping of objects to counts.

    """
    object_to_count: dict[object, int]

    def __init__(self):
        self.object_to_count = {}

    def post_increment(self, key: object) -> int:
        """
        Returns the current count and increments it.
        A count of 0 is returned the first time the key is used.

        Args:
            key: the immutable object to increment.

        Returns:
            the count before incrementing.
        """

        count: int = 0 if key not in self.object_to_count else self.object_to_count[key]
        self.object_to_count[key] = count + 1
        return count


class Quadrant(StrEnum):
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"


NodePair: TypeAlias = tuple[Quadrant, Quadrant]


def mk_standard_node_pair(quadrant1: Quadrant, quadrant2: Quadrant) -> NodePair:
    """
    Returns a pair of nodes in ascending order.

    Args:
        quadrant1: a node
        quadrant2: a node

    Returns:
        A pair of nodes in ascending order.
    """

    return min(quadrant1, quadrant2), max(quadrant1, quadrant2)


QUADRANT_TO_POSITION: dict[Quadrant, np.ndarray] = {
    Quadrant.I: RIGHT + UP,
    Quadrant.II: LEFT + UP,
    Quadrant.III: LEFT + DOWN,
    Quadrant.IV: RIGHT + DOWN
}

QUADRANT_TO_BASIS: dict[Quadrant, tuple[np.ndarray, np.ndarray]] = {
    Quadrant.I: (RIGHT, UP),
    Quadrant.II: (UP, LEFT),
    Quadrant.III: (LEFT, DOWN),
    Quadrant.IV: (DOWN, RIGHT)
}

# each node is identified by its quadrant and has a unique colour
ColourToNodeMapping: TypeAlias = dict[FaceColour, Quadrant]
NodeToColourMapping: TypeAlias = dict[Quadrant, FaceColour]

DEFAULT_EDGE_FONT_COLOR: ManimColor = BLACK
DEFAULT_EDGE_FONT_SIZE: int = 15
DEFAULT_EDGE_STROKE_COLOUR: ManimColor = BLACK
DEFAULT_EDGE_STROKE_WIDTH: float = 2.0


def mk_colour_to_node(puzzle: Puzzle) -> ColourToNodeMapping:
    """
    Make the mapping of face colours to quadrants.
    The colours are sorted and then assigned to the quadrants to minimize diagonal crossovers.

    Args:
        puzzle: the puzzle

    Returns:
        a mapping of the faces colours to quadrants as a dict.

    """
    if not isinstance(puzzle, Puzzle):
        raise TypeError(f'Expected a Puzzle but got {type(puzzle).__name__}')

    colours: set[FaceColour] = puzzle.mk_colours()
    colour: FaceColour
    for colour in colours:
        if not isinstance(colour, FaceColour):
            raise TypeError(f'Expected colour type {FaceColour.__name__} but got {type(colour).__name__}')

    n: int = len(colours)
    if n != 4:
        raise ValueError(f'Expected 4 colours but got {n}')

    # make the set of strictly increasing colour pairs
    sorted_colours: list[FaceColour] = sorted(colours)
    colour_pairs: set[FaceColourPair] = {
        (colour_1, colour_2)
        for colour_1 in sorted_colours
        for colour_2 in sorted_colours
        if colour_1 < colour_2
    }

    # initialize their counts to 0
    colour_pair_to_count: dict[FaceColourPair, int] = {
        key: 0 for key in colour_pairs
    }

    # add the counts for the puzzle
    cube: PuzzleCube
    for cube in puzzle.number_to_cube.values():
        # add the counts for the cube
        name_1: FaceName
        name_2: FaceName
        for (name_1, name_2) in AXIS_TO_FACE_NAME_PAIR.values():
            # add the counts for the axis
            colour_1: FaceColour = cube.name_to_colour[name_1]
            colour_2: FaceColour = cube.name_to_colour[name_2]
            # ignore loops
            if colour_1 == colour_2:
                continue
            colour_min: FaceColour = min(colour_1, colour_2)
            colour_max: FaceColour = max(colour_1, colour_2)
            colour_pair_to_count[(colour_min, colour_max)] += 1

    # always assign sorted_colours[0] to quadrant I
    # compute the crossover count when sorted_colours[i] for i in 1, 2, 3 is in quadrant III

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


CARTEBLANCHE_NODE_LAYOUT: ColourToNodeMapping = mk_colour_to_node(CARTEBLANCHE_PUZZLE)
WINNING_MOVES_NODE_LAYOUT: ColourToNodeMapping = mk_colour_to_node(WINNING_MOVES_PUZZLE)


def mk_dot(face_colour: FaceColour, point: np.ndarray) -> Dot:
    """
    Makes a dot for the given face colour and point.
    Args:
        face_colour: the face colour
        point: the centre of the dot

    Returns:
        a Dot mobject
    """
    fill_colour: ManimColor = MANIM_COLOUR_MAP[face_colour]
    dot: Dot = Dot(point=point,
                   radius=DEFAULT_DOT_RADIUS * 2,
                   fill_color=fill_colour,
                   stroke_color=BLACK,
                   stroke_width=2)
    return dot


def mk_text(text: str, point: np.ndarray) -> Text:
    label: Text = Text(text,
                       font_size=DEFAULT_EDGE_FONT_SIZE,
                       color=DEFAULT_EDGE_FONT_COLOR,
                       font='sans-serif')
    label.move_to(point)
    return label


class CurveEdge:
    """
    Graph edges always connect their nodes in ascending order.
    There may be parallel edges between nodes.
    The shape of the edge depends on its sequence number within the set
    of parallel edges.

    Attributes:
        node_pair: a pair of nodes in ascending order.
        text: the text of the edge label.
        sequence_number: the sequence number of the edge for the given node pair.
        curve: the VMobject for the edge curve.
        label: the VMobject for the edge label.
    """
    node_pair: NodePair
    text: str
    sequence_number: int
    curve: VMobject
    label: VMobject

    def __init__(self, node_pair: NodePair, text: str, sequence_number: int) -> None:
        self.node_pair = node_pair
        self.text = text
        self.sequence_number = sequence_number


class LineEdge(CurveEdge):
    """
    A LineEdge is a graph edge that connects two distinct nodes.
    """
    start_point: np.ndarray
    end_point: np.ndarray

    def __init__(self,
                 node_pair: NodePair,
                 text: str,
                 sequence_number: int,
                 start_point: np.ndarray,
                 end_point: np.ndarray):
        start_node: Quadrant
        end_node: Quadrant
        start_node, end_node = node_pair
        if start_node >= end_node:
            raise ValueError(f'Expected start_node < end_node but got {start_node} >= {end_node}')

        super().__init__(node_pair, text, sequence_number)
        self.start_point = start_point
        self.end_point = end_point

        direction: np.ndarray = end_point - start_point
        unit_tangent: np.ndarray = direction / np.linalg.norm(direction)
        unit_normal: np.ndarray = np.cross(unit_tangent, OUT)

        # special case treatment: reverse the normal for I - IV edges so it points outward
        if start_node == Quadrant.I and end_node == Quadrant.IV:
            unit_normal = -1.0 * unit_normal

        # create the curve
        diagonals: set[NodePair] = {
            (Quadrant.I, Quadrant.III),
            (Quadrant.II, Quadrant.IV)
        }
        alpha: float
        beta: float
        alpha, beta = (0.5, 0.5) if node_pair in diagonals else (0.5, 0.6)

        tangent_displacement: np.ndarray = alpha * unit_tangent
        normal_displacement: np.ndarray = beta * sequence_number * unit_normal

        start_handle: np.ndarray = start_point + tangent_displacement + normal_displacement
        end_handle: np.ndarray = end_point - tangent_displacement + normal_displacement

        line: CubicBezier = CubicBezier(start_point,
                                        start_handle,
                                        end_handle,
                                        end_point,
                                        color=BLACK,
                                        stroke_width=DEFAULT_EDGE_STROKE_WIDTH)
        self.curve = line

        # create the label
        line_midpoint: np.ndarray = line.point_from_proportion(0.5)
        label: Text = mk_text(text, line_midpoint)
        label.move_to(line_midpoint + 0.15 * unit_normal)
        self.label = label


class LoopEdge(CurveEdge):
    """
    A LoopEdge is a graph edge that connects a node to itself.
    """
    point: np.ndarray

    def __init__(self, node_pair: NodePair, text: str, sequence_number: int, point: np.ndarray) -> None:
        start_node: Quadrant
        end_node: Quadrant
        start_node, end_node = node_pair
        if start_node != end_node:
            raise ValueError(f'Expected start_node == end_node but got {start_node} != {end_node}')

        super().__init__(node_pair, text, sequence_number)
        self.point = point

        # create the loop
        start_anchor: np.ndarray = point
        end_anchor: np.ndarray = point
        start_tangent: np.ndarray
        end_tangent: np.ndarray
        start_tangent, end_tangent = QUADRANT_TO_BASIS[start_node]
        velocity_0: float = 1.5
        acceleration: float = 0.5
        velocity: float = velocity_0 + acceleration * sequence_number
        start_handle = start_anchor + velocity * start_tangent
        end_handle = end_anchor + velocity * end_tangent
        loop: CubicBezier = CubicBezier(start_anchor,
                                        start_handle,
                                        end_handle,
                                        end_anchor,
                                        color=BLACK,
                                        stroke_width=DEFAULT_EDGE_STROKE_WIDTH)
        self.curve = loop

        # create the label
        loop_midpoint: np.ndarray = loop.point_from_proportion(0.5)
        label: Text = mk_text(text, loop_midpoint)
        outward_direction: np.ndarray = start_tangent + end_tangent
        label.move_to(loop_midpoint + 0.125 * outward_direction)
        self.label = label


NodeToMobjectMapping: TypeAlias = dict[Quadrant, VMobject]
EdgeToMobjectMapping: TypeAlias = dict[CubeAxis, VMobject]
EdgeToCurveMapping: TypeAlias = dict[CubeAxis, CurveEdge]


class OppositeFaceGraph(VGroup):
    """
    This class animates the opposite face graph of a puzzle.

    The graph has four nodes, one for each face colour.
    The node mobjects are stored in the node_dict.
    The key for each node is its Quadrant.

    The graph has zero or more edges.
    The edges mobjects are stored in the edge_dict.
    The key for each edge is a pair that consists of its PuzzleCubeNumber and AxisLabel.
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

    Attributes:
        centre: the scene coordinates of the centre of the graph
        puzzle: the puzzle
        colours: the set of face colours in the puzzle
        colour_to_node: the mapping of face colours to quadrants
        node_to_colour: the mapping of quadrants to face colours
        node_to_mobject: the mapping of quadrants to mobjects that draw the nodes
        node_pair_to_count: the node pair to count mapping
        edge_to_mobject: the mapping of edge keys to mobjects that draw the edges
    """
    centre: np.ndarray
    puzzle: Puzzle
    colours: set[FaceColour]
    colour_to_node: ColourToNodeMapping
    node_to_colour: NodeToColourMapping
    node_pair_to_count: ObjectToCountMapping
    node_to_mobject: NodeToMobjectMapping
    edge_to_curve: EdgeToCurveMapping
    edge_to_mobject: EdgeToMobjectMapping  # TODO: use edge_to_curve instead

    def __init__(self, centre: np.ndarray, puzzle: Puzzle) -> None:
        """
        Creates a new opposite face graph with no edges.
        """
        super().__init__()
        self.centre = centre
        self.puzzle = puzzle
        self.colours = puzzle.mk_colours()
        self.colour_to_node = mk_colour_to_node(puzzle)

        face_colour: FaceColour
        quadrant: Quadrant
        self.node_to_colour = {
            quadrant: face_colour for face_colour, quadrant in self.colour_to_node.items()
        }

        self.node_pair_to_count = ObjectToCountMapping()

        # initialize the nodes before the edges because the edges use the node centres
        self.init_node_to_mobject()
        self.init_edge_to_mobject()

        # add the edges before the nodes so that the edges will be drawn before the nodes
        self.add(*self.edge_to_mobject.values())
        self.add(*self.node_to_mobject.values())
        curve_edges: list[CurveEdge] = list(self.edge_to_curve.values())
        curve_edge: CurveEdge
        self.add(*[curve_edge.label for curve_edge in curve_edges])

    def init_node_to_mobject(self) -> None:
        """
        Initializes node_to_mobject.
        """
        self.node_to_mobject = {}
        position: np.ndarray
        for face_colour, quadrant in self.colour_to_node.items():
            position: np.ndarray = QUADRANT_TO_POSITION[quadrant]
            point: np.ndarray = position + self.centre
            node: Dot = mk_dot(face_colour, point)
            self.node_to_mobject[quadrant] = node

    def init_edge_to_mobject(self) -> None:
        """
        Initializes edge_to_mobject.
        """
        self.edge_to_curve = {}
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
            if quadrant1 != quadrant2:
                # add a straight line edge
                start_point: np.ndarray = self.node_to_mobject[start_quadrant].get_center()
                end_point: np.ndarray = self.node_to_mobject[end_quadrant].get_center()
                line_edge: LineEdge = LineEdge(node_pair,
                                               text,
                                               sequence_number,
                                               start_point,
                                               end_point)
                self.edge_to_curve[cube_axis] = line_edge
                line: VMobject = line_edge.curve
                self.edge_to_mobject[cube_axis] = line
            else:
                # add a loop edge
                point: np.ndarray = self.node_to_mobject[quadrant1].get_center()
                loop_edge: LoopEdge = LoopEdge(node_pair,
                                               text,
                                               sequence_number,
                                               point)
                self.edge_to_curve[cube_axis] = loop_edge
                loop: VMobject = loop_edge.curve
                self.edge_to_mobject[cube_axis] = loop


class FourNodeSquareGraph(Scene):
    def construct(self):
        # add_coordinate_grid(self)

        cb_graph: OppositeFaceGraph = OppositeFaceGraph(ORIGIN + 3 * LEFT, CARTEBLANCHE_PUZZLE)
        self.add(cb_graph)
        # self.play(FadeIn(cb_graph))
        # self.wait()

        wm_graph: OppositeFaceGraph = OppositeFaceGraph(ORIGIN + 3 * RIGHT, WINNING_MOVES_PUZZLE)
        self.add(wm_graph)
        # self.play(FadeIn(wm_graph))
        # self.wait()
        #
        #self.wait(4.0)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = FourNodeSquareGraph()
        scene.render()
