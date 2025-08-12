import numpy as np

from manim import Dot, ManimColor, DEFAULT_DOT_RADIUS, BLACK

from instant_insanity.core.puzzle import FaceColour
from instant_insanity.manim_scenes.coloured_cube import MANIM_COLOUR_MAP


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
