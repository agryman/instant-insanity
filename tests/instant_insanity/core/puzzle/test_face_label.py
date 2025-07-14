import pytest
from instant_insanity.core.cube import FaceName
from instant_insanity.core.puzzle import FaceLabel, FACE_LABEL_TO_NAME


@pytest.mark.parametrize(
    "face, expected_label",
    [
        (FaceLabel.FRONT, FaceName.FRONT),
        (FaceLabel.RIGHT, FaceName.RIGHT),
        (FaceLabel.TOP, FaceName.TOP),
        (FaceLabel.BOTTOM, FaceName.BOTTOM),
        (FaceLabel.LEFT, FaceName.LEFT),
        (FaceLabel.BACK, FaceName.BACK),
    ]
)
def test_face_label_to_name(face, expected_label):
    assert FACE_LABEL_TO_NAME[face] is expected_label
