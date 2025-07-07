"""This module contains the Puzzle class which represents a single Instant Insanity puzzle."""

from dataclasses import dataclass
from enum import IntEnum
from cube import Cube, FaceLabel, FaceColour

class CubeNumber(IntEnum):
    """ The numbers of the cubes in an Instant Insanity puzzle. """
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4

# The Carteblanche 1947 Tantalizer puzzle face colour table
CARTEBLANCHE_PUZZLE: list[str] = [
    'ROWOGG'
    'GRORWW'
    'OWGWGR',
    'WGRGRW'
]

# The Winning Moves face colour table
WINNING_MOVES_PUZZLE: list[str] = [
    'GWBRRR',
    'RGBBWG',
    'WRWBGR',
    'BRGWBW'
]

class Puzzle:
    """ An Instant Insanity puzzle. """
    cubes: dict[CubeNumber, Cube]

    def __init__(self, puzzle: list[str]) -> None:
        """
        Create a puzzle from a face colour table.

        Args:
            puzzle: a list of 4 6-letter strings giving the initial letters of the face colours.

        Raises:
            ValueError: if puzzle is not a list of 4 6-letter strings,
            or if any of the letters are not valid face colour initials.
        """
        n_cubes: int = len(puzzle)
        if n_cubes != 4:
            raise ValueError(f"Expected 4 cubes, got: {n_cubes}")

        for face_colours in puzzle:
            if len(face_colours) != 6 or not face_colours.isalpha():
                raise ValueError(f"Expected a string of 6 face colours, got: {face_colours!r}")

        # STOPPED HERE - is this too complicated? too abstract?
        self.cubes = dict()
        for (i, (cube_number, face_colours)) in enumerate(zip(CubeNumber, puzzle)):
            faces: dict[FaceLabel, FaceColour] = dict()
            for (face_label, face_colour_initial) in zip(FaceLabel, face_colours):
                face_colour = FaceColour.from_initial(face_colour_initial)
                faces[face_label] = face_colour


