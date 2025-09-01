"""
This module defines the ConvexPlanarPolygon class.
"""

import numpy as np
from shapely.geometry import Polygon
from shapely.validation import explain_validity

from instant_insanity.core.type_check import check_matrix_nx3_float64, check_array_float64


def check_convex_polygon(points: np.ndarray) -> None:
    """Validate that a NumPy array of 2D points defines a valid, convex polygon.

    Args:
        points: A NumPy array of shape (n, 2) representing polygon vertices.

    Raises:
        ValueError: If the input does not define a valid convex polygon.
    """
    check_array_float64(points, 'points', 2, 2)

    if points.shape[0] < 3:
        raise ValueError('A polygon must have at least 3 points.')

    polygon = Polygon(points)

    if not polygon.is_valid:
        reason = explain_validity(polygon)
        raise ValueError(f'Invalid polygon geometry: {reason}')

    if not polygon.equals(polygon.convex_hull):
        raise ValueError('The polygon is not convex.')


# the default minimum polygon edge length
MIN_EDGE_LENGTH: float = 1e-3


class ConvexPlanarPolygon:
    """
    A convex planar polygon is a nonempty subset of a plane in euclidean 3-space
    that is the intersection of three or more half-planes.

    The vertices of the polygon are the intersections of the half-planes.
    The polygon is therefore defined by its vertex list.

    The edges are vectors that point from each vertex to the next one with wrap-around.

    Attributes:
        vertices: The (n,3) array of vertices.
        min_edge_length: The minimum length of the edges.
        unit_i: unit vector tangent to the polygon plane along the first edge.
        unit_j: unit vector tangent to the polygon plane orthogonal to unit_i.
        unit_k: unit vector perpendicular to the polygon plane forming a right-handed system.
    """

    vertices: np.ndarray
    min_edge_length: float
    unit_i: np.ndarray
    unit_j: np.ndarray
    unit_k: np.ndarray

    def __init__(self, vertices: np.ndarray, min_edge_length: float = MIN_EDGE_LENGTH) -> None:

        # validate min_edge_length
        if min_edge_length <= 0.0:
            raise ValueError('minimum edge length must be positive')
        self.min_edge_length = min_edge_length

        # validate vertices
        check_matrix_nx3_float64(vertices)
        n: int
        d: int
        n, d = vertices.shape
        if n < 3:
            raise ValueError('there must be at least 3 vertices.')
        self.vertices = vertices

        # compute coordinate axes defined by the polygon
        unit_i: np.ndarray = vertices[1] - vertices[0]
        if np.allclose(unit_i, 0):
            raise ValueError('unit_i vector is ill-defined')
        unit_i = unit_i / np.linalg.norm(unit_i)
        self.unit_i = unit_i

        unit_k: np.ndarray = np.cross(unit_i, vertices[2] - vertices[1])
        if np.allclose(unit_k, 0):
            raise ValueError('unit_k vector is ill-defined')
        unit_k = unit_k / np.linalg.norm(unit_k)
        self.unit_k = unit_k

        unit_j: np.ndarray = np.cross(unit_k, unit_i)
        if np.allclose(unit_j, 0):
            raise ValueError('unit_j vector is ill-defined')
        unit_j = unit_j / np.linalg.norm(unit_j)
        self.unit_j = unit_j

        # Compute edge vectors using np.roll to wrap around the polygon
        edges: np.ndarray = np.roll(vertices, -1, axis=0) - vertices  # shape (n, 3)

        # Compute edge lengths
        edge_lengths: np.ndarray = np.linalg.norm(edges, axis=1)  # shape (n,)
        short_edges: np.ndarray = edge_lengths < min_edge_length

        if np.any(short_edges):
            i: int = int(np.where(short_edges)[0][0])
            raise ValueError(f'edge {i} is too small')

        # Check planarity: dot product with unit_k must be zero
        # Use abs(dot) > tol rather than np.isclose to avoid ambiguity with array inputs
        dot_products: np.ndarray = edges @ unit_k  # shape (n,)
        nonplanar: np.ndarray = ~np.isclose(dot_products, 0.0)

        if np.any(nonplanar):
            i = int(np.where(nonplanar)[0][0])
            raise ValueError(f'edge {i} is nonplanar')

        # compute the 2d coordinates of the polygon and check for convexity
        v_rel: np.ndarray = vertices - vertices[0]  # shape (n, 3)
        T: np.ndarray = np.stack((unit_i, unit_j), axis=1)  # shape (3, 2)
        xy: np.ndarray = v_rel @ T  # shape (n, 2)
        check_convex_polygon(xy)
