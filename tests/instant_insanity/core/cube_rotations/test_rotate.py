from collections.abc import Callable

import numpy as np
import pytest
from manim import LEFT, RIGHT, UP, DOWN, IN, OUT
from manim.typing import Vector3D

from instant_insanity.core.cube_rotations import (
    INITIAL_PLANE_TO_LABEL_MAPPING,
    PlaneToLabelMapping,
    rotate_back,
    rotate_by_vector,
    rotate_down,
    rotate_front,
    rotate_left,
    rotate_right,
    rotate_up,
)

Rotation = Callable[[PlaneToLabelMapping], PlaneToLabelMapping]

ALL_ROTATIONS: list[Rotation] = [
    rotate_up,
    rotate_down,
    rotate_left,
    rotate_right,
    rotate_front,
    rotate_back,
]

# Each pair is (rotation, its inverse); composing them yields the identity.
INVERSE_PAIRS: list[tuple[Rotation, Rotation]] = [
    (rotate_up, rotate_down),
    (rotate_left, rotate_right),
    (rotate_front, rotate_back),
]

# Each Manim direction constant dispatches to the corresponding rotation.
VECTOR_ROTATIONS: list[tuple[str, Vector3D, Rotation]] = [
    ("LEFT", LEFT, rotate_left),
    ("RIGHT", RIGHT, rotate_right),
    ("UP", UP, rotate_up),
    ("DOWN", DOWN, rotate_down),
    ("OUT", OUT, rotate_front),
    ("IN", IN, rotate_back),
]


@pytest.mark.parametrize("rotate", ALL_ROTATIONS, ids=lambda f: f.__name__)
def test_rotate_four_times_is_identity(rotate: Rotation) -> None:
    mapping: PlaneToLabelMapping = INITIAL_PLANE_TO_LABEL_MAPPING
    for _ in range(4):
        mapping = rotate(mapping)
    assert mapping == INITIAL_PLANE_TO_LABEL_MAPPING


@pytest.mark.parametrize(
    "rotate, inverse", INVERSE_PAIRS, ids=lambda f: f.__name__
)
def test_rotate_inverse_pair_is_identity(rotate: Rotation, inverse: Rotation) -> None:
    assert rotate(inverse(INITIAL_PLANE_TO_LABEL_MAPPING)) == INITIAL_PLANE_TO_LABEL_MAPPING
    assert inverse(rotate(INITIAL_PLANE_TO_LABEL_MAPPING)) == INITIAL_PLANE_TO_LABEL_MAPPING


@pytest.mark.parametrize(
    "vector, rotate",
    [(vector, rotate) for _, vector, rotate in VECTOR_ROTATIONS],
    ids=[name for name, _, _ in VECTOR_ROTATIONS],
)
def test_rotate_by_vector_dispatches(vector: Vector3D, rotate: Rotation) -> None:
    assert rotate_by_vector(vector, INITIAL_PLANE_TO_LABEL_MAPPING) == rotate(
        INITIAL_PLANE_TO_LABEL_MAPPING
    )


def test_rotate_by_vector_rejects_invalid_vector() -> None:
    invalid_vector: Vector3D = np.array([1.0, 1.0, 0.0])
    with pytest.raises(ValueError):
        rotate_by_vector(invalid_vector, INITIAL_PLANE_TO_LABEL_MAPPING)