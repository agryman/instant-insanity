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
import numpy as np
from manim import X_AXIS, Y_AXIS, Z_AXIS
from manim.typing import Point3D, Vector3D

from instant_insanity.core.geometry_types import Point3D_Array


class FacePlane(StrEnum):
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
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6

    def opposite(self) -> 'FaceNumber':
        """Return the opposite face number."""
        return FaceNumber(7 - self.value)

# map face planes to initial face numbers
INITIAL_FACE_PLANE_TO_NUMBER: dict[FacePlane, FaceNumber] = {
    FacePlane.RIGHT: FaceNumber.ONE,
    FacePlane.LEFT: FaceNumber.SIX,
    FacePlane.TOP: FaceNumber.TWO,
    FacePlane.BOTTOM: FaceNumber.FIVE,
    FacePlane.FRONT: FaceNumber.THREE,
    FacePlane.BACK: FaceNumber.FOUR
}

# map initial face numbers to face planes
INITIAL_FACE_NUMBER_TO_PLANE: dict[FaceNumber, FacePlane] = {
    FaceNumber.ONE: FacePlane.RIGHT,
    FaceNumber.SIX: FacePlane.LEFT,
    FaceNumber.TWO: FacePlane.TOP,
    FaceNumber.FIVE: FacePlane.BOTTOM,
    FaceNumber.THREE: FacePlane.FRONT,
    FaceNumber.FOUR: FacePlane.BACK
}

def mk_point(point: list[float]) -> Point3D:
    return np.array(point, dtype=np.float64)

# 3D coordinates of standard cube vertices
RTF: Point3D = mk_point([1.0, 1.0, 1.0])
RTB: Point3D = mk_point([1.0, 1.0, -1.0])
RBF: Point3D = mk_point([1.0, -1.0, 1.0])
RBB: Point3D = mk_point([1.0, -1.0, -1.0])
LTF: Point3D = mk_point([-1.0, 1.0, 1.0])
LTB: Point3D = mk_point([-1.0, 1.0, -1.0])
LBF: Point3D = mk_point([-1.0, -1.0, 1.0])
LBB: Point3D = mk_point([-1.0, -1.0, -1.0])

def mk_points(points: list[Point3D]) -> Point3D_Array:
    return np.array(points, dtype=np.float64)

# vertex paths of standard cube faces
FACE_PLANE_TO_VERTEX_PATH: dict[FacePlane, Point3D_Array] = {
    FacePlane.RIGHT: mk_points([RTF, RTB, RBB, RBF]),
    FacePlane.LEFT: mk_points([LTF, LTB, LBB, LBF]),
    FacePlane.TOP: mk_points([RTF, RTB, LTB, LTF]),
    FacePlane.BOTTOM: mk_points([RBF, RBB, LBB, LBF]),
    FacePlane.FRONT: mk_points([RTF, LTF, LBF, RBF]),
    FacePlane.BACK: mk_points([RTB, LTB, LBB, RBB])
}

# outward-pointing unit normals of standard cube faces
FACE_PLANE_TO_UNIT_NORMAL: dict[FacePlane, Vector3D] = {
    FacePlane.RIGHT: X_AXIS,
    FacePlane.LEFT: -1.0 * X_AXIS,
    FacePlane.TOP: Y_AXIS,
    FacePlane.BOTTOM: -1.0 * Y_AXIS,
    FacePlane.FRONT: Z_AXIS,
    FacePlane.BACK: -1.0 * Z_AXIS,
}
