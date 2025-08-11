from typing import TypeAlias
from enum import StrEnum
from manim import *
from mypyc.primitives.generic_ops import next_op
from svgelements import Curve

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.puzzle import (Puzzle, FaceColour, PuzzleCubeNumber, AxisLabel,
                                          WINNING_MOVES_PUZZLE, CARTEBLANCHE_PUZZLE,
                                          WINNING_MOVES_COLOURS, CARTEBLANCHE_COLOURS, CubeAxis, FaceColourPair)
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

# each node is identified by its quadrant and has a unique colour
ColourToNodeMapping: TypeAlias = dict[FaceColour, Quadrant]
NodeToColourMapping: TypeAlias = dict[Quadrant, FaceColour]


def mk_colour_to_node(colours: set[FaceColour]) -> ColourToNodeMapping:
    """
    Make the mapping of face colours to quadrants.
    The colours are sorted and then assigned to the quadrants in their standard order.

    Args:
        colours: a set of exactly four face colours.

    Returns:
        a mapping of the faces colours to quadrants as a dict.

    """
    if not isinstance(colours, set):
        raise TypeError(f'Expected a set but got {type(colours).__name__}')

    colour: FaceColour
    for colour in colours:
        if not isinstance(colour, FaceColour):
            raise TypeError(f'Expected colour type {FaceColour.__name__} but got {type(colour).__name__}')

    n: int = len(colours)
    if n != 4:
        raise ValueError(f'Expected 4 colours but got {n}')

    sorted_colours: list[FaceColour] = sorted(colours)
    quadrant: Quadrant
    node_layout: ColourToNodeMapping = {
        colour: quadrant for colour, quadrant in zip(sorted_colours, Quadrant)
    }
    return node_layout


CARTEBLANCHE_NODE_LAYOUT: ColourToNodeMapping = mk_colour_to_node(CARTEBLANCHE_COLOURS)
WINNING_MOVES_NODE_LAYOUT: ColourToNodeMapping = mk_colour_to_node(WINNING_MOVES_COLOURS)


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
    return Text(text, font_size=24, color=BLACK).move_to(point)

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
        super().__init__(node_pair, text, sequence_number)
        self.start_point = start_point
        self.end_point = end_point
        # TODO: use cubic Bezier and adjust to sequent number
        line: Line = Line(start_point, end_point, color=BLACK)
        self.curve = line
        # TODO: position label better
        label_point: np.ndarray = (start_point + end_point) / 2.0
        self.label = mk_text(text, label_point)

class LoopEdge(CurveEdge):
    """
    A LoopEdge is a graph edge that connects a node to itself.
    """
    point: np.ndarray

    def __init__(self, node_pair: NodePair, text: str, sequence_number: int, point: np.ndarray) -> None:
        super().__init__(node_pair, text, sequence_number)
        self.point = point
        # TODO: use cubic Bezier and adjust to sequent number
        line: Line = Line(point, point, color=BLACK)
        self.curve = line
        # TODO: position label better
        label_point: np.ndarray = point
        self.label = mk_text(text, label_point)

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
    edge_to_mobject: EdgeToMobjectMapping # TODO: use edge_to_cube instead

    def __init__(self, centre: np.ndarray, puzzle: Puzzle) -> None:
        """
        Creates a new opposite face graph with no edges.
        """
        super().__init__()
        self.centre = centre
        self.puzzle = puzzle
        self.colours = puzzle.mk_colours()
        self.colour_to_node = mk_colour_to_node(self.colours)

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
        add_coordinate_grid(self)

        cb_graph: OppositeFaceGraph = OppositeFaceGraph(ORIGIN + 3 * LEFT, CARTEBLANCHE_PUZZLE)
        self.play(FadeIn(cb_graph))
        self.wait()

        wm_graph: OppositeFaceGraph = OppositeFaceGraph(ORIGIN + 3 * RIGHT, WINNING_MOVES_PUZZLE)
        self.play(FadeIn(wm_graph))
        self.wait()

        self.wait(4.0)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = FourNodeSquareGraph()
        scene.render()
