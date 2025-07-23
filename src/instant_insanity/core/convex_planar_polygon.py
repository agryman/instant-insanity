"""
This module defines the ConvexPlanarPolygon class.
"""

import numpy as np
import numpy.typing as npt

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
        vertices: the (n,3) array of n 3d points defining the vertices
        edges: the (n,3) array of n 3d vectors defining the edges
        normal: the 3d vector normal to the plane of the polygon
    """

    vertices: npt.NDArray[np.float64]
    edges: npt.NDArray[np.float64]
    normal: npt.NDArray[np.float64]

    def __init__(self, vertices: npt.NDArray[np.float64]) -> None:

        # check the type of vertices
        if not isinstance(vertices, np.ndarray):
            raise TypeError("vertices must be a NumPy array")

        if vertices.dtype != np.float64:
            raise TypeError("vertices must contain 64-bit floats")

        self.vertices = vertices

        # check the number of dimensions
        ndim: int = vertices.ndim
        if ndim != 2:
            raise ValueError("vertices must be a 2-d array")

        n: int
        d: int
        n, d = vertices.shape
        if n < 3:
            raise ValueError("there must be at least 3 vertices.")
        if d != 3:
            raise ValueError("each vertex must be a 3-d point")

        # compute the array of edge vectors and
        # check that each edge is at least the minimum allowed length
        self.edges = np.zeros_like(vertices)
        i1: int
        for i1 in range(n):
            i2: int = (i1 + 1) % n
            edge: npt.NDArray[np.float64] = vertices[i2] - vertices[i1]
            self.edges[i1] = edge
            edge_length: float = float(np.linalg.norm(edge))
            if edge_length < MIN_EDGE_LENGTH:
                raise ValueError(f"edge {i1} is too small")

        # compute the normal vector from the cross product of the first two edges
        normal: npt.NDArray[np.float64] = np.cross(self.edges[0], self.edges[1])
        if np.allclose(normal, 0.0):
            raise ValueError("the normal to the polygon plane is approximately 0")
        self.normal = normal

        # each edge vector must be orthogonal to the normal
        i: int
        for i in range(n):
            dot: float = np.dot(normal, self.edges[i])
            if not np.isclose(dot,0.0):
                raise ValueError(f"edge {i} is not orthogonal to the normal")

        # test for convexity
        # define the inward-pointing vector normal cross edge1