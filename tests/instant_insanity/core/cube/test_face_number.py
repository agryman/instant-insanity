import pytest
from instant_insanity.core.cube import FaceName, FaceNumber, INITIAL_FACE_NUMBER_TO_NAME


@pytest.mark.parametrize(
    "face, expected_opposite",
    [
        (FaceNumber.THREE, FaceNumber.FOUR),
        (FaceNumber.ONE, FaceNumber.SIX),
        (FaceNumber.TWO, FaceNumber.FIVE),
        (FaceNumber.FIVE, FaceNumber.TWO),
        (FaceNumber.SIX, FaceNumber.ONE),
        (FaceNumber.FOUR, FaceNumber.THREE),
    ]
)
def test_opposite_faces(face, expected_opposite):
    assert face.opposite() is expected_opposite

@pytest.mark.parametrize(
    "face, expected_name",
    [
        (FaceNumber.THREE, FaceName.FRONT),
        (FaceNumber.ONE, FaceName.RIGHT),
        (FaceNumber.TWO, FaceName.TOP),
        (FaceNumber.FIVE, FaceName.BOTTOM),
        (FaceNumber.SIX, FaceName.LEFT),
        (FaceNumber.FOUR, FaceName.BACK),
    ]
)
def test_face_number_to_name(face, expected_name):
    assert INITIAL_FACE_NUMBER_TO_NAME[face] is expected_name
