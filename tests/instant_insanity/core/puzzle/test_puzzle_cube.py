import pytest
from instant_insanity.core.cube import FacePlane
from instant_insanity.core.puzzle import (FaceColour, PuzzleCube, PuzzleCubeNumber, Puzzle,
                                          CARTEBLANCHE_PUZZLE_SPEC, WINNING_MOVES_PUZZLE_SPEC)

TANTALIZER_1 = { # ROWOGG
    FacePlane.FRONT: FaceColour.RED,
    FacePlane.BACK: FaceColour.ORANGE,
    FacePlane.RIGHT: FaceColour.WHITE,
    FacePlane.LEFT: FaceColour.ORANGE,
    FacePlane.TOP: FaceColour.GREEN,
    FacePlane.BOTTOM: FaceColour.GREEN
}

TANTALIZER_2 = { # GRORWW
    FacePlane.FRONT: FaceColour.GREEN,
    FacePlane.BACK: FaceColour.RED,
    FacePlane.RIGHT: FaceColour.ORANGE,
    FacePlane.LEFT: FaceColour.RED,
    FacePlane.TOP: FaceColour.WHITE,
    FacePlane.BOTTOM: FaceColour.WHITE
}

TANTALIZER_3 = { # OWGWGR
    FacePlane.FRONT: FaceColour.ORANGE,
    FacePlane.BACK: FaceColour.WHITE,
    FacePlane.RIGHT: FaceColour.GREEN,
    FacePlane.LEFT: FaceColour.WHITE,
    FacePlane.TOP: FaceColour.GREEN,
    FacePlane.BOTTOM: FaceColour.RED
}

TANTALIZER_4 = { # WGRGRW
    FacePlane.FRONT: FaceColour.WHITE,
    FacePlane.BACK: FaceColour.GREEN,
    FacePlane.RIGHT: FaceColour.RED,
    FacePlane.LEFT: FaceColour.GREEN,
    FacePlane.TOP: FaceColour.RED,
    FacePlane.BOTTOM: FaceColour.WHITE
}

WINNING_MOVES_1 = { # GWBRRR
    FacePlane.FRONT: FaceColour.GREEN,
    FacePlane.BACK: FaceColour.WHITE,
    FacePlane.RIGHT: FaceColour.BLUE,
    FacePlane.LEFT: FaceColour.RED,
    FacePlane.TOP: FaceColour.RED,
    FacePlane.BOTTOM: FaceColour.RED
}

WINNING_MOVES_2 = { # RGBBWG
    FacePlane.FRONT: FaceColour.RED,
    FacePlane.BACK: FaceColour.GREEN,
    FacePlane.RIGHT: FaceColour.BLUE,
    FacePlane.LEFT: FaceColour.BLUE,
    FacePlane.TOP: FaceColour.WHITE,
    FacePlane.BOTTOM: FaceColour.GREEN
}

WINNING_MOVES_3 = { # WRWBGR
    FacePlane.FRONT: FaceColour.WHITE,
    FacePlane.BACK: FaceColour.RED,
    FacePlane.RIGHT: FaceColour.WHITE,
    FacePlane.LEFT: FaceColour.BLUE,
    FacePlane.TOP: FaceColour.GREEN,
    FacePlane.BOTTOM: FaceColour.RED
}

WINNING_MOVES_4 = { # BRGWBW
    FacePlane.FRONT: FaceColour.BLUE,
    FacePlane.BACK: FaceColour.RED,
    FacePlane.RIGHT: FaceColour.GREEN,
    FacePlane.LEFT: FaceColour.WHITE,
    FacePlane.TOP: FaceColour.BLUE,
    FacePlane.BOTTOM: FaceColour.WHITE
}

@pytest.mark.parametrize(
    "cube_spec, expected_faces",
    [
        ('wwwwww', {face_name: FaceColour.WHITE for face_name in FacePlane}),
        ('WWWWWW', {face_name: FaceColour.WHITE for face_name in FacePlane}),
        (CARTEBLANCHE_PUZZLE_SPEC[0], TANTALIZER_1),
        (CARTEBLANCHE_PUZZLE_SPEC[1], TANTALIZER_2),
        (CARTEBLANCHE_PUZZLE_SPEC[2], TANTALIZER_3),
        (CARTEBLANCHE_PUZZLE_SPEC[3], TANTALIZER_4),
        (WINNING_MOVES_PUZZLE_SPEC[0], WINNING_MOVES_1),
        (WINNING_MOVES_PUZZLE_SPEC[1], WINNING_MOVES_2),
        (WINNING_MOVES_PUZZLE_SPEC[2], WINNING_MOVES_3),
        (WINNING_MOVES_PUZZLE_SPEC[3], WINNING_MOVES_4)
    ]
)
def test_puzzle_cube(cube_spec, expected_faces):
    puzzle_cube: PuzzleCube = PuzzleCube(cube_spec)
    assert puzzle_cube.name_to_colour == expected_faces

@pytest.mark.parametrize(
    "puzzle_spec, expected_cubes",
    [
        (CARTEBLANCHE_PUZZLE_SPEC, [TANTALIZER_1, TANTALIZER_2, TANTALIZER_3, TANTALIZER_4]),
        (WINNING_MOVES_PUZZLE_SPEC, [WINNING_MOVES_1, WINNING_MOVES_2, WINNING_MOVES_3, WINNING_MOVES_4])
    ]
)
def test_puzzle(puzzle_spec, expected_cubes):
    puzzle: Puzzle = Puzzle(puzzle_spec)
    for (i, cube_number) in enumerate(PuzzleCubeNumber):
        assert puzzle.number_to_cube[cube_number].name_to_colour == expected_cubes[i]
