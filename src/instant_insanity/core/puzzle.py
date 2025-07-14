"""This module contains the Puzzle class which represents a single Instant Insanity puzzle."""

from enum import IntEnum, StrEnum
from dataclasses import dataclass
from instant_insanity.core.cube import FaceName, FaceNumber

class FaceLabel(StrEnum):
    """Labels that appear on the faces of a cube in Carteblanche 1947."""
    FRONT = "x"
    BACK = "x'"
    RIGHT = "y"
    LEFT = "y'"
    TOP = "z"
    BOTTOM = "z'"

# map face names to face labels
FACE_NAME_TO_LABEL: dict[FaceName, FaceLabel] = {
    FaceName.FRONT: FaceLabel.FRONT,
    FaceName.RIGHT: FaceLabel.RIGHT,
    FaceName.TOP: FaceLabel.TOP,
    FaceName.BOTTOM: FaceLabel.BOTTOM,
    FaceName.LEFT: FaceLabel.LEFT,
    FaceName.BACK: FaceLabel.BACK
}

# map face labels to face names
FACE_LABEL_TO_NAME: dict[FaceLabel, FaceName] = {
    FaceLabel.FRONT: FaceName.FRONT,
    FaceLabel.BACK: FaceName.BACK,
    FaceLabel.RIGHT: FaceName.RIGHT,
    FaceLabel.LEFT: FaceName.LEFT,
    FaceLabel.TOP: FaceName.TOP,
    FaceLabel.BOTTOM: FaceName.BOTTOM
}

# map face numbers to face labels
FACE_NUMBER_TO_LABEL: dict[FaceNumber, FaceLabel] = {
    FaceNumber.FRONT: FaceLabel.FRONT,
    FaceNumber.RIGHT: FaceLabel.RIGHT,
    FaceNumber.TOP: FaceLabel.TOP,
    FaceNumber.BOTTOM: FaceLabel.BOTTOM,
    FaceNumber.LEFT: FaceLabel.LEFT,
    FaceNumber.BACK: FaceLabel.BACK
}

# map face labels to face numbers
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

# use black as the default colour for cube face edges
DEFAULT_EDGE_COLOUR: str = 'black'

# PuzzleCubeSpec is a string of six characters.
# Each character is the initial letter of a face colour.
# The colours are listed in the Carteblache label order: x, x', y, y', z, z'.
# This is the order of the enum FaceLabel.
PuzzleCubeSpec = str


@dataclass
class PuzzleCube:
    """ An Instant Insanity puzzle cube. A cube has a colour assigned to each face."""
    faces: dict[FaceName, FaceColour]

    def __init__(self, cube_spec: PuzzleCubeSpec):
        # cube_spec must be a string of six face colour initials
        if not isinstance(cube_spec, str):
            raise ValueError(f"Expected a string, got {type(cube_spec).__name__}")
        if len(cube_spec) != 6:
            raise ValueError(f"Expected string of length 6, got length {len(cube_spec)}")

        self.faces = {FACE_LABEL_TO_NAME[label]: FaceColour.from_initial(initial)
                      for label, initial in zip(FaceLabel, cube_spec)}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PuzzleCube):
            return NotImplemented
        return self.faces == other.faces

class PuzzleCubeNumber(IntEnum):
    """ The numbers of the cubes in an Instant Insanity puzzle. """
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

# PuzzleSpec is a list of four strings, one per cube.
# Each string contains six characters that are the initial letters of the face colours.
PuzzleSpec = list[PuzzleCubeSpec]

# The Carteblanche 1947 Tantalizer puzzle specification
TANTALIZER_PUZZLE: PuzzleSpec = [
    'ROWOGG',
    'GRORWW',
    'OWGWGR',
    'WGRGRW'
]

# The Winning Moves puzzle specification
WINNING_MOVES_PUZZLE: PuzzleSpec = [
    'GWBRRR',
    'RGBBWG',
    'WRWBGR',
    'BRGWBW'
]

class Puzzle:
    """ An Instant Insanity puzzle. """
    cubes: dict[PuzzleCubeNumber, PuzzleCube]

    def __init__(self, puzzle: PuzzleSpec) -> None:
        """
        Create a puzzle from a specification.

        Args:
            puzzle: a list of 4 6-letter strings giving the initial letters of the face colours.

        Raises:
            ValueError: if puzzle is not a list of 4 6-letter strings,
            or if any of the letters are not valid face colour initials.
        """
        n_cubes: int = len(puzzle)
        if n_cubes != 4:
            raise ValueError(f"Expected 4 cubes, got: {n_cubes}")

        self.cubes = {cube_number: PuzzleCube(cube_spec) for cube_number, cube_spec in zip(PuzzleCubeNumber, puzzle)}
