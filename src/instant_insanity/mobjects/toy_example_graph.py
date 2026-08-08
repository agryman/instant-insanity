"""
This module makes the toy example graph that is shown in
resources/images/graph_theory/latex/example-multigraph.png
and defined by the TikZ source example-multigraph.tex.

The graph has two connected components:
* a triangle on nodes A, B, C, with a loop at B, and
* a pair of parallel edges that join nodes D and E.

The loop and the parallel edge are edges 5 and 6. Omitting them leaves a simple
graph, since a simple graph has neither loops nor parallel edges.

Manim's Graph and DiGraph classes cannot draw the multigraph.
They store edge mobjects in a dict that is keyed by the node pair, so parallel
edges overwrite each other, and they draw each edge as a Line between the node
centres, so a loop collapses to a point.
Every edge here is therefore drawn directly as a CubicBezier mobject, including
the straight ones, which are the degenerate case in which the two internal
control points lie on the straight segment between the end points. Using one
mobject class for every edge lets the arrow tips be placed by a single
calculation, with no special case per edge kind.
"""
from typing import Self, cast

import numpy as np

from manim import (BLACK, CubicBezier, DEGREES, DL, Dot, DOWN, DR, ManimColor, RIGHT, Text,
                   UL, UP, UR, VGroup, rotate_vector)
from manim.typing import Point3D, Vector3D

from instant_insanity.mobjects.stealth_tip import EdgeTip, mk_stealth_tip_at_node_boundary

NODE_COLOUR: ManimColor = BLACK
NODE_RADIUS: float = 0.12

EDGE_COLOUR: ManimColor = BLACK
EDGE_STROKE_WIDTH: float = 2.0

# the scaling factor for the arrow tips.
TIP_SCALE: float = 0.8

# the factor to narrow the arrow tips by, across their axis.
# a value of 1.0 leaves them at the default Manim width.
TIP_WIDTH_RATIO: float = 0.7

LABEL_COLOUR: ManimColor = BLACK
LABEL_FONT: str = 'sans-serif'
LABEL_FONT_SIZE: float = 28.0
LABEL_BUFF: float = 0.3

# the loop at B leaves the node at -45 degrees and returns to it at 45 degrees.
LOOP_OUT_ANGLE: float = -45.0 * DEGREES
LOOP_IN_ANGLE: float = 45.0 * DEGREES

# the length of the loop control handles. the loop reaches 3 / 8 * sqrt(2) of this
# distance from the node, which is about 0.53 * LOOP_HANDLE_LENGTH.
LOOP_HANDLE_LENGTH: float = 1.5

# the TikZ source bends the parallel edge 6 to the right of the edge D -- E.
BEND_ANGLE: float = 40.0 * DEGREES

# the TikZ source places the nodes on a centimetre grid whose bounding box runs
# from (1, 1.5) to (7.5, 3.5). translate its centre to the origin and scale it up
# so that the graph fills the scene.
TIKZ_CENTRE: Point3D = np.array([4.25, 2.5, 0.0])
TIKZ_SCALE: float = 1.5


def tikz_point(x: float, y: float) -> Point3D:
    """
    Convert a TikZ coordinate to a point in the Manim scene.

    Args:
        x: the TikZ x coordinate in centimetres.
        y: the TikZ y coordinate in centimetres.

    Returns:
        The corresponding point in the Manim scene.
    """
    return (np.array([x, y, 0.0]) - TIKZ_CENTRE) * TIKZ_SCALE


# the node positions, copied from the TikZ \node commands.
NODE_TO_POINT: dict[str, Point3D] = {
    'A': tikz_point(1.0, 2.0),
    'B': tikz_point(3.0, 3.5),
    'C': tikz_point(4.0, 1.5),
    'D': tikz_point(6.0, 2.0),
    'E': tikz_point(7.5, 3.0),
}

# the node label placements, copied from the TikZ label= options.
NODE_TO_LABEL_DIRECTION: dict[str, Vector3D] = {
    'A': DL,
    'B': UP,
    'C': RIGHT,
    'D': DOWN,
    'E': UR,
}


def mk_node(point: Point3D) -> Dot:
    """
    Make a node of the graph.

    Args:
        point: the position of the node.

    Returns:
        The node mobject.
    """
    return Dot(point, radius=NODE_RADIUS, color=NODE_COLOUR)


def mk_label(text: str, point: Point3D, direction: Vector3D, buff: float = LABEL_BUFF) -> Text:
    """
    Make a node or edge label, offset from a point in the given direction.

    Args:
        text: the text of the label.
        point: the point that the label is placed relative to.
        direction: the direction to offset the label in.
        buff: the distance to offset the label by.

    Returns:
        The label mobject.
    """
    label: Text = Text(text, font=LABEL_FONT, font_size=LABEL_FONT_SIZE, color=LABEL_COLOUR)
    label.move_to(point + buff * direction)
    return label


def mk_link(start_point: Point3D, end_point: Point3D) -> CubicBezier:
    """
    Make a straight edge, as drawn by the TikZ -- operator.

    A straight line is the degenerate cubic Bézier curve whose two internal control
    points lie on the straight segment between its end points. Spacing them at one third
    and two thirds of the way along also gives the curve a constant speed
    parameterization. Every edge is therefore a CubicBezier, so the arrow tips need no
    special case for straight edges.

    Args:
        start_point: the position of the start node.
        end_point: the position of the end node.

    Returns:
        The edge mobject.
    """
    displacement: Vector3D = end_point - start_point
    start_handle: Point3D = start_point + displacement / 3.0
    end_handle: Point3D = start_point + 2.0 * displacement / 3.0

    return CubicBezier(start_point, start_handle, end_handle, end_point,
                       color=EDGE_COLOUR, stroke_width=EDGE_STROKE_WIDTH)


def mk_bent_link(start_point: Point3D, end_point: Point3D, bend_angle: float) -> CubicBezier:
    """
    Make a curved edge, as drawn by the TikZ to[bend right=<angle>] operator.

    The curve leaves the start node and arrives at the end node at bend_angle to the
    straight segment that joins them. A positive bend_angle bends the curve to the right
    of the direction of travel.

    Args:
        start_point: the position of the start node.
        end_point: the position of the end node.
        bend_angle: the angle at each node between the curve and the straight segment
            that joins the nodes.

    Returns:
        The edge mobject.
    """
    displacement: Vector3D = end_point - start_point
    distance: float = float(np.linalg.norm(displacement))
    unit_direction: Vector3D = cast(Vector3D, displacement / distance)

    # this handle length makes the curve approximate a circular arc.
    handle_length: float = distance / 3.0
    start_handle: Point3D = start_point + handle_length * rotate_vector(unit_direction, -bend_angle)
    end_handle: Point3D = end_point - handle_length * rotate_vector(unit_direction, bend_angle)

    return CubicBezier(start_point, start_handle, end_handle, end_point,
                       color=EDGE_COLOUR, stroke_width=EDGE_STROKE_WIDTH)


def mk_loop(point: Point3D,
            out_angle: float,
            in_angle: float,
            handle_length: float) -> CubicBezier:
    """
    Make a loop edge, as drawn by the TikZ loop operator.

    Both ends of the curve are at the node. The curve leaves the node in the direction
    out_angle and returns to it from the direction in_angle, so the loop bulges out
    along the bisector of those two directions.

    Args:
        point: the position of the node.
        out_angle: the angle that the curve leaves the node at.
        in_angle: the angle that the curve returns to the node at.
        handle_length: the length of the control handles, which sets the size of the loop.

    Returns:
        The edge mobject.
    """
    start_handle: Point3D = point + handle_length * rotate_vector(RIGHT, out_angle)
    end_handle: Point3D = point + handle_length * rotate_vector(RIGHT, in_angle)

    return CubicBezier(point, start_handle, end_handle, point,
                       color=EDGE_COLOUR, stroke_width=EDGE_STROKE_WIDTH)


class ToyExampleGraph(VGroup):
    """
    The toy example graph, as a mobject whose nodes can be moved.

    The whole figure is derived from the node positions, so moving a node and rebuilding
    brings the edges, the labels and the arrow tips along with it.

    Attributes:
        simple: True if edges 5 and 6 are omitted, leaving a simple graph.
        labelled: True if the node and edge labels are included.
        directed: True if each edge carries a stealth arrow tip.
        node_to_point: maps each node label to the position of that node.
        edges: the edge mobjects.
        tips: the arrow tip mobjects. It is empty unless the graph is directed.
        nodes: the node mobjects.
        node_labels: the node label mobjects. It is empty unless the graph is labelled.
        edge_labels: the edge label mobjects. It is empty unless the graph is labelled.
    """
    simple: bool
    labelled: bool
    directed: bool
    node_to_point: dict[str, Point3D]
    edges: VGroup
    tips: VGroup
    nodes: VGroup
    node_labels: VGroup
    edge_labels: VGroup

    def __init__(self,
                 simple: bool = False,
                 labelled: bool = True,
                 directed: bool = False) -> None:
        """
        Make the toy example graph, with its nodes at their initial positions.

        Args:
            simple: True to omit edges 5 and 6, which are the loop and the parallel
                edge, leaving a simple graph. False to keep them, leaving a multigraph.
            labelled: True to include the node and edge labels, else False.
            directed: True to add a stealth arrow tip to each edge, else False.
        """
        super().__init__()

        self.simple = simple
        self.labelled = labelled
        self.directed = directed

        # copy the points so that moving a node cannot alter the module level positions.
        self.node_to_point = {node: point.copy() for node, point in NODE_TO_POINT.items()}

        self._build()

    def _build(self) -> None:
        """
        Rebuild every component of the graph from the current node positions.

        The components are always added in the same order, and the label and tip groups
        are empty rather than absent when they are switched off, so the structure of the
        mobject does not depend on the flags. That keeps the structure stable across a
        rebuild, which is what lets Manim interpolate one state of the graph into another.
        """
        point_a: Point3D = self.node_to_point['A']
        point_b: Point3D = self.node_to_point['B']
        point_c: Point3D = self.node_to_point['C']
        point_d: Point3D = self.node_to_point['D']
        point_e: Point3D = self.node_to_point['E']

        # the triangle component, and the straight edge of the two node component.
        # the edge label placements are copied from the TikZ node[...] options.
        edge_specs: list[tuple[CubicBezier, str, Vector3D]] = [
            (mk_link(point_a, point_b), '1', UL),
            (mk_link(point_b, point_c), '2', UR),
            (mk_link(point_c, point_a), '3', DR),
            (mk_link(point_d, point_e), '4', UL),
        ]

        if not self.simple:
            # the loop at B and the edge parallel to edge 4 are what make this a
            # multigraph, so a simple graph has neither of them.
            edge_specs += [
                (mk_loop(point_b, LOOP_OUT_ANGLE, LOOP_IN_ANGLE, LOOP_HANDLE_LENGTH), '5', RIGHT),
                (mk_bent_link(point_d, point_e, BEND_ANGLE), '6', DR),
            ]

        self.edges = VGroup(*[edge for edge, _, _ in edge_specs])
        self.nodes = VGroup(*[mk_node(self.node_to_point[node]) for node in NODE_TO_POINT])

        # every edge is a cubic Bézier curve, so each one is tipped the same way.
        self.tips = VGroup()
        if self.directed:
            edge_tips: list[EdgeTip] = [
                EdgeTip(edge, True, mk_stealth_tip_at_node_boundary(edge, NODE_RADIUS,
                                                                    scale=TIP_SCALE,
                                                                    width_ratio=TIP_WIDTH_RATIO))
                for edge in self.edges
            ]
            self.tips = VGroup(*[edge_tip.tip for edge_tip in edge_tips])

        self.node_labels = VGroup()
        self.edge_labels = VGroup()
        if self.labelled:
            self.node_labels = VGroup(*[
                mk_label(node, self.node_to_point[node], direction)
                for node, direction in NODE_TO_LABEL_DIRECTION.items()
            ])
            # the midpoint of the curve works for every edge, unlike the centre of the
            # bounding box, which is off the curve for the loop.
            self.edge_labels = VGroup(*[
                mk_label(text, edge.point_from_proportion(0.5), direction)
                for edge, text, direction in edge_specs
            ])

        # add the edges first so that the nodes are drawn on top of them.
        self.remove(*self.submobjects)
        self.add(self.edges, self.tips, self.nodes, self.node_labels, self.edge_labels)

    def move_node_to(self, node_label: str, point: Point3D) -> Self:
        """
        Move a node to a new position and rebuild the graph around it.

        Every edge that meets the node is redrawn, along with its label and its arrow
        tip, and the node's own label follows it. The whole graph is rebuilt rather than
        just the affected parts, which is simpler and fast enough here.

        Args:
            node_label: the label of the node to move.
            point: the new position of the node.

        Returns:
            This graph, so that calls can be chained.

        Raises:
            ValueError: if node_label is not the label of a node of this graph.
        """
        if node_label not in self.node_to_point:
            raise ValueError(f'Expected one of {sorted(self.node_to_point)} but got: {node_label!r}')

        self.node_to_point[node_label] = np.array(point, dtype=float)
        self._build()

        return self


def mk_toy_example(simple: bool = False,
                   labelled: bool = True,
                   directed: bool = False) -> ToyExampleGraph:
    """
    Make the toy example graph.

    Args:
        simple: True to omit edges 5 and 6, which are the loop and the parallel edge,
            leaving a simple graph. False to keep them, leaving a multigraph.
        labelled: True to include the node and edge labels, else False.
        directed: True to add a stealth arrow tip to each edge, else False.

    Returns:
        The toy example graph.
    """
    return ToyExampleGraph(simple=simple, labelled=labelled, directed=directed)
