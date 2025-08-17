"""
This module defines the Quadrant class which is a string enumeration of the usual
quadrants of the cartesian plane.

We use quadrants to identify the nodes of an opposite-face graph.
"""

from enum import StrEnum
from typing import TypeAlias
import numpy as np
from manim import RIGHT, UP, LEFT, DOWN


class Quadrant(StrEnum):
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"


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

NodePair: TypeAlias = tuple[Quadrant, Quadrant]


def mk_standard_node_pair(quadrant_1: Quadrant, quadrant_2: Quadrant) -> NodePair:
    """
    Returns a pair of nodes in ascending order.

    Args:
        quadrant_1: a node
        quadrant_2: a node

    Returns:
        A pair of nodes in ascending order.
    """

    return min(quadrant_1, quadrant_2), max(quadrant_1, quadrant_2)
