import pytest
from instant_insanity.cube import FaceNumber, FaceLabel, FACE_NUMBER_TO_LABEL


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
        (FaceNumber.FRONT, FaceLabel.FRONT),
        (FaceNumber.RIGHT, FaceLabel.RIGHT),
        (FaceNumber.TOP, FaceLabel.TOP),
        (FaceNumber.BOTTOM, FaceLabel.BOTTOM),
        (FaceNumber.LEFT, FaceLabel.LEFT),
        (FaceNumber.BACK, FaceLabel.BACK),
    ]
)
def test_face_number_to_label(face, expected_label):
    assert FACE_NUMBER_TO_LABEL[face] is expected_label
