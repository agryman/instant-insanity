"""
This module implements cube rotations.
Given any initial cube orientation and any final cube orientation,
we define a canonical rotation matrix that maps the initial orientation to the final orientation.
"""

from dataclasses import dataclass
from scipy.spatial.transform import Rotation

from instant_insanity.core.cube import FacePlane
from instant_insanity.core.puzzle import FaceLabel

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