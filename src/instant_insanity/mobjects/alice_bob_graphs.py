"""
This module creates two example graphs.

NeighbourGraph is an undirected graph that means Alice and Bob are neighbours.
LikesGraph is a directed graph that means Alice likes Bob.
"""
from manim import VGroup, RIGHT, LEFT, UP, DOWN, CubicBezier
from manim.typing import Point3D, Vector3D

from instant_insanity.mobjects.stealth_tip import EdgeTip, mk_stealth_tip_at_node_boundary
from instant_insanity.mobjects.toy_example_graph import mk_link, mk_label, mk_node, NODE_RADIUS, TIP_SCALE, \
    TIP_WIDTH_RATIO

ALICE: str = "Alice"
BOB: str = "Bob"

NODE_TO_POINT: dict[str, Point3D] = {
    ALICE: 1.5 * LEFT,
    BOB: 1.5 * RIGHT,
}

NODE_TO_LABEL_DIRECTION: dict[str, Vector3D] = {
    ALICE: DOWN,
    BOB: DOWN,
}

class AliceBobGraph(VGroup):
    def __init__(self, edge_label: str, directed: bool) -> None:
        super().__init__()

        self.labelled = True
        self.edge_label = edge_label
        self.directed = directed

        self.node_to_point = NODE_TO_POINT.copy()

        point_alice: Point3D = self.node_to_point[ALICE]
        point_bob: Point3D = self.node_to_point[BOB]

        edge_specs: list[tuple[CubicBezier, str, Vector3D]] = [
            (mk_link(point_alice, point_bob), edge_label, UP),
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
