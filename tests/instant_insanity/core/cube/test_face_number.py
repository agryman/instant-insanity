import pytest
from instant_insanity.core.cube import FaceName, FaceNumber, FACE_NUMBER_TO_NAME


@pytest.mark.parametrize(
    "face, expected_opposite",
    [
        (FaceNumber.FRONT, FaceNumber.BACK),
        (FaceNumber.RIGHT, FaceNumber.LEFT),
        (FaceNumber.TOP, FaceNumber.BOTTOM),
        (FaceNumber.BOTTOM, FaceNumber.TOP),
        (FaceNumber.LEFT, FaceNumber.RIGHT),
        (FaceNumber.BACK, FaceNumber.FRONT),
    ]
)
def test_opposite_faces(face, expected_opposite):
    assert face.opposite() is expected_opposite

@pytest.mark.parametrize(
    "face, expected_label",
    [
        (FaceNumber.FRONT, FaceName.FRONT),
        (FaceNumber.RIGHT, FaceName.RIGHT),
        (FaceNumber.TOP, FaceName.TOP),
        (FaceNumber.BOTTOM, FaceName.BOTTOM),
        (FaceNumber.LEFT, FaceName.LEFT),
        (FaceNumber.BACK, FaceName.BACK),
    ]
)
def test_face_number_to_name(face, expected_label):
    assert FACE_NUMBER_TO_NAME[face] is expected_label
