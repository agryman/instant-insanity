"""
This module contains functions for the geometry of convex polygons in 2 and 3 dimensions.
"""

import numpy as np
from manim.typing import Point3D, Vector3D, Point3D_Array

type Triangle = list[Point3D]

def check_triangle(triangle: Triangle) -> None:
    """Check that the triangle contains 3 vertices."""
    size: int = len(triangle)
    if size != 3:
        raise ValueError(f"Invalid triangle. Expected size=3. Actual size={size}.")

def triangle_area(triangle: Triangle) -> float:
    """Return the area of the triangle."""
    check_triangle(triangle)

    return 0.0

def overlap(triangle1, triangle2) -> int:
    """
    Given two triangles in 3-space, consider their 2-d projections onto the plane
    z = 0.

    Return 0 if the triangles do not overlap or either projection has zero area.
    Return 1 if they overlap and triangle 1 is in front of triangle 2.
    Return -1 if the overlap and triangle 2 is in front of triangle 1.
    """

    return 0

def get_translation(v1: Point3D_Array, v2: Point3D_Array) -> Vector3D:
    """Check if v2 is a translation of v1 by some vector t.

    Args:
        v1: A (4, 3) array of floats.
        v2: A (4, 3) array of floats.

    Returns:
        A (3,) translation vector t such that v2 ≈ v1 + t.

    Raises:
        ValueError: If no such translation vector exists.
    """
    if v1.shape != (4, 3) or v2.shape != (4, 3):
        raise ValueError('Both v1 and v2 must have shape (4, 3)')

    # Candidate translation vector: difference of first row
    t: Vector3D = v2[0] - v1[0]

    # Check if all differences match t (within floating point tolerance)
    if np.allclose(v2, v1 + t):
        return t

    raise ValueError('v2 is not a translation of v1')
