import pytest
from instant_insanity.core.cube import FaceName
from instant_insanity.core.puzzle import (FaceColour, PuzzleCube, PuzzleCubeNumber, Puzzle,
                                          TANTALIZER_PUZZLE, WINNING_MOVES_PUZZLE)

TANTALIZER_1 = { # ROWOGG
    FaceName.FRONT: FaceColour.RED,
    FaceName.BACK: FaceColour.ORANGE,
    FaceName.RIGHT: FaceColour.WHITE,
    FaceName.LEFT: FaceColour.ORANGE,
    FaceName.TOP: FaceColour.GREEN,
    FaceName.BOTTOM: FaceColour.GREEN
}

TANTALIZER_2 = { # GRORWW
    FaceName.FRONT: FaceColour.GREEN,
    FaceName.BACK: FaceColour.RED,
    FaceName.RIGHT: FaceColour.ORANGE,
    FaceName.LEFT: FaceColour.RED,
    FaceName.TOP: FaceColour.WHITE,
    FaceName.BOTTOM: FaceColour.WHITE
}

TANTALIZER_3 = { # OWGWGR
    FaceName.FRONT: FaceColour.ORANGE,
    FaceName.BACK: FaceColour.WHITE,
    FaceName.RIGHT: FaceColour.GREEN,
    FaceName.LEFT: FaceColour.WHITE,
    FaceName.TOP: FaceColour.GREEN,
    FaceName.BOTTOM: FaceColour.RED
}

TANTALIZER_4 = { # WGRGRW
    FaceName.FRONT: FaceColour.WHITE,
    FaceName.BACK: FaceColour.GREEN,
    FaceName.RIGHT: FaceColour.RED,
    FaceName.LEFT: FaceColour.GREEN,
    FaceName.TOP: FaceColour.RED,
    FaceName.BOTTOM: FaceColour.WHITE
}

WINNING_MOVES_1 = { # GWBRRR
    FaceName.FRONT: FaceColour.GREEN,
    FaceName.BACK: FaceColour.WHITE,
    FaceName.RIGHT: FaceColour.BLUE,
    FaceName.LEFT: FaceColour.RED,
    FaceName.TOP: FaceColour.RED,
    FaceName.BOTTOM: FaceColour.RED
}

WINNING_MOVES_2 = { # RGBBWG
    FaceName.FRONT: FaceColour.RED,
    FaceName.BACK: FaceColour.GREEN,
    FaceName.RIGHT: FaceColour.BLUE,
    FaceName.LEFT: FaceColour.BLUE,
    FaceName.TOP: FaceColour.WHITE,
    FaceName.BOTTOM: FaceColour.GREEN
}

WINNING_MOVES_3 = { # WRWBGR
    FaceName.FRONT: FaceColour.WHITE,
    FaceName.BACK: FaceColour.RED,
    FaceName.RIGHT: FaceColour.WHITE,
    FaceName.LEFT: FaceColour.BLUE,
    FaceName.TOP: FaceColour.GREEN,
    FaceName.BOTTOM: FaceColour.RED
}

WINNING_MOVES_4 = { # BRGWBW
    FaceName.FRONT: FaceColour.BLUE,
    FaceName.BACK: FaceColour.RED,
    FaceName.RIGHT: FaceColour.GREEN,
    FaceName.LEFT: FaceColour.WHITE,
    FaceName.TOP: FaceColour.BLUE,
    FaceName.BOTTOM: FaceColour.WHITE
}

@pytest.mark.parametrize(
    "cube_spec, expected_faces",
    [
        ('wwwwww', {face_name: FaceColour.WHITE for face_name in FaceName}),
        ('WWWWWW', {face_name: FaceColour.WHITE for face_name in FaceName}),
        (TANTALIZER_PUZZLE[0], TANTALIZER_1),
        (TANTALIZER_PUZZLE[1], TANTALIZER_2),
        (TANTALIZER_PUZZLE[2], TANTALIZER_3),
        (TANTALIZER_PUZZLE[3], TANTALIZER_4),
        (WINNING_MOVES_PUZZLE[0], WINNING_MOVES_1),
        (WINNING_MOVES_PUZZLE[1], WINNING_MOVES_2),
        (WINNING_MOVES_PUZZLE[2], WINNING_MOVES_3),
        (WINNING_MOVES_PUZZLE[3], WINNING_MOVES_4)
    ]
)
def test_puzzle_cube(cube_spec, expected_faces):
    puzzle_cube: PuzzleCube = PuzzleCube(cube_spec)
    assert puzzle_cube.faces == expected_faces

@pytest.mark.parametrize(
    "puzzle_spec, expected_cubes",
    [
        (TANTALIZER_PUZZLE, [TANTALIZER_1, TANTALIZER_2, TANTALIZER_3, TANTALIZER_4]),
        (WINNING_MOVES_PUZZLE, [WINNING_MOVES_1, WINNING_MOVES_2, WINNING_MOVES_3, WINNING_MOVES_4])
    ]
)
def test_puzzle(puzzle_spec, expected_cubes):
    puzzle: Puzzle = Puzzle(puzzle_spec)
    for (i, cube_number) in enumerate(PuzzleCubeNumber):
        assert puzzle.cubes[cube_number].faces == expected_cubes[i]
