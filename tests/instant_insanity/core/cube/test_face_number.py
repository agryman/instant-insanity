import pytest
from instant_insanity.core.cube import FacePlane, FaceNumber, INITIAL_FACE_NUMBER_TO_PLANE


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
        (FaceNumber.THREE, FacePlane.FRONT),
        (FaceNumber.ONE, FacePlane.RIGHT),
        (FaceNumber.TWO, FacePlane.TOP),
        (FaceNumber.FIVE, FacePlane.BOTTOM),
        (FaceNumber.SIX, FacePlane.LEFT),
        (FaceNumber.FOUR, FacePlane.BACK),
    ]
)
def test_face_number_to_name(face, expected_name):
    assert INITIAL_FACE_NUMBER_TO_PLANE[face] is expected_name
