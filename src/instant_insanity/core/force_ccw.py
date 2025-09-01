import numpy as np
from manim import Polygon
from shapely import is_ccw, LinearRing
from shapely.geometry import LinearRing

def force_ccw(poly: Polygon) -> Polygon:
    """Ensure a Manim Polygon has CCW vertex order (modify in place).

    Uses Shapely's orientation test on the polygon's 2D projection (x, y).
    If the order is clockwise, the vertices are reversed and written back
    to the same Polygon using `set_points_as_corners(...)` + `close_path()`.

    Args:
        poly: The Manim Polygon to normalize (modified in place).

    Returns:
        The same Polygon instance, now guaranteed to be CCW.

    Notes:
        - Assumes standard Cartesian coordinates (y up).
        - For convex polygons this test is unambiguous.
    """
    verts3d: np.ndarray = poly.get_vertices()  # shape (N, 3)

    if not is_ccw_vertices(verts3d):
        # Update THIS polygon in place; no new Polygon is created.
        reversed_verts: np.ndarray = verts3d[::-1]
        poly.set_points_as_corners(reversed_verts)
        poly.close_path()

    return poly


def is_ccw_vertices(vertices3d: np.ndarray) -> bool:
    """Return True if the vertex loop is counterclockwise (y-up convention).

    Args:
        vertices3d: Array of shape (N, 3) giving polygon vertices (x, y, z).

    Returns:
        bool: True if CCW; False otherwise.

    Notes:
        Uses Shapely's orientation on the (x, y) projection. Return type is
        cast to builtin bool to avoid numpy.bool_ identity issues in tests.
    """
    vertices2d = [(float(x), float(y)) for x, y, _ in vertices3d]
    return bool(is_ccw(LinearRing(vertices2d)))
