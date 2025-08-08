from typing import TypeAlias
import numpy as np

from manim import VGroup, Mobject, LEFT, UP, RIGHT, DOWN, ManimColor, Dot, DEFAULT_DOT_RADIUS, BLACK, Scene, ORIGIN, \
    FadeIn, tempconfig

from instant_insanity.core.config import ALTERNATE_CONFIG
from instant_insanity.core.puzzle import FaceColour, PuzzleCubeNumber, FaceLabel
from instant_insanity.manim_scenes.coloured_cube import MANIM_COLOUR_MAP

EdgeDictKey: TypeAlias = tuple[PuzzleCubeNumber, FaceLabel]
NodeLayout: TypeAlias = dict[FaceColour, np.ndarray]

CARTEBLANCHE_NODE_LAYOUT: NodeLayout = {
    FaceColour.RED: LEFT + UP,
    FaceColour.ORANGE: RIGHT + UP,
    FaceColour.GREEN: RIGHT + DOWN,
    FaceColour.WHITE: LEFT + DOWN,
}

WINNING_MOVES_NODE_LAYOUT: NodeLayout = {
    FaceColour.RED: LEFT + UP,
    FaceColour.BLUE: RIGHT + UP,
    FaceColour.GREEN: RIGHT + DOWN,
    FaceColour.WHITE: LEFT + DOWN,
}

class OppositeFaceGraph(VGroup):
    """
    This class animates the opposite face graph of a puzzle.

    The graph has four nodes, one for each face colour.
    The node mobjects are stored in the node_dict.
    The key for each node is its FaceColour.

    The graph has zero or more edges.
    The edges mobjects are stored in the edge_dict.
    The key for each edge consists of its:
     * PuzzleCubeNumber,
     * FaceLabel of its right, top, or front face, and

    For example, the edge key for the front-back face of cube 2
    is (PuzzleCubeNumber.TWO, FaceLabel.FRONT).

    Attributes:
        centre: the scene coordinates of the center of the graph
        node_layout: the node layout of the graph relative to the origin
        node_dict: the node dict of mobjects
        edge_dict: the edge dict of mobjects
    """
    centre: np.ndarray
    node_layout: NodeLayout
    node_dict: dict[FaceColour, Mobject]
    edge_dict: dict[EdgeDictKey, Mobject]

    @staticmethod
    def mk_dot(face_colour: FaceColour, point: np.ndarray) -> Mobject:
        """
        Makes a dot for the given face colour and point.
        Args:
            face_colour: the face colour
            point: the centre of the dot

        Returns:
            a Dot mobject
        """
        fill_colour: ManimColor = MANIM_COLOUR_MAP[face_colour]
        dot: Mobject = Dot(point=point,
                           radius=DEFAULT_DOT_RADIUS * 2,
                           fill_color=fill_colour,
                           stroke_color=BLACK,
                           stroke_width=2)
        return dot

    def __init__(self, centre: np.ndarray, node_layout: NodeLayout) -> None:
        """
        Creates a new opposite face graph with no edges.
        """
        super().__init__()
        self.centre = centre
        self.node_layout = node_layout
        self.node_dict = {}
        self.edge_dict = {}

        # initialize the nodes
        face_colour: FaceColour
        position: np.ndarray
        for face_colour, position in node_layout.items():
            point: np.ndarray = position + centre
            node: Mobject = self.mk_dot(face_colour, point)
            self.add(node)
            self.node_dict[face_colour] = node


class FourNodeSquareGraph(Scene):
    def construct(self):
        graph: VGroup = OppositeFaceGraph(2 * RIGHT, WINNING_MOVES_NODE_LAYOUT)
        self.play(FadeIn(graph))
        self.wait()


if __name__ == "__main__":
    with tempconfig(ALTERNATE_CONFIG):
        scene = FourNodeSquareGraph()
        scene.render()
