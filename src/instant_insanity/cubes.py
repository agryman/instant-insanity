"""This module contains code for drawing cubes."""

from dataclasses import dataclass
from enum import Enum, IntEnum, StrEnum
import numpy as np

# min and max coordinates of standard cube
CUBE_MIN: float = -1.0
CUBE_MAX: float = 1.0

# 3D coordinates of standard cube vertices
FRT = np.array([CUBE_MAX, CUBE_MAX, CUBE_MAX])
FRB = np.array([CUBE_MAX, CUBE_MAX, CUBE_MIN])
FLT = np.array([CUBE_MAX, CUBE_MIN, CUBE_MAX])
FLB = np.array([CUBE_MAX, CUBE_MIN, CUBE_MIN])
BRT = np.array([CUBE_MIN, CUBE_MAX, CUBE_MAX])
BRB = np.array([CUBE_MIN, CUBE_MAX, CUBE_MIN])
BLT = np.array([CUBE_MIN, CUBE_MIN, CUBE_MAX])
BLB = np.array([CUBE_MIN, CUBE_MIN, CUBE_MIN])


# 3D vertices of standard cube faces
FRONT = np.array([FRT, FLT, FLB, FRB, FRT])
BACK = np.array([BRT, BLT, BLB, BRB, BRT])
RIGHT = np.array([FRT, FRB, BRB, BRT, FRT])
LEFT = np.array([FLT, FLB, BLB, BLT, FLT])
TOP = np.array([FRT, FLT, BLT, BRT, FRT])
BOTTOM = np.array([FRB, FLB, BLB, BRB, FRB])


class FaceLabel(StrEnum):
    """Labels used in Carteblanche 1947."""
    FRONT = "x"
    BACK = "x'"
    RIGHT = "y"
    LEFT = "y'"
    TOP = "z"
    BOTTOM = "z'"


class FaceNumber(IntEnum):
    """Numbers that appear on the faces of a die."""
    FRONT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4
    LEFT = 5
    BACK = 6

    def opposite(self) -> 'FaceNumber':
        """Return the opposite face number."""
        return FaceNumber(7 - self.value)

    def label(self) -> FaceLabel:
        """Return the Carteblanche 1947 label for the face."""
        match self:
            case FaceNumber.FRONT:
                return FaceLabel.FRONT
            case FaceNumber.BACK:
                return FaceLabel.BACK
            case FaceNumber.RIGHT:
                return FaceLabel.RIGHT
            case FaceNumber.LEFT:
                return FaceLabel.LEFT
            case FaceNumber.TOP:
                return FaceLabel.TOP
            case FaceNumber.BOTTOM:
                return FaceLabel.BOTTOM
        raise ValueError(f"Unknown face: {self}")


class FaceColour(StrEnum):
    """Colours that appear on a puzzle block face."""
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    WHITE = 'white'

# use black as the edge colour
BLACK: str = 'black'

@dataclass
class Face:
    """A face of a block"""
    face_number: FaceNumber
    face_colour: FaceColour

    def draw_face(self) -> None:
        """Draw a face."""
        pass


class Cube:
    """ An Instant Insanity puzzle block. """
    pass

class Puzzle:
    """ An Instant Insanity puzzle. """
    pass
