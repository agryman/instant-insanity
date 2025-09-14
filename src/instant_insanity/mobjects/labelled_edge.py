"""
This module implements the LabelledEdge class which is used in the OppositeFaceGraph.
"""
from typing import Self
import numpy as np

from manim import CubicBezier, Text, VGroup, ManimColor, BLACK, OUT
from manim.typing import Point3D

from instant_insanity.mobjects.quadrant import Quadrant, NodePair, QUADRANT_TO_BASIS

type PointPair = tuple[Point3D, Point3D]

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

def compute_alpha_from_points(point_0: Point3D, point_1: Point3D, point_alpha: Point3D) -> float:
    if np.allclose(point_0, point_1):
        raise ValueError('Expected point_1 != point_0.')
    alpha: float
    if np.allclose(point_0, point_alpha):
        alpha = 0.0
    elif np.allclose(point_1, point_alpha):
        alpha = 1.0
    else:
        numerator: float = float(np.linalg.norm(point_alpha - point_0))
        denominator: float = float(np.linalg.norm(point_1 - point_0))
        alpha = numerator / denominator

    return alpha

def check_alpha_from_points(point_0: Point3D, point_1: Point3D, point_alpha: Point3D, alpha: float):
    point_alpha_predicted: Point3D = (1.0 - alpha) * point_0 + alpha * point_1
    if not np.allclose(point_alpha, point_alpha_predicted):
        raise ValueError('Predicted point_alpha is not close to actual point_alpha.')

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
        point_pair_0: the initial point pair of the curve.
        point_pair_1: the final point pair of the curve.
        point_pair_alpha: the intermediate point pair of the curve.
        moving: True if the edge is moving, else False.
        label: The label of the edge. It is a submobject.
        curve: The curve followed by the edge. It is a submobject.
    """
    node_pair: NodePair
    text: str
    sequence_number: int
    point_pair_0: PointPair
    point_pair_1: PointPair
    point_pair_alpha: PointPair
    moving: bool
    curve: CubicBezier
    label: Text

    def __init__(self,
                 node_pair: NodePair,
                 text: str,
                 sequence_number: int,
                 point_pair_0: PointPair,
                 point_pair_1: PointPair,
                 point_pair_alpha: PointPair,
                 moving: bool = True) -> None:

        alpha: float
        if moving:
            # check that some movement will occur
            start_point_0: Point3D = point_pair_0[0]
            start_point_1: Point3D = point_pair_1[0]
            if np.allclose(start_point_0, start_point_1):
                raise ValueError(f'Expected start_point_0 to not equal start_point_1')

            end_point_0: Point3D = point_pair_0[1]
            end_point_1: Point3D = point_pair_1[1]
            if np.allclose(end_point_0, end_point_1):
                raise ValueError(f'Expected end_point_0 to not equal end_point_1')

            # compute alpha from the point pairs and verify that they are reasonable
            start_point_alpha: Point3D = point_pair_alpha[0]
            end_point_alpha: Point3D = point_pair_alpha[1]
            alpha = compute_alpha_from_points(start_point_0, start_point_1, start_point_alpha)
            check_alpha_from_points(start_point_0, start_point_1, start_point_alpha, alpha)
            check_alpha_from_points(end_point_0, end_point_1, end_point_alpha, alpha)
        else:
            # treat a nonmoving edge as if it has completed the move and is sitting on the graph
            assert point_pair_0 == point_pair_1 == point_pair_alpha
            alpha = 1.0

        # the given points are reasonable so proceed with constructing the edge

        super().__init__()

        self.node_pair = node_pair
        self.text = text
        self.sequence_number = sequence_number
        self.point_pair_0 = point_pair_0
        self.point_pair_1 = point_pair_1
        self.point_pair_alpha = point_pair_alpha
        self.alpha = alpha

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
        start_anchor_alpha: np.ndarray
        end_anchor_alpha: np.ndarray
        start_anchor_alpha, end_anchor_alpha = self.point_pair_alpha

        start_tangent_1: np.ndarray
        end_tangent_1: np.ndarray
        start_tangent_1, end_tangent_1 = QUADRANT_TO_BASIS[start_node]

        velocity_base: float = 1.5
        acceleration: float = 0.5
        velocity: float = velocity_base + acceleration * self.sequence_number
        start_handle = start_anchor_alpha + velocity * start_tangent_1 * self.alpha
        end_handle = end_anchor_alpha + velocity * end_tangent_1 * self.alpha
        curve: CubicBezier = mk_cubic_bezier(start_anchor_alpha,
                                            start_handle,
                                            end_handle,
                                            end_anchor_alpha)
        self.set_curve(curve)

        # create the label
        curve_midpoint: np.ndarray = curve.point_from_proportion(0.5)
        label: Text = mk_text(self.text, curve_midpoint)
        outward_direction_1: np.ndarray = start_tangent_1 + end_tangent_1
        label.move_to(curve_midpoint + 0.125 * outward_direction_1)
        self.set_label(label)

    def mk_link(self) -> None:
        start_node: Quadrant
        end_node: Quadrant
        start_node, end_node = self.node_pair
        if start_node >= end_node:
            raise ValueError(f'Expected start_node < end_node but got {start_node} >= {end_node}')

        start_alpha: Point3D
        end_alpha: Point3D
        start_alpha, end_alpha = self.point_pair_alpha

        direction_alpha: np.ndarray = end_alpha - start_alpha
        unit_tangent_alpha: np.ndarray = direction_alpha / np.linalg.norm(direction_alpha)
        unit_normal_alpha: np.ndarray = np.cross(unit_tangent_alpha, OUT)

        # special case treatment: reverse the normal for (I,IV) edges so it points outward
        if start_node == Quadrant.I and end_node == Quadrant.IV:
            unit_normal_alpha = -1.0 * unit_normal_alpha

        # create the curve
        diagonals: set[NodePair] = {
            (Quadrant.I, Quadrant.III),
            (Quadrant.II, Quadrant.IV)
        }
        a: float
        b: float
        a, b = (0.5, 0.5) if self.node_pair in diagonals else (0.5, 0.6)

        tangent_displacement_alpha: np.ndarray = a * unit_tangent_alpha
        normal_displacement_alpha: np.ndarray = b * self.alpha * self.sequence_number * unit_normal_alpha

        start_point_alpha, end_point_alpha = self.point_pair_alpha

        start_handle_alpha: np.ndarray = start_point_alpha + tangent_displacement_alpha + normal_displacement_alpha
        end_handle_alpha: np.ndarray = end_point_alpha - tangent_displacement_alpha + normal_displacement_alpha

        curve: CubicBezier = mk_cubic_bezier(start_point_alpha,
                                             start_handle_alpha,
                                             end_handle_alpha,
                                             end_point_alpha)

        self.set_curve(curve)

        # create the label
        curve_midpoint: np.ndarray = curve.point_from_proportion(0.5)
        label: Text = mk_text(self.text, curve_midpoint)
        label.move_to(curve_midpoint + 0.15 * unit_normal_alpha)

        self.set_label(label)

    def copy_from_to(self,
                     point_pair_0: PointPair,
                     point_pair_1: PointPair,
                     point_pair_alpha: PointPair) -> Self:
        """
        Copies this LabelledEdge instance to the given start_point and end_point.

        Args:
            point_pair_0: the initial point pair of the curve.
            point_pair_1: the final point pair of the curve.
            point_pair_alpha: the current intermediate point pair of the curve.

        Returns:
            the new LabelledEdge instance at the given current point pair.
        """
        return LabelledEdge(self.node_pair,
                            self.text,
                            self.sequence_number,
                            point_pair_0,
                            point_pair_1,
                            point_pair_alpha)
