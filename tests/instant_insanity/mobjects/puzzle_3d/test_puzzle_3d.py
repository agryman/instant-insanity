import pytest

from instant_insanity.core.cube import FacePlane
from instant_insanity.core.geometry_types import PolygonId
from instant_insanity.core.puzzle import PuzzleCubeNumber, FaceLabel
from instant_insanity.mobjects.puzzle_3d import Puzzle3D

# Valid test cases
valid_cases = [
    ("1/y", (1, "y")),
    ("2/y'", (2, "y'")),
    ("3/z", (3, "z")),
    ("4/z'", (4, "z'")),
    ("1/x", (1, "x")),
    ("4/x'", (4, "x'")),
]

@pytest.mark.parametrize('text, expected_tuple', valid_cases)
def test_id_to_name_valid(text: str, expected_tuple: tuple[int, str]) -> None:
    """Test id_to_name parses valid strings into correct tuples."""
    result = Puzzle3D.id_to_name(PolygonId(text))
    assert result == (PuzzleCubeNumber(expected_tuple[0]), FaceLabel(expected_tuple[1]))

@pytest.mark.parametrize('tuple_value, expected_text', [(t, s) for s, t in valid_cases])
def test_name_to_id_valid(tuple_value: tuple[int, str], expected_text: str) -> None:
    """Test name_to_id formats valid tuples into correct strings."""
    name = (PuzzleCubeNumber(tuple_value[0]), FaceLabel(tuple_value[1]))
    result = Puzzle3D.name_to_id(name)
    assert result == expected_text

@pytest.mark.parametrize('tuple_value', [t for _, t in valid_cases])
def test_round_trip(tuple_value: tuple[int, str]) -> None:
    """Test round-trip conversion: tuple -> string -> tuple."""
    name = (PuzzleCubeNumber(tuple_value[0]), FaceLabel(tuple_value[1]))
    text = Puzzle3D.name_to_id(name)
    parsed = Puzzle3D.id_to_name(text)
    assert parsed == tuple_value

# Invalid test cases for id_to_name (invalid string format or values)
invalid_strings = [
    "0/y",  # number out of range
    "5/z",  # number out of range
    "3/w",  # invalid word
    "x/z",  # non-digit number
    "2",    # missing "/"
    "2-z",  # wrong delimiter
]

@pytest.mark.parametrize('text', invalid_strings)
def test_id_to_name_invalid(text: str) -> None:
    """Test id_to_name raises ValueError on invalid strings."""
    with pytest.raises(ValueError):
        Puzzle3D.id_to_name(PolygonId(text))

# Invalid test cases for name_to_id (invalid tuple values)
invalid_tuples = [
    (0, "z"),       # number out of range
    (5, "y'"),      # number out of range
    (3, "w"),       # invalid word
    ("3", "z"),     # number not int
    (3, 7),         # word not str
]

@pytest.mark.parametrize('tuple_value', invalid_tuples)
def test_name_to_id_invalid(tuple_value: tuple) -> None:
    """Test name_to_id raises ValueError on invalid tuples."""
    with pytest.raises(ValueError):
        name = (PuzzleCubeNumber(tuple_value[0]), FaceLabel(tuple_value[1]))
        Puzzle3D.name_to_id(name)