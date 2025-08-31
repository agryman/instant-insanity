"""This module contains the Puzzle class which represents a single Instant Insanity puzzle."""

from typing import TypeAlias, Self
from enum import IntEnum, StrEnum
from dataclasses import dataclass

from instant_insanity.core.cube import FacePlane, FaceNumber

# there is one opposite face pair for each axis
class AxisLabel(StrEnum):
    """Labels that appear on cube axes that connect pairs of opposite faces."""
    X = 'x'
    Y = 'y'
    Z = 'z'

FacePlanePair: TypeAlias = tuple[FacePlane, FacePlane]

# use the Carteblanche labels
INITIAL_AXIS_TO_FACE_NAME_PAIR: dict[AxisLabel, FacePlanePair] = {
    AxisLabel.X: (FacePlane.FRONT, FacePlane.BACK),
    AxisLabel.Y: (FacePlane.RIGHT, FacePlane.LEFT),
    AxisLabel.Z: (FacePlane.TOP, FacePlane.BOTTOM)
}

INITIAL_FACE_NAME_TO_AXIS: dict[FacePlane, AxisLabel] = {
    FacePlane.FRONT: AxisLabel.X,
    FacePlane.BACK: AxisLabel.X,
    FacePlane.RIGHT: AxisLabel.Y,
    FacePlane.LEFT: AxisLabel.Y,
    FacePlane.TOP: AxisLabel.Z,
    FacePlane.BOTTOM: AxisLabel.Z
}

class FaceLabel(StrEnum):
    """Labels that appear on the faces of a cube in Carteblanche 1947."""
    X = "x"
    X_PRIME = "x'"
    Y = "y"
    Y_PRIME = "y'"
    Z = "z"
    Z_PRIME = "z'"

# map face names to face labels
INITIAL_FACE_NAME_TO_LABEL: dict[FacePlane, FaceLabel] = {
    FacePlane.FRONT: FaceLabel.X,
    FacePlane.RIGHT: FaceLabel.Y,
    FacePlane.TOP: FaceLabel.Z,
    FacePlane.BOTTOM: FaceLabel.Z_PRIME,
    FacePlane.LEFT: FaceLabel.Y_PRIME,
    FacePlane.BACK: FaceLabel.X_PRIME
}

# map face labels to face names
INITIAL_FACE_LABEL_TO_NAME: dict[FaceLabel, FacePlane] = {
    FaceLabel.X: FacePlane.FRONT,
    FaceLabel.X_PRIME: FacePlane.BACK,
    FaceLabel.Y: FacePlane.RIGHT,
    FaceLabel.Y_PRIME: FacePlane.LEFT,
    FaceLabel.Z: FacePlane.TOP,
    FaceLabel.Z_PRIME: FacePlane.BOTTOM
}

# map face numbers to face labels
FACE_NUMBER_TO_LABEL: dict[FaceNumber, FaceLabel] = {
    FaceNumber.THREE: FaceLabel.X,
    FaceNumber.ONE: FaceLabel.Y,
    FaceNumber.TWO: FaceLabel.Z,
    FaceNumber.FIVE: FaceLabel.Z_PRIME,
    FaceNumber.SIX: FaceLabel.Y_PRIME,
    FaceNumber.FOUR: FaceLabel.X_PRIME
}

# map face labels to face numbers
FACE_LABEL_TO_NUMBER: dict[FaceLabel, FaceNumber] = {
    FaceLabel.X: FaceNumber.THREE,
    FaceLabel.X_PRIME: FaceNumber.FOUR,
    FaceLabel.Y: FaceNumber.ONE,
    FaceLabel.Y_PRIME: FaceNumber.SIX,
    FaceLabel.Z: FaceNumber.TWO,
    FaceLabel.Z_PRIME: FaceNumber.FIVE
}

class FaceColour(StrEnum):
    """Colours that appear on a puzzle cube face."""
    BLUE = 'blue'
    GREEN = 'green'
    ORANGE = 'orange'
    PURPLE = 'purple'
    RED = 'red'
    WHITE = 'white'
    YELLOW = 'yellow'

    @classmethod
    def from_initial(cls, c: str) -> Self:
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
            raise ValueError(f"Expected a single alphabetic character but got: {c!r}")

        c = c.upper()
        for member in cls:
            if member.name.startswith(c):
                return member

        raise ValueError(f"No FaceColour member name starts with '{c}'")

# use black as the default colour for cube face edges
DEFAULT_EDGE_COLOUR: str = 'black'

FaceColourPair: TypeAlias = tuple[FaceColour, FaceColour]

# PuzzleCubeSpec is a string of six characters.
# Each character is the initial letter of a face colour.
# The colours are listed in the Carteblache label order: x, x', y, y', z, z'.
# This is the order of the enum FaceLabel.
PuzzleCubeSpec: TypeAlias = str


@dataclass
class PuzzleCube:
    """
    An Instant Insanity puzzle cube. A cube has a colour assigned to each face.

    Attributes:
        cube_spec: the puzzle cube specification
        name_to_colour: maps face names to face colours.

    """
    cube_spec: PuzzleCubeSpec
    name_to_colour: dict[FacePlane, FaceColour]

    def __init__(self, cube_spec: PuzzleCubeSpec):
        # cube_spec must be a string of six face colour initials
        if not isinstance(cube_spec, str):
            raise ValueError(f"Expected a string, got {type(cube_spec).__name__}")
        if len(cube_spec) != 6:
            raise ValueError(f"Expected string of length 6, got length {len(cube_spec)}")

        self.cube_spec = cube_spec

        label: FaceLabel
        initial: str
        self.name_to_colour = {INITIAL_FACE_LABEL_TO_NAME[label]: FaceColour.from_initial(initial)
                               for label, initial in zip(FaceLabel, cube_spec)}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PuzzleCube):
            return NotImplemented
        return self.name_to_colour == other.name_to_colour

    def get_axis_to_face_colour_pair(self) -> dict[AxisLabel, FaceColourPair]:

        axis_to_face_colour_pair: dict[AxisLabel, FaceColourPair] = {}
        axis: AxisLabel
        face_name_pair: FacePlanePair
        for axis, face_name_pair in INITIAL_AXIS_TO_FACE_NAME_PAIR.items():
            name1: FacePlane
            name2: FacePlane
            name1, name2 = face_name_pair
            colour1: FaceColour = self.name_to_colour[name1]
            colour2: FaceColour = self.name_to_colour[name2]
            axis_to_face_colour_pair[axis] = (colour1, colour2)

        return axis_to_face_colour_pair

    def get_colours(self) -> list[FaceColour]:
        return list(set(self.name_to_colour.values()))

class PuzzleCubeNumber(IntEnum):
    """ The numbers of the cubes in an Instant Insanity puzzle. """
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

CubeAxis: TypeAlias = tuple[PuzzleCubeNumber, AxisLabel]

# PuzzleSpec is a list of four strings, one per cube.
# Each string contains six characters that are the initial letters of the face colours.
PuzzleSpec: TypeAlias = list[PuzzleCubeSpec]

# The 1947 Carteblanche Tantalizer puzzle specification
CARTEBLANCHE_PUZZLE_SPEC: PuzzleSpec = [
    'ROWOGG',
    'GRORWW',
    'OWGWGR',
    'WGRGRW'
]

# The 1967 Winning Moves Instant Insanity puzzle specification
WINNING_MOVES_PUZZLE_SPEC: PuzzleSpec = [
    'GWBRRR',
    'RGBBWG',
    'WRWBGR',
    'BRGWBW'
]

class Puzzle:
    """
    An Instant Insanity puzzle.

    Attributes:
        number_to_cube: maps cube numbers to puzzle cubes.
    """
    puzzle_spec: PuzzleSpec
    number_to_cube: dict[PuzzleCubeNumber, PuzzleCube]

    def __init__(self, puzzle_spec: PuzzleSpec) -> None:
        """
        Create a puzzle from a specification.

        Args:
            puzzle_spec: a list of 4 6-letter strings giving the initial letters of the face colours.

        Raises:
            ValueError: if puzzle is not a list of 4 6-letter strings,
            or if any of the letters are not valid face colour initials.
        """
        n_cubes: int = len(puzzle_spec)
        if n_cubes != 4:
            raise ValueError(f"Expected 4 cubes, got: {n_cubes}")

        self.puzzle_spec = puzzle_spec
        self.number_to_cube = {
            cube_number: PuzzleCube(cube_spec)
            for cube_number, cube_spec in zip(PuzzleCubeNumber, puzzle_spec)
        }

    def mk_colours(self) -> set[FaceColour]:

        colours: set[FaceColour] = {
            colour
            for cube in self.number_to_cube.values()
            for colour in cube.name_to_colour.values()
        }
        return colours

    def mk_cube_axis_to_face_colour_pair(self) -> dict[CubeAxis, tuple[FaceColour, FaceColour]]:
        cube_axis_to_face_colour_pair: dict[CubeAxis, FaceColourPair] = {}
        number: PuzzleCubeNumber
        cube: PuzzleCube
        for number, cube in self.number_to_cube.items():
            axis: AxisLabel
            face_colour_pair: FaceColourPair
            axis_to_face_colour_pair: dict[AxisLabel, FaceColourPair] = cube.get_axis_to_face_colour_pair()
            for axis, face_colour_pair in axis_to_face_colour_pair.items():
                cube_axis_to_face_colour_pair[(number, axis)] = face_colour_pair
        return cube_axis_to_face_colour_pair

    def get_colours(self) -> list[FaceColour]:
        cube_colour_lists: list[list[FaceColour]] = [cube.get_colours()
                                               for cube in self.number_to_cube.values()]
        cube_colour_list: list[FaceColour]
        colour: FaceColour
        puzzle_colours: set[FaceColour] = {colour
                                           for cube_colour_list in cube_colour_lists
                                           for colour in cube_colour_list}
        return list(puzzle_colours)

WINNING_MOVES_PUZZLE: Puzzle = Puzzle(WINNING_MOVES_PUZZLE_SPEC)
WINNING_MOVES_COLOURS: set[FaceColour] = WINNING_MOVES_PUZZLE.mk_colours()

CARTEBLANCHE_PUZZLE: Puzzle = Puzzle(CARTEBLANCHE_PUZZLE_SPEC)
CARTEBLANCHE_COLOURS: set[FaceColour] = CARTEBLANCHE_PUZZLE.mk_colours()
