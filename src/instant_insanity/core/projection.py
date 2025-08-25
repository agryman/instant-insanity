"""
This module implements projection of points in model space onto
the camera plane.

Refer to projection.md for the math.
"""

from abc import ABC, abstractmethod

import numpy as np

from instant_insanity.core.convex_planar_polygon import ConvexPlanarPolygon
from instant_insanity.core.type_check import check_vector3_float64, check_matrix_nx3_float64


class Projection(ABC):
    """
    This is the abstract base class for projections.

    Attributes:
        scene_x: The x-offset to subtract from the projection onto the camera plane.
        scene_y: The y-offset to subtract from the projection onto the camera plane.
        camera_z: The z coordinate c of the camera plane.
        scale: the scale factor to convert model coordinates to camera coordinates.

    """

    camera_z: float

    def __init__(self, scene_x: float = 0.0, scene_y: float = 0.0, camera_z: float = 2.0, scale: float = 1.0) -> None:
        self.scene_x = scene_x
        self.scene_y = scene_y
        self.camera_z = camera_z
        self.scale = scale

    @abstractmethod
    def compute_u(self, model_point: np.ndarray) -> np.ndarray:
        pass

    def project_point(self, model_point: np.ndarray) -> np.ndarray:
        """Projects the model point onto the camera plane and computes its parameter t along the projection line.

        Args:
            model_point: A point in model space.

        Returns:
            A 3-vector containing (x, y, t) where (x, y, c) is the projection of the model point onto
                the camera plane z=c and t is the parameter value of the model point along the projection line.

        Raises:
            TypeError: if model_point is not a NumPy array of float64 values.
            ValueError: if model_point is not a 3-vector
        """
        check_vector3_float64(model_point)
        u: np.ndarray = self.compute_u(model_point)

        return self._project_point_along_u(model_point, u)

    def project_points(self, model_points: np.ndarray) -> np.ndarray:
        check_matrix_nx3_float64(model_points)

        projected_points: list[np.ndarray] = [self.project_point(model_point)
                                              for model_point in model_points]
        return np.array(projected_points, dtype=np.float64)

    def _project_point_along_u(self, model_point: np.ndarray, u: np.ndarray) -> np.ndarray:
        """Projects the model point onto the camera plane along the direction given by the unit vector u.

        This is a protected method. It is the responsibility of callers to ensure that u is a unit vector.

        Args:
            model_point: A NumPy array containing a point in model space.
            u: A NumPy array containing a unit direction vector.

        Returns:
            A NumPy array containing (x, y, t) where (x, y, c) is the projection of the model point onto
                the camera plane z=c and t is the parameter value of the model point along the projection line.

        Raises:
            TypeError: if model_point is not a NumPy array of float64 values.
            ValueError: if model_point is not a 3-vector or the z-component of u is too small.
        """
        u_x: float
        u_y: float
        u_z: float
        u_x, u_y, u_z = u
        if np.isclose(u_z, 0.0):
            raise ValueError('unit vector z-component is too small')

        m_x: float
        m_y: float
        m_z: float
        m_x, m_y, m_z = model_point

        c: float = self.camera_z

        t: float = (m_z - c) / u_z
        x: float = m_x - t * u_x - self.scene_x
        y: float = m_y - t * u_y - self.scene_y

        return  self.scale * np.array((x, y, t), dtype=np.float64)

    def polygon_t(self, polygon: ConvexPlanarPolygon, x: float, y: float) -> float:
        """
        Compute the t parameter of the point in model space that projects to (x, y).
        Args:
            polygon: the convex planar polygon in model space.
            x: the x coordinate of the projected point.
            y: the y coordinate of the projected point.

        Returns:
            the parameter t of the point in model space.

        Let u be the unit vector that defines the direction of the light ray.
        Let P = (x, y, c) be a point on the camera plane.
        Let M be the point in model space that projects to (x, y).
        We have:
        M = P + t * u
        for some parameter t.

        Let v0 be the first vertex of the polygon.
        Let k be the unit vector perpendicular to the plane of the polygon.
        Any model point M that lies on the polygon satisfies:
        (M - v0) @ k = 0
        where here @ means dot product.

        Therefore (P + t * u - v0) @ k = 0. We can solve for t as follows:
        t = (v0 - P) @ k / u @ k
        """
        p: np.ndarray = np.array([
            x / self.scale + self.scene_x,
            y / self.scale + self.scene_y,
            self.camera_z
        ], dtype=np.float64)
        unit_u: np.ndarray = self.compute_u(p)
        v0: np.ndarray = polygon.vertices[0]
        unit_k: np.ndarray = polygon.unit_k
        t: float = np.dot(v0 - p, unit_k) / np.dot(unit_u, unit_k)

        return t


class PerspectiveProjection(Projection):
    """This class models a perspective projection.

    Attributes:
        camera_z: A float that specifies the position of the camera plane.
        viewpoint: A 3d point that specifies the position of the viewpoint in model space.
    """
    viewpoint: np.ndarray

    def __init__(self, viewpoint: np.ndarray, **kwargs) -> None:
        """Initialize the projection.

        Args:
            viewpoint: The position of the viewpoint.

        Raises:
            TypeError: if viewpoint is not an NumPy array of type float64.
            ValueError: if viewpoint is not a 3-vector.

        """
        check_vector3_float64(viewpoint)

        super().__init__(**kwargs)
        self.viewpoint = viewpoint

    def compute_u(self, model_point: np.ndarray) -> np.ndarray:
        check_vector3_float64(model_point)

        # compute the unit vector u pointing from the model point to the viewpoint
        direction: np.ndarray  = self.viewpoint - model_point
        norm: np.floating = np.linalg.norm(direction)
        if np.isclose(norm, 0.0):
            raise ValueError('model point is too close to viewpoint')
        u: np.ndarray = direction / norm

        return u


class OrthographicProjection(Projection):
    """This class models an orthographic projection.

    Attributes:
        u: A unit vector that specifies the direction of the projection.
    """

    u: np.ndarray

    def __init__(self, u: np.ndarray, **kwargs) -> None:
        """Initializes an orthographic projection object.

        Args:
            u: A unit vector that specifies the direction of the projection.

        Raises:
            TypeError: if u is not a NumPy array of float64 values.
            ValueError: if u is not a unit 3-vector or its z-component is too small.
        """
        check_vector3_float64(u)

        super().__init__(**kwargs)

        norm: np.floating = np.linalg.norm(u)
        if not np.isclose(norm, 1.0):
            raise ValueError('u must be a unit vector')

        u_z: float
        _, _, u_z = u
        if np.isclose(u_z, 0.0):
            raise ValueError('unit vector z-component is too small')

        self.u = u

    def compute_u(self, model_point: np.ndarray) -> np.ndarray:
        check_vector3_float64(model_point)

        return self.u
