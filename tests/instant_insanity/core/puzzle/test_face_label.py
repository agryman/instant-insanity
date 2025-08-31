import pytest
from instant_insanity.core.cube import FaceName
from instant_insanity.core.puzzle import FaceLabel, INITIAL_FACE_LABEL_TO_NAME


@pytest.mark.parametrize(
    "face, expected_label",
    [
        (FaceLabel.X, FaceName.FRONT),
        (FaceLabel.Y, FaceName.RIGHT),
        (FaceLabel.Z, FaceName.TOP),
        (FaceLabel.Z_PRIME, FaceName.BOTTOM),
        (FaceLabel.Y_PRIME, FaceName.LEFT),
        (FaceLabel.X_PRIME, FaceName.BACK),
    ]
)
def test_face_label_to_name(face, expected_label):
    assert INITIAL_FACE_LABEL_TO_NAME[face] is expected_label
