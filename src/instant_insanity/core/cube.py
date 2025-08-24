"""
This module describes the geometry of cubes.

Imagine euclidean 3-space as intersecting the 2-space associated with a computer screen.
The standard orientation of the 3-space coordinate axes is as follows:
* the x-axis is oriented horizontally and increases from left to right
* the y-axis is oriented vertically and increases from bottom to top, aka from down to up
* the z-axis is oriented perpendicularly to the screen and increases from back to front, aka from in to out
These axes define the standard coordinate system.
In terms of (x,y,z) coordinates, the screen is contained in the plane z=0.
The centre of the screen is the origin of 3-space.

The standard cube is the set of points in euclidean 3-space consisting
of the cartesian product of three closed unit intervals [-1, 1].
It has 8 vertices, 12 edges, and 6 faces.

This module defines names and coordinates for the vertices, edges, and faces
of the standard cube using the standard coordinate system.
"""

from enum import IntEnum, StrEnum
from typing import Self
import numpy as np

from instant_insanity.core.geometry_types import VertexPath


class FaceName(StrEnum):
    """
    This enum assigns names to the faces of a cube.
    * The right face is in the plane x = 1.
    * The left face is in the plane x = -1.
    * The top face is in the plane y = 1.
    * The bottom face is in the plane y = -1.
    * The front face is in the plane z = 1.
    * The bottom face is in the plane z = -1.
    """
    RIGHT = 'right'
    LEFT = 'left'
    TOP = 'top'
    BOTTOM = 'bottom'
    FRONT = 'front'
    BACK = 'back'


class FaceNumber(IntEnum):
    """Numbers that appear on the faces of a die."""
    RIGHT = 1
    TOP = 2
    FRONT = 3
    BACK = 4
    BOTTOM = 5
    LEFT = 6

    def opposite(self) -> 'FaceNumber':
        """Return the opposite face number."""
        return FaceNumber(7 - self.value)

# map face names to face numbers
FACE_NAME_TO_NUMBER: dict[FaceName, FaceNumber] = {
    FaceName.RIGHT: FaceNumber.RIGHT,
    FaceName.LEFT: FaceNumber.LEFT,
    FaceName.TOP: FaceNumber.TOP,
    FaceName.BOTTOM: FaceNumber.BOTTOM,
    FaceName.FRONT: FaceNumber.FRONT,
    FaceName.BACK: FaceNumber.BACK
}

# map face numbers to face names
FACE_NUMBER_TO_NAME: dict[FaceNumber, FaceName] = {
    FaceNumber.RIGHT: FaceName.RIGHT,
    FaceNumber.LEFT: FaceName.LEFT,
    FaceNumber.TOP: FaceName.TOP,
    FaceNumber.BOTTOM: FaceName.BOTTOM,
    FaceNumber.FRONT: FaceName.FRONT,
    FaceNumber.BACK: FaceName.BACK
}

def mk_point(point: list[float]) -> np.ndarray:
    return np.array(point, dtype=np.float64)

# 3D coordinates of standard cube vertices
RTF: np.ndarray = mk_point([1.0, 1.0, 1.0])
RTB: np.ndarray = mk_point([1.0, 1.0, -1.0])
RBF: np.ndarray = mk_point([1.0, -1.0, 1.0])
RBB: np.ndarray = mk_point([1.0, -1.0, -1.0])
LTF: np.ndarray = mk_point([-1.0, 1.0, 1.0])
LTB: np.ndarray = mk_point([-1.0, 1.0, -1.0])
LBF: np.ndarray = mk_point([-1.0, -1.0, 1.0])
LBB: np.ndarray = mk_point([-1.0, -1.0, -1.0])

def mk_points(points: list[np.ndarray]) -> np.ndarray:
    return np.array(points, dtype=np.float64)

# vertex paths of standard cube faces
FACE_NAME_TO_VERTEX_PATH: dict[FaceName, VertexPath] = {
    FaceName.RIGHT: mk_points([RTF, RTB, RBB, RBF]),
    FaceName.LEFT: mk_points([LTF, LTB, LBB, LBF]),
    FaceName.TOP: mk_points([RTF, RTB, LTB, LTF]),
    FaceName.BOTTOM: mk_points([RBF, RBB, LBB, LBF]),
    FaceName.FRONT: mk_points([RTF, LTF, LBF, RBF]),
    FaceName.BACK: mk_points([RTB, LTB, LBB, RBB])
}

# outward-pointing unit normals of standard cube faces
FACE_NAME_TO_UNIT_NORMAL: dict[FaceName, np.ndarray] = {
    FaceName.RIGHT: mk_point([1.0, 0.0, 0.0]),
    FaceName.LEFT: mk_point([-1.0, 0.0, 0.0]),
    FaceName.TOP: mk_point([0.0, 1.0, 0.0]),
    FaceName.BOTTOM: mk_point([0.0, -1.0, 0.0]),
    FaceName.FRONT: mk_point([0.0, 0.0, 1.0]),
    FaceName.BACK: mk_point([0.0, 0.0, -1.0])
}
