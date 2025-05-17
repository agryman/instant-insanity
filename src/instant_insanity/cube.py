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

class FaceLabel(StrEnum):
    """Labels that appear on the faces of a cube in Carteblanche 1947."""
    FRONT = "x"
    BACK = "x'"
    RIGHT = "y"
    LEFT = "y'"
    TOP = "z"
    BOTTOM = "z'"


FACE_NUMBER_TO_LABEL: dict[FaceNumber, FaceLabel] = {
    FaceNumber.FRONT: FaceLabel.FRONT,
    FaceNumber.RIGHT: FaceLabel.RIGHT,
    FaceNumber.TOP: FaceLabel.TOP,
    FaceNumber.BOTTOM: FaceLabel.BOTTOM,
    FaceNumber.LEFT: FaceLabel.LEFT,
    FaceNumber.BACK: FaceLabel.BACK
}

FACE_LABEL_TO_NUMBER: dict[FaceLabel, FaceNumber] = {
    FaceLabel.FRONT: FaceNumber.FRONT,
    FaceLabel.BACK: FaceNumber.BACK,
    FaceLabel.RIGHT: FaceNumber.RIGHT,
    FaceLabel.LEFT: FaceNumber.LEFT,
    FaceLabel.TOP: FaceNumber.TOP,
    FaceLabel.BOTTOM: FaceNumber.BOTTOM
}

class FaceColour(StrEnum):
    """Colours that appear on a puzzle cube face."""
    BLUE = 'dodgerblue'
    GREEN = 'forestgreen'
    ORANGE = 'orange'
    PURPLE = 'purple'
    RED = 'red'
    WHITE = 'white'
    YELLOW = 'yellow'

    @classmethod
    def from_initial(cls, c: str) -> 'FaceColour':
        """
        Return the FaceColour object whose member name starts with the input character, ignoring case.

        Args:
            c: a single alphabetic character, e.g. 'R' or 'r'

        Returns:
            The FaceColour object whose member name starts with the input character, ignoring case.

        Raises:
            ValueError: if c is not a single alphabetic character, or if there is no match.
        """
        if len(c) != 1 or not c.isalpha():
            raise ValueError(f"Expected a single alphabetic character, got: {c!r}")

        c = c.upper()
        for member in cls:
            if member.name.startswith(c):
                return member

        raise ValueError(f"No FaceColour member name starts with '{c}'")

# use black as the default edge colour for cube faces
DEFAULT_EDGE_COLOUR: str = 'black'

@dataclass
class Face:
    """A face of a cube"""
    face_number: FaceNumber
    face_colour: FaceColour


@dataclass
class Cube:
    """ An Instant Insanity puzzle cube. """
    faces: dict[FaceLabel, FaceColour]
