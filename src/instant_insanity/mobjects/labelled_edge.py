"""
This module implements the LabelledEdge class which is used in the OppositeFaceGraph.
"""
from typing import Self
import numpy as np

from manim import CubicBezier, Text, VGroup, ManimColor, BLACK, OUT

from instant_insanity.mobjects.quadrant import Quadrant, NodePair, QUADRANT_TO_BASIS

DEFAULT_EDGE_FONT: str = 'sans-serif'
DEFAULT_EDGE_FONT_SIZE: int = 15
DEFAULT_EDGE_FONT_COLOR: ManimColor = BLACK

DEFAULT_EDGE_STROKE_WIDTH: float = 2.0
DEFAULT_EDGE_STROKE_COLOUR: ManimColor = BLACK


def mk_cubic_bezier(start_point: np.ndarray,
                    start_handle: np.ndarray,
                    end_handle: np.ndarray,
                    end_point: np.ndarray,
                    colour: ManimColor = BLACK,
                    stroke_width: float = DEFAULT_EDGE_STROKE_WIDTH) -> CubicBezier:
    curve: CubicBezier = CubicBezier(start_point,
                                     start_handle,
                                     end_handle,
                                     end_point,
                                     color=colour,
                                     stroke_width=stroke_width)
    return curve

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
    The edge may be either a link that connects  two nodes or a loop that connects a
    node to itself.

    Attributes:
        node_pair: a pair of nodes in ascending order.
        text: the text of the edge label.
        sequence_number: the sequence number of the edge for the given node pair.
        start_point: the start point of the curve.
        end_point: the end point of the curve.
        label: The label of the edge. It is a submobject.
        curve: The curve followed by the edge. It is a submobject.
    """
    node_pair: NodePair
    text: str
    sequence_number: int
    start_point: np.ndarray
    end_point: np.ndarray
    curve: CubicBezier | None
    label: Text | None

    def __init__(self,
                 node_pair: NodePair,
                 text: str,
                 sequence_number: int,
                 start_point: np.ndarray,
                 end_point: np.ndarray) -> None:
        super().__init__()
        self.node_pair = node_pair
        self.text = text
        self.sequence_number = sequence_number
        self.start_point = start_point
        self.end_point = end_point
        self.curve = None
        self.label = None

        start_node: Quadrant
        end_node: Quadrant
        start_node, end_node = node_pair
        if start_node == end_node:
            self.mk_loop()
        else:
            self.mk_link()

    def set_label(self, label: Text) -> None:
        self.label = label
        self.add(label)

    def set_curve(self, curve: CubicBezier) -> None:
        self.curve = curve
        self.add(curve)

    def mk_loop(self) -> None:
        start_node: Quadrant
        end_node: Quadrant
        start_node, end_node = self.node_pair
        if start_node != end_node:
            raise ValueError(f'Expected start_node == end_node but got {start_node} != {end_node}')

        # create the loop
        start_anchor: np.ndarray = self.start_point
        end_anchor: np.ndarray = self.end_point
        start_tangent: np.ndarray
        end_tangent: np.ndarray
        start_tangent, end_tangent = QUADRANT_TO_BASIS[start_node]
        velocity_0: float = 1.5
        acceleration: float = 0.5
        velocity: float = velocity_0 + acceleration * self.sequence_number
        start_handle = start_anchor + velocity * start_tangent
        end_handle = end_anchor + velocity * end_tangent
        curve: CubicBezier = mk_cubic_bezier(start_anchor,
                                            start_handle,
                                            end_handle,
                                            end_anchor)
        self.set_curve(curve)

        # create the label
        curve_midpoint: np.ndarray = curve.point_from_proportion(0.5)
        label: Text = mk_text(self.text, curve_midpoint)
        outward_direction: np.ndarray = start_tangent + end_tangent
        label.move_to(curve_midpoint + 0.125 * outward_direction)
        self.set_label(label)

    def mk_link(self) -> None:
        start_node: Quadrant
        end_node: Quadrant
        start_node, end_node = self.node_pair
        if start_node >= end_node:
            raise ValueError(f'Expected start_node < end_node but got {start_node} >= {end_node}')

        direction: np.ndarray = self.end_point - self.start_point
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
        alpha, beta = (0.5, 0.5) if self.node_pair in diagonals else (0.5, 0.6)

        tangent_displacement: np.ndarray = alpha * unit_tangent
        normal_displacement: np.ndarray = beta * self.sequence_number * unit_normal

        start_handle: np.ndarray = self.start_point + tangent_displacement + normal_displacement
        end_handle: np.ndarray = self.end_point - tangent_displacement + normal_displacement

        curve: CubicBezier = mk_cubic_bezier(self.start_point,
                                            start_handle,
                                            end_handle,
                                            self.end_point)
        self.set_curve(curve)

        # create the label
        curve_midpoint: np.ndarray = curve.point_from_proportion(0.5)
        label: Text = mk_text(self.text, curve_midpoint)
        label.move_to(curve_midpoint + 0.15 * unit_normal)

        self.set_label(label)

    def copy_to(self, start_point: np.ndarray, end_point: np.ndarray) -> Self:
        """
        Copies this LabelledEdge instance to the given start_point and end_point.

        Args:
            start_point: the new start point.
            end_point: the new end point.

        Returns:
            the new LabelledEdge instance at the given start_point and end_point.
        """
        return LabelledEdge(self.node_pair,
                            self.text,
                            self.sequence_number,
                            start_point,
                            end_point)