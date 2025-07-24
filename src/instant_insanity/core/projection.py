"""
This module implements projection of points in model space onto
the camera plane.

Refer to projection.md for the math.
"""

from abc import ABC, abstractmethod

import numpy as np

from instant_insanity.core.type_check import check_vector3_float64

class Projection(ABC):
    """
    This is the abstract base class for projections.

    Attributes:
        camera_z: The z coordinate c of the camera plane.
    """

    camera_z: float

    def __init__(self, camera_z: float) -> None:
        self.camera_z = camera_z

    @abstractmethod
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
        pass

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
        x: float = m_x - t * u_x
        y: float = m_y - t * u_y

        return np.array((x, y, t), dtype=np.float64)


class PerspectiveProjection(Projection):
    """This class models a perspective projection.

    Attributes:
        camera_z: A float that specifies the position of the camera plane.
        viewpoint: A 3d point that specifies the position of the viewpoint in model space.
    """
    viewpoint: np.ndarray

    def __init__(self, camera_z: float, viewpoint: np.ndarray) -> None:
        """Initialize the projection.

        Args:
            camera_z: The position c of the camera plane z=c.
            viewpoint: The position of the viewpoint.

        Raises:
            TypeError: if viewpoint is not an NumPy array of type float64.
            ValueError: if viewpoint is not a 3-vector.

        """
        super().__init__(camera_z)

        check_vector3_float64(viewpoint)
        self.viewpoint = viewpoint

    def project_point(self, model_point: np.ndarray) -> np.ndarray:
        check_vector3_float64(model_point)

        # compute the unit vector u pointing from the model point to the viewpoint
        direction: np.ndarray  = self.viewpoint - model_point
        norm: np.floating = np.linalg.norm(direction)
        if np.isclose(norm, 0.0):
            raise ValueError('model point is too close to viewpoint')
        u: np.ndarray = direction / norm

        return self._project_point_along_u(model_point, u)


class OrthographicProjection(Projection):
    """This class models an orthographic projection.

    Attributes:
        camera_z: A float that specifies the position of the camera plane.
        u: A unit vector that specifies the direction of the projection.
    """

    u: np.ndarray

    def __init__(self, camera_z: float, u: np.ndarray) -> None:
        """Initializes an orthographic projection object.

        Args:
            camera_z: A float that specifies the position of the camera plane.
            u: A unit vector that specifies the direction of the projection.

        Raises:
            TypeError: if u is not a NumPy array of float64 values.
            ValueError: if u is not a unit 3-vector or its z-component is too small.
        """
        super().__init__(camera_z)

        check_vector3_float64(u)

        norm: np.floating = np.linalg.norm(u)
        if not np.isclose(norm, 1.0):
            raise ValueError('u must be a unit vector')

        u_z: float
        _, _, u_z = u
        if np.isclose(u_z, 0.0):
            raise ValueError('unit vector z-component is too small')

        self.u = u

    def project_point(self, model_point: np.ndarray) -> np.ndarray:
        """Projects the model point along the direction of the unit vector."""
        check_vector3_float64(model_point)

        return self._project_point_along_u(model_point, self.u)
