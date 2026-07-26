"""
This module implements cube rotations.
Given any initial cube orientation and any final cube orientation,
we define a canonical rotation matrix that maps the initial orientation to the final orientation.
"""

from dataclasses import dataclass

import numpy as np
from manim import LEFT, RIGHT, UP, DOWN, IN, OUT, BLACK, Text
from manim.typing import Vector3D
from scipy.spatial.transform import Rotation

from instant_insanity.core.cube import FacePlane
from instant_insanity.core.puzzle import FaceLabel

type PlaneToLabelMapping = dict[FacePlane, FaceLabel]

INITIAL_PLANE_TO_LABEL_MAPPING: PlaneToLabelMapping = {
    FacePlane.FRONT: FaceLabel.X,
    FacePlane.BACK: FaceLabel.X_PRIME,
    FacePlane.RIGHT: FaceLabel.Y,
    FacePlane.LEFT: FaceLabel.Y_PRIME,
    FacePlane.TOP: FaceLabel.Z,
    FacePlane.BOTTOM: FaceLabel.Z_PRIME,
}

@dataclass
class VisibleCubeTexts:
    """The three Text labels visible on a cube: front, right, and top faces."""
    front: Text
    right: Text
    top: Text

    def get_label(self, plane: FacePlane) -> Text:
        """
        Returns the label on the given visible face plane.

        Args:
            plane: one of FacePlane.FRONT, FacePlane.RIGHT, or FacePlane.TOP

        Returns:
            the Text label on the given face plane

        Raises:
            ValueError: if the plane is not front, right, or top
        """
        match plane:
            case FacePlane.FRONT:
                return self.front
            case FacePlane.RIGHT:
                return self.right
            case FacePlane.TOP:
                return self.top
            case _:
                raise ValueError(f'Invalid plane: {plane}')

    def set_label(self, plane: FacePlane, label: Text) -> None:
        """
        Sets the label on the given visible face plane.

        Args:
            plane: one of FacePlane.FRONT, FacePlane.RIGHT, or FacePlane.TOP
            label: the Text label to set on the given face plane

        Raises:
            ValueError: if the plane is not front, right, or top
        """
        match plane:
            case FacePlane.FRONT:
                self.front = label
            case FacePlane.RIGHT:
                self.right = label
            case FacePlane.TOP:
                self.top = label
            case _:
                raise ValueError(f'Invalid plane: {plane}')

def mk_label_from_str(text: str) -> Text:
    """
    Creates a Text label with the standard cube label styling.

    Args:
        text: the text for the label

    Returns:
        a Text label with the standard cube label styling
    """
    return Text(text, font='sans-serif', color=BLACK, font_size=24)

def make_visible_cube_labels(front: str, right: str, top: str) -> VisibleCubeTexts:
    """
    Creates a VisibleCubeLabels object from the given label strings.

    Args:
        front: the text for the front face label
        right: the text for the right face label
        top: the text for the top face label

    Returns:
        a VisibleCubeLabels object with a Text label for each of the front, right, and top faces
    """
    return VisibleCubeTexts(
        front=mk_label_from_str(front),
        right=mk_label_from_str(right),
        top=mk_label_from_str(top),
    )

def make_visible_cube_texts_from_mapping(mapping: PlaneToLabelMapping) -> VisibleCubeTexts:
    """
    Creates a VisibleCubeTexts object from a plane to label mapping.

    The label string for each visible face is the value of its FaceLabel.

    Args:
        mapping: the face plane to label mapping

    Returns:
        a VisibleCubeLabels object with a Text label for each of the front, right, and top faces
    """
    return make_visible_cube_labels(
        front=mapping[FacePlane.FRONT].value,
        right=mapping[FacePlane.RIGHT].value,
        top=mapping[FacePlane.TOP].value,
    )

def rotate_down(before_mapping: PlaneToLabelMapping) -> PlaneToLabelMapping:
    """
    The function applies a 90-degree counter-clockwise rotation around the DOWN axis
    to the before cube labelling to produce the after cube labelling.

    Args:
        before_mapping: the face plane to label mapping before the rotation

    Returns:
        the face plane to label mapping after the rotation

    """
    after_mapping: PlaneToLabelMapping = dict()
    after_mapping[FacePlane.FRONT] = before_mapping[FacePlane.RIGHT]
    after_mapping[FacePlane.BACK] = before_mapping[FacePlane.LEFT]
    after_mapping[FacePlane.RIGHT] = before_mapping[FacePlane.BACK]
    after_mapping[FacePlane.LEFT] = before_mapping[FacePlane.FRONT]
    after_mapping[FacePlane.TOP] = before_mapping[FacePlane.TOP]
    after_mapping[FacePlane.BOTTOM] = before_mapping[FacePlane.BOTTOM]

    return after_mapping

def rotate_right(before_mapping: PlaneToLabelMapping) -> PlaneToLabelMapping:
    """
    The function applies a 90-degree counter-clockwise rotation around the RIGHT axis
    to the before cube labelling to produce the after cube labelling.

    Args:
        before_mapping: the face plane to label mapping before the rotation

    Returns:
        the face plane to label mapping after the rotation

    """
    after_mapping: PlaneToLabelMapping = dict()
    after_mapping[FacePlane.FRONT] = before_mapping[FacePlane.TOP]
    after_mapping[FacePlane.BACK] = before_mapping[FacePlane.BOTTOM]
    after_mapping[FacePlane.RIGHT] = before_mapping[FacePlane.RIGHT]
    after_mapping[FacePlane.LEFT] = before_mapping[FacePlane.LEFT]
    after_mapping[FacePlane.TOP] = before_mapping[FacePlane.BACK]
    after_mapping[FacePlane.BOTTOM] = before_mapping[FacePlane.FRONT]

    return after_mapping

def rotate_up(before_mapping: PlaneToLabelMapping) -> PlaneToLabelMapping:
    """
    The function applies a 90-degree counter-clockwise rotation around the UP axis
    to the before cube labelling to produce the after cube labelling.
    This is the inverse of rotate_down.

    Args:
        before_mapping: the face plane to label mapping before the rotation

    Returns:
        the face plane to label mapping after the rotation

    """
    after_mapping: PlaneToLabelMapping = dict()
    after_mapping[FacePlane.FRONT] = before_mapping[FacePlane.LEFT]
    after_mapping[FacePlane.BACK] = before_mapping[FacePlane.RIGHT]
    after_mapping[FacePlane.RIGHT] = before_mapping[FacePlane.FRONT]
    after_mapping[FacePlane.LEFT] = before_mapping[FacePlane.BACK]
    after_mapping[FacePlane.TOP] = before_mapping[FacePlane.TOP]
    after_mapping[FacePlane.BOTTOM] = before_mapping[FacePlane.BOTTOM]

    return after_mapping

def rotate_left(before_mapping: PlaneToLabelMapping) -> PlaneToLabelMapping:
    """
    The function applies a 90-degree counter-clockwise rotation around the LEFT axis
    to the before cube labelling to produce the after cube labelling.
    This is the inverse of rotate_right.

    Args:
        before_mapping: the face plane to label mapping before the rotation

    Returns:
        the face plane to label mapping after the rotation

    """
    after_mapping: PlaneToLabelMapping = dict()
    after_mapping[FacePlane.FRONT] = before_mapping[FacePlane.BOTTOM]
    after_mapping[FacePlane.BACK] = before_mapping[FacePlane.TOP]
    after_mapping[FacePlane.RIGHT] = before_mapping[FacePlane.RIGHT]
    after_mapping[FacePlane.LEFT] = before_mapping[FacePlane.LEFT]
    after_mapping[FacePlane.TOP] = before_mapping[FacePlane.FRONT]
    after_mapping[FacePlane.BOTTOM] = before_mapping[FacePlane.BACK]

    return after_mapping

def rotate_front(before_mapping: PlaneToLabelMapping) -> PlaneToLabelMapping:
    """
    The function applies a 90-degree counter-clockwise rotation around the FRONT axis
    to the before cube labelling to produce the after cube labelling.

    Args:
        before_mapping: the face plane to label mapping before the rotation

    Returns:
        the face plane to label mapping after the rotation

    """
    after_mapping: PlaneToLabelMapping = dict()
    after_mapping[FacePlane.FRONT] = before_mapping[FacePlane.FRONT]
    after_mapping[FacePlane.BACK] = before_mapping[FacePlane.BACK]
    after_mapping[FacePlane.RIGHT] = before_mapping[FacePlane.BOTTOM]
    after_mapping[FacePlane.LEFT] = before_mapping[FacePlane.TOP]
    after_mapping[FacePlane.TOP] = before_mapping[FacePlane.RIGHT]
    after_mapping[FacePlane.BOTTOM] = before_mapping[FacePlane.LEFT]

    return after_mapping

def rotate_back(before_mapping: PlaneToLabelMapping) -> PlaneToLabelMapping:
    """
    The function applies a 90-degree counter-clockwise rotation around the BACK axis
    to the before cube labelling to produce the after cube labelling.
    This is the inverse of rotate_front.

    Args:
        before_mapping: the face plane to label mapping before the rotation

    Returns:
        the face plane to label mapping after the rotation

    """
    after_mapping: PlaneToLabelMapping = dict()
    after_mapping[FacePlane.FRONT] = before_mapping[FacePlane.FRONT]
    after_mapping[FacePlane.BACK] = before_mapping[FacePlane.BACK]
    after_mapping[FacePlane.RIGHT] = before_mapping[FacePlane.TOP]
    after_mapping[FacePlane.LEFT] = before_mapping[FacePlane.BOTTOM]
    after_mapping[FacePlane.TOP] = before_mapping[FacePlane.LEFT]
    after_mapping[FacePlane.BOTTOM] = before_mapping[FacePlane.RIGHT]

    return after_mapping

def rotate_by_vector(vector: Vector3D, before_mapping: PlaneToLabelMapping) -> PlaneToLabelMapping:
    """
    The function applies a 90-degree counter-clockwise rotation around the axis
    given by the vector to the before cube labelling to produce the after cube labelling.

    The vector must be one of the Manim direction constants LEFT, RIGHT, UP, DOWN, IN, OUT.

    Args:
        vector: the axis of rotation, a Manim direction constant
        before_mapping: the face plane to label mapping before the rotation

    Returns:
        the face plane to label mapping after the rotation

    Raises:
        ValueError: if the vector is not one of the allowed Manim direction constants
    """
    if np.array_equal(vector, LEFT):
        return rotate_left(before_mapping)
    if np.array_equal(vector, RIGHT):
        return rotate_right(before_mapping)
    if np.array_equal(vector, UP):
        return rotate_up(before_mapping)
    if np.array_equal(vector, DOWN):
        return rotate_down(before_mapping)
    if np.array_equal(vector, OUT):
        return rotate_front(before_mapping)
    if np.array_equal(vector, IN):
        return rotate_back(before_mapping)
    raise ValueError(f'Invalid vector: {vector}')


def get_opposite_face_label(face_label: FaceLabel) -> FaceLabel:
    match face_label:
        case FaceLabel.X:
            return FaceLabel.X_PRIME
        case FaceLabel.X_PRIME:
            return FaceLabel.X
        case FaceLabel.Z:
            return FaceLabel.Z_PRIME
        case FaceLabel.Z_PRIME:
            return FaceLabel.Z
        case FaceLabel.Y:
            return FaceLabel.Y_PRIME
        case FaceLabel.Y_PRIME:
            return FaceLabel.Y
    raise ValueError(f"Invalid face_label: {face_label}")

@dataclass
class CubeOrientation:
    """
    The orientation of a cube is defined by the labels that appear on its front and top faces.
    There are 24 possible orientations.
    """
    front: FaceLabel
    top: FaceLabel

    def __post_init__(self):
        if self.front == get_opposite_face_label(self.top):
            raise ValueError(f'Expected adjacent faces but got opposites {self.front} and {self.top}')

    def get_face_plane_to_label_mapping(self) -> dict[FacePlane, FaceLabel]:
        """
        TODO: Should this go the other way, namely map a face name (e.g. x) to its plane (e.g. front)
        in the cube orientation?

        Returns:

        """
        mapping: dict[FacePlane, FaceLabel] = {
            FacePlane.FRONT: self.front,
            FacePlane.BACK: get_opposite_face_label(self.front),
            FacePlane.TOP: self.top,
            FacePlane.BOTTOM: get_opposite_face_label(self.top),

        }
        return mapping

CUBE_ORIENTATIONS: list[CubeOrientation] = [
    CubeOrientation(front, top)
    for front in FaceLabel
    for top in FaceLabel
    if front != get_opposite_face_label(top)
]

def rotate_to_match_front(current_orientation: CubeOrientation, target_front: FaceLabel) -> Rotation:
    """
    Returns a rotation transformation that rotates cube in its current orientation
    so that its front face matches the target front face.

    Args:
        current_orientation: The initial orientation of the cube.
        target_front: the target front face

    Returns:
        a rotation that sends the given target front face to the front of the cube.
    """
    initial_front: FaceLabel = current_orientation.front
    initial_top: FaceLabel = current_orientation.top
    if initial_front == target_front:
        return Rotation.identity()
    return Rotation.identity()