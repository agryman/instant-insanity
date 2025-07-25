"""
This module defines the ConvexPlanarPolygon class.
"""

import numpy as np
from shapely.geometry import Polygon
from shapely.validation import explain_validity

from instant_insanity.core.type_check import check_matrix_nx3_float64

def check_convex_polygon(points: np.ndarray) -> None:
    """Validate that a NumPy array of 2D points defines a valid, convex polygon.

    Args:
        points: A NumPy array of shape (n, 2) representing polygon vertices.

    Raises:
        ValueError: If the input does not define a valid convex polygon.
    """
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError('Input must be a 2D NumPy array of shape (n, 2).')

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

    The edges are vectors that point from each vertex to the next one.

    The normal is the vector perpendicular to the plane defined as the cross
    product edges[0] x edges[1].

    Attributes:
        min_edge_length: The minimum length of the edges.
        vertices: The (n,3) array of vertices.
        edges: The (n,3) array of edges.
        unit_normal: The 3d vector unit normal to the plane of the polygon.
    """

    min_edge_length: float
    vertices: np.ndarray
    edges: np.ndarray
    unit_normal: np.ndarray

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

        # compute the array of edge vectors and
        # check that each edge is at least the minimum allowed length
        self.edges = np.zeros_like(vertices)
        i: int
        for i in range(n):
            j: int = (i + 1) % n
            edge: np.ndarray = vertices[j] - vertices[i]
            edge_length: float = float(np.linalg.norm(edge))
            if edge_length < min_edge_length:
                raise ValueError(f'edge {i} is too small')
            self.edges[i] = edge

        # compute the normal vector as the cross product of the first two edges
        normal: np.ndarray = np.cross(self.edges[0], self.edges[1])
        norm: np.floating = np.linalg.norm(normal)
        if np.isclose(norm, 0.0):
            raise ValueError('the normal to the polygon plane is approximately 0')
        self.unit_normal = normal / norm

        # each edge vector must be orthogonal to the normal
        for i in range(n):
            dot: float = np.dot(self.unit_normal, self.edges[i])
            if not np.isclose(dot,0.0):
                raise ValueError(f'edge {i} is not orthogonal to the normal')

        # test for convexity
        # define the inward-pointing vector normal cross edge1