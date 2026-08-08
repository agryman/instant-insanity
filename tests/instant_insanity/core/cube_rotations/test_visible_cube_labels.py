import pytest
from manim import BLACK, Text

from instant_insanity.core.cube import FacePlane
from instant_insanity.core.cube_rotations import (
    INITIAL_PLANE_TO_LABEL_MAPPING,
    VisibleCubeTexts,
    make_visible_cube_labels,
    make_visible_cube_texts_from_mapping,
)
from instant_insanity.core.puzzle import FaceLabel

VISIBLE_PLANES: list[FacePlane] = [FacePlane.FRONT, FacePlane.RIGHT, FacePlane.TOP]
INVALID_PLANES: list[FacePlane] = [FacePlane.BACK, FacePlane.LEFT, FacePlane.BOTTOM]


def make_labels() -> VisibleCubeTexts:
    return VisibleCubeTexts(front=Text("front"), right=Text("right"), top=Text("top"))


@pytest.mark.parametrize("plane", VISIBLE_PLANES, ids=lambda p: p.name)
def test_set_then_get_returns_set_object(plane: FacePlane) -> None:
    labels: VisibleCubeTexts = make_labels()
    new_label: Text = Text("new")
    labels.set_label(plane, new_label)
    assert labels.get_label(plane) is new_label


@pytest.mark.parametrize("plane", INVALID_PLANES, ids=lambda p: p.name)
def test_get_label_rejects_invalid_plane(plane: FacePlane) -> None:
    labels: VisibleCubeTexts = make_labels()
    with pytest.raises(ValueError):
        labels.get_label(plane)


@pytest.mark.parametrize("plane", INVALID_PLANES, ids=lambda p: p.name)
def test_set_label_rejects_invalid_plane(plane: FacePlane) -> None:
    labels: VisibleCubeTexts = make_labels()
    with pytest.raises(ValueError):
        labels.set_label(plane, Text("new"))


def test_make_visible_cube_labels_sets_text() -> None:
    labels: VisibleCubeTexts = make_visible_cube_labels("F", "R", "T")
    assert labels.front.text == "F"
    assert labels.right.text == "R"
    assert labels.top.text == "T"


@pytest.mark.parametrize("plane", VISIBLE_PLANES, ids=lambda p: p.name)
def test_make_visible_cube_labels_applies_styling(plane: FacePlane) -> None:
    labels: VisibleCubeTexts = make_visible_cube_labels("F", "R", "T")
    label: Text = labels.get_label(plane)
    reference: Text = Text(label.text, font="sans-serif", color=BLACK, font_size=24)
    assert label.font == reference.font
    assert label.font_size == reference.font_size
    assert label.color.to_hex() == BLACK.to_hex()


@pytest.mark.parametrize("plane", VISIBLE_PLANES, ids=lambda p: p.name)
def test_make_visible_cube_labels_from_mapping_uses_face_label_value(plane: FacePlane) -> None:
    labels: VisibleCubeTexts = make_visible_cube_texts_from_mapping(
        INITIAL_PLANE_TO_LABEL_MAPPING
    )
    expected: FaceLabel = INITIAL_PLANE_TO_LABEL_MAPPING[plane]
    assert labels.get_label(plane).text == expected.value


@pytest.mark.parametrize("plane", VISIBLE_PLANES, ids=lambda p: p.name)
def test_make_visible_cube_labels_from_mapping_applies_styling(plane: FacePlane) -> None:
    labels: VisibleCubeTexts = make_visible_cube_texts_from_mapping(
        INITIAL_PLANE_TO_LABEL_MAPPING
    )
    label: Text = labels.get_label(plane)
    reference: Text = Text(label.text, font="sans-serif", color=BLACK, font_size=24)
    assert label.font == reference.font
    assert label.font_size == reference.font_size
    assert label.color.to_hex() == BLACK.to_hex()
