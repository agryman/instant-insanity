"""
Tests for the get_cube_width and get_cube_gap methods of the Puzzle3D class.
"""
import numpy as np

from instant_insanity.core.projection import PerspectiveProjection
from instant_insanity.core.puzzle import CARTEBLANCHE_PUZZLE_SPEC, PuzzleSpec
from instant_insanity.mobjects.puzzle_3d import (
    DEFAULT_CUBE_SIDE_LENGTH,
    Puzzle3D,
    mk_standard_puzzle3d,
)


def mk_puzzle3d() -> Puzzle3D:
    """Builds a standard Puzzle3D for use in the tests."""
    viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
    projection: PerspectiveProjection = PerspectiveProjection(viewpoint, camera_z=2.0)
    puzzle_spec: PuzzleSpec = CARTEBLANCHE_PUZZLE_SPEC
    return mk_standard_puzzle3d(puzzle_spec, projection)


def test_get_cube_width() -> None:
    # the standard cube occupies [-1, 1]^3, so its width equals the side length.
    puzzle3d: Puzzle3D = mk_puzzle3d()
    width: float = puzzle3d.get_cube_width()
    assert np.isclose(width, DEFAULT_CUBE_SIDE_LENGTH)


def test_get_cube_width_is_positive() -> None:
    puzzle3d: Puzzle3D = mk_puzzle3d()
    width: float = puzzle3d.get_cube_width()
    assert width > 0.0


def test_get_cube_gap() -> None:
    # mk_standard_puzzle3d separates cube centres by (side_length + buff),
    # so the gap between adjacent cubes equals buff.
    puzzle3d: Puzzle3D = mk_puzzle3d()
    expected_buff: float = DEFAULT_CUBE_SIDE_LENGTH * 2.0 * (np.sqrt(2.0) - 1.0)
    gap: float = puzzle3d.get_cube_gap()
    assert np.isclose(gap, expected_buff)


def test_get_cube_gap_is_positive() -> None:
    # the gap must be positive so that adjacent cubes do not collide.
    puzzle3d: Puzzle3D = mk_puzzle3d()
    gap: float = puzzle3d.get_cube_gap()
    assert gap > 0.0


def test_gap_matches_centre_spacing() -> None:
    # centre spacing equals one cube width plus the gap.
    puzzle3d: Puzzle3D = mk_puzzle3d()
    width: float = puzzle3d.get_cube_width()
    gap: float = puzzle3d.get_cube_gap()
    centre_spacing: float = float(puzzle3d.cube_delta[0])
    assert np.isclose(width + gap, centre_spacing)