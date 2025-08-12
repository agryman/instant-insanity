"""
This module implements the LabelledEdge class which is used in the OppositeFaceGraph.
"""
from manim import *
from manim import ManimColor, BLACK, Text, VMobject, OUT, CubicBezier

from instant_insanity.manim_scenes.graph_theory.quadrant import Quadrant, NodePair, QUADRANT_TO_BASIS

DEFAULT_EDGE_FONT: str = 'sans-serif'
DEFAULT_EDGE_FONT_SIZE: int = 15
DEFAULT_EDGE_FONT_COLOR: ManimColor = BLACK

DEFAULT_EDGE_STROKE_WIDTH: float = 2.0
DEFAULT_EDGE_STROKE_COLOUR: ManimColor = BLACK


def mk_text(text: str, point: np.ndarray) -> Text:
    label: Text = Text(text,
                       font=DEFAULT_EDGE_FONT,
                       font_size=DEFAULT_EDGE_FONT_SIZE,
                       color=DEFAULT_EDGE_FONT_COLOR)
    label.move_to(point)
    return label

class LabelledEdge(VGroup):
    """
    A LabelledEdge is an edge in an OppositeFaceGraph.
    It is a composite Manim object which consists of a label and an edge.
    The label is a Text object.
    The edge is a CubicBezier object.
    The edge may be either a link that connect two nodes or a loop that connects a
    node to itself.

    Attributes:
        node_pair: a pair of nodes in ascending order.
        text: the text of the edge label.
        sequence_number: the sequence number of the edge for the given node pair.
        label: The label of the edge. It is a submobject.
        curve: The curve followed by the edge. It is a submobject.
    """
    node_pair: NodePair
    text: str
    sequence_number: int
    curve: CubicBezier
    label: Text

    def __init__(self, node_pair: NodePair, text: str, sequence_number: int) -> None:
        super().__init__()
        self.node_pair = node_pair
        self.text = text
        self.sequence_number = sequence_number

    def set_label(self, label: Text) -> None:
        self.label = label
        self.add(label)

    def set_curve(self, curve: CubicBezier) -> None:
        self.curve = curve
        self.add(curve)


class LabelledLink(LabelledEdge):
    """
    A LabelledLink is a LabelledEdge that connects two distinct nodes.
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

        # special case treatment: reverse the normal for (I,IV) edges so it points outward
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

        link: CubicBezier = CubicBezier(start_point,
                                        start_handle,
                                        end_handle,
                                        end_point,
                                        color=BLACK,
                                        stroke_width=DEFAULT_EDGE_STROKE_WIDTH)
        self.set_curve(link)

        # create the label
        link_midpoint: np.ndarray = link.point_from_proportion(0.5)
        label: Text = mk_text(text, link_midpoint)
        label.move_to(link_midpoint + 0.15 * unit_normal)

        self.set_label(label)

class LabelledLoop(LabelledEdge):
    """
    A LabelledLoop is a LabelledEdge that connects one node to itself.
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
        self.set_curve(loop)

        # create the label
        loop_midpoint: np.ndarray = loop.point_from_proportion(0.5)
        label: Text = mk_text(text, loop_midpoint)
        outward_direction: np.ndarray = start_tangent + end_tangent
        label.move_to(loop_midpoint + 0.125 * outward_direction)
        self.set_label(label)
