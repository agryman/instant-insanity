import pytest
from instant_insanity.core.puzzle import (FaceColour, PuzzleCube, PuzzleCubeNumber, Puzzle,
                                          CARTEBLANCHE_PUZZLE_SPEC, WINNING_MOVES_PUZZLE_SPEC, FaceLabel)

CARTEBLANCHE_1 = { # ROWOGG
    FaceLabel.X: FaceColour.RED,
    FaceLabel.X_PRIME: FaceColour.ORANGE,
    FaceLabel.Y: FaceColour.WHITE,
    FaceLabel.Y_PRIME: FaceColour.ORANGE,
    FaceLabel.Z: FaceColour.GREEN,
    FaceLabel.Z_PRIME: FaceColour.GREEN
}

CARTEBLANCHE_2 = { # GRORWW
    FaceLabel.X: FaceColour.GREEN,
    FaceLabel.X_PRIME: FaceColour.RED,
    FaceLabel.Y: FaceColour.ORANGE,
    FaceLabel.Y_PRIME: FaceColour.RED,
    FaceLabel.Z: FaceColour.WHITE,
    FaceLabel.Z_PRIME: FaceColour.WHITE
}

CARTEBLANCHE_3 = { # OWGWGR
    FaceLabel.X: FaceColour.ORANGE,
    FaceLabel.X_PRIME: FaceColour.WHITE,
    FaceLabel.Y: FaceColour.GREEN,
    FaceLabel.Y_PRIME: FaceColour.WHITE,
    FaceLabel.Z: FaceColour.GREEN,
    FaceLabel.Z_PRIME: FaceColour.RED
}

CARTEBLANCHE_4 = { # WGRGRW
    FaceLabel.X: FaceColour.WHITE,
    FaceLabel.X_PRIME: FaceColour.GREEN,
    FaceLabel.Y: FaceColour.RED,
    FaceLabel.Y_PRIME: FaceColour.GREEN,
    FaceLabel.Z: FaceColour.RED,
    FaceLabel.Z_PRIME: FaceColour.WHITE
}

WINNING_MOVES_1 = { # GWBRRR
    FaceLabel.X: FaceColour.GREEN,
    FaceLabel.X_PRIME: FaceColour.WHITE,
    FaceLabel.Y: FaceColour.BLUE,
    FaceLabel.Y_PRIME: FaceColour.RED,
    FaceLabel.Z: FaceColour.RED,
    FaceLabel.Z_PRIME: FaceColour.RED
}

WINNING_MOVES_2 = { # RGBBWG
    FaceLabel.X: FaceColour.RED,
    FaceLabel.X_PRIME: FaceColour.GREEN,
    FaceLabel.Y: FaceColour.BLUE,
    FaceLabel.Y_PRIME: FaceColour.BLUE,
    FaceLabel.Z: FaceColour.WHITE,
    FaceLabel.Z_PRIME: FaceColour.GREEN
}

WINNING_MOVES_3 = { # WRWBGR
    FaceLabel.X: FaceColour.WHITE,
    FaceLabel.X_PRIME: FaceColour.RED,
    FaceLabel.Y: FaceColour.WHITE,
    FaceLabel.Y_PRIME: FaceColour.BLUE,
    FaceLabel.Z: FaceColour.GREEN,
    FaceLabel.Z_PRIME: FaceColour.RED
}

WINNING_MOVES_4 = { # BRGWBW
    FaceLabel.X: FaceColour.BLUE,
    FaceLabel.X_PRIME: FaceColour.RED,
    FaceLabel.Y: FaceColour.GREEN,
    FaceLabel.Y_PRIME: FaceColour.WHITE,
    FaceLabel.Z: FaceColour.BLUE,
    FaceLabel.Z_PRIME: FaceColour.WHITE
}

@pytest.mark.parametrize(
    "cube_spec, expected_faces",
    [
        ('wwwwww', {face_label: FaceColour.WHITE for face_label in FaceLabel}),
        ('WWWWWW', {face_label: FaceColour.WHITE for face_label in FaceLabel}),
        (CARTEBLANCHE_PUZZLE_SPEC[0], CARTEBLANCHE_1),
        (CARTEBLANCHE_PUZZLE_SPEC[1], CARTEBLANCHE_2),
        (CARTEBLANCHE_PUZZLE_SPEC[2], CARTEBLANCHE_3),
        (CARTEBLANCHE_PUZZLE_SPEC[3], CARTEBLANCHE_4),
        (WINNING_MOVES_PUZZLE_SPEC[0], WINNING_MOVES_1),
        (WINNING_MOVES_PUZZLE_SPEC[1], WINNING_MOVES_2),
        (WINNING_MOVES_PUZZLE_SPEC[2], WINNING_MOVES_3),
        (WINNING_MOVES_PUZZLE_SPEC[3], WINNING_MOVES_4)
    ]
)
def test_puzzle_cube(cube_spec, expected_faces):
    puzzle_cube: PuzzleCube = PuzzleCube(cube_spec)
    assert puzzle_cube.face_label_to_colour == expected_faces

@pytest.mark.parametrize(
    "puzzle_spec, expected_cubes",
    [
        (CARTEBLANCHE_PUZZLE_SPEC, [CARTEBLANCHE_1, CARTEBLANCHE_2, CARTEBLANCHE_3, CARTEBLANCHE_4]),
        (WINNING_MOVES_PUZZLE_SPEC, [WINNING_MOVES_1, WINNING_MOVES_2, WINNING_MOVES_3, WINNING_MOVES_4])
    ]
)
def test_puzzle(puzzle_spec, expected_cubes):
    puzzle: Puzzle = Puzzle(puzzle_spec)
    for (i, cube_number) in enumerate(PuzzleCubeNumber):
        assert puzzle.number_to_cube[cube_number].face_label_to_colour == expected_cubes[i]
