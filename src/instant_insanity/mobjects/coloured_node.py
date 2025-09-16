import numpy as np

from manim.typing import Point3D
from manim import Dot, ManimColor, DEFAULT_DOT_RADIUS, BLACK

from instant_insanity.core.puzzle import FaceColour
from instant_insanity.mobjects.coloured_cube import MANIM_COLOUR_MAP

DEFAULT_COLOURED_NODE_RADIUS: float = DEFAULT_DOT_RADIUS * 2.0


def mk_dot(face_colour: FaceColour, point: Point3D) -> Dot:
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
                   radius=DEFAULT_COLOURED_NODE_RADIUS,
                   fill_color=fill_colour,
                   stroke_color=BLACK,
                   stroke_width=2)
    return dot
