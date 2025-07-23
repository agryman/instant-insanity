"""
This module contains functions for the geometry of convex polygons in 2 and 3 dimensions.
"""

import numpy as np
from manim.typing import Vector3D

Triangle = list[Vector3D]

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