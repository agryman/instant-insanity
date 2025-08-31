import pytest
from instant_insanity.core.cube import FacePlane
from instant_insanity.core.puzzle import FaceLabel, INITIAL_FACE_LABEL_TO_NAME


@pytest.mark.parametrize(
    "face, expected_label",
    [
        (FaceLabel.X, FacePlane.FRONT),
        (FaceLabel.Y, FacePlane.RIGHT),
        (FaceLabel.Z, FacePlane.TOP),
        (FaceLabel.Z_PRIME, FacePlane.BOTTOM),
        (FaceLabel.Y_PRIME, FacePlane.LEFT),
        (FaceLabel.X_PRIME, FacePlane.BACK),
    ]
)
def test_face_label_to_name(face, expected_label):
    assert INITIAL_FACE_LABEL_TO_NAME[face] is expected_label
