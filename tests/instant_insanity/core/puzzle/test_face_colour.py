import pytest
from instant_insanity.core.puzzle import FaceColour

@pytest.mark.parametrize("char, expected", [
    ('b', FaceColour.BLUE),
    ('G', FaceColour.GREEN),
    ('o', FaceColour.ORANGE),
    ('P', FaceColour.PURPLE),
    ('r', FaceColour.RED),
    ('w', FaceColour.WHITE),
    ('Y', FaceColour.YELLOW),
])
def test_from_initial_valid(char, expected):
    assert FaceColour.from_initial(char) == expected

@pytest.mark.parametrize("invalid_input", [
    '',       # empty string
    'gr',     # multiple characters
    '1',      # digit
    '!',      # punctuation
    'z',      # no matching colour
])
def test_from_initial_invalid(invalid_input):
    with pytest.raises(ValueError):
        FaceColour.from_initial(invalid_input)
