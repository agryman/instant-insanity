"""
This module implements projection of points in model space onto
the camera plane.

Refer to projection.md for the math.
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Protocol

import numpy as np
from manim import RIGHT, UP, OUT
from manim.typing import Point3D, Vector3D, Point3D_Array

from instant_insanity.core.type_check import check_vector3_float64, check_matrix_nx3_float64


class Planar(Protocol):
    """
    A planar region is defined by giving any base point b on it and a nonzero normal vector n.
    The plane consists of all the points p that satisfy (p - b) @ n = 0.
    """

    def get_point(self) -> Point3D:
        """
        Gets any point on the plane.

        Returns:
            A base point on the plane.
        """
        ...

    def get_normal(self) -> Vector3D:
        """
        Gets any nonzero vector that is normal to the plane.

        Returns:
            A nonzero normal vector.
        """
        ...


@dataclass
class ModelToSceneConversion:
    """
    This class converts between model space and scene space.

    Attributes
        scene_origin: the model space point that maps to ORIGIN in scene space.
        scene_per_model: the conversion factor from model to scene distances.

    For example, the standard cube in model space has side length = 2.0.
    To make it look like a cube in scene space with side length = 1.0 use scene_per_model = 0.5.
    """
    scene_origin: Point3D
    scene_per_model: float

    def convert_model_to_scene(self, model_point: Point3D) -> Point3D:
        """
        Converts a point in model space to a point in scene space.
        Args:
            model_point: the point in model space to convert.

        Returns:
            the point in scene space.
        """
        return (model_point - self.scene_origin) * self.scene_per_model

    def convert_scene_to_model(self, scene_point: Point3D) -> Point3D:
        """
        Converts a point in scene space to a point in model space.
        Args:
            scene_point: the point in scene space to convert.

        Returns:
            the point in model space.
        """
        return scene_point / self.scene_per_model + self.scene_origin


class Projection(ABC):
    """
    This is the abstract base class for projections.

    Attributes:
        camera_z: the z-coordinate c of the camera plane.
        conversion: the transformation that converts model space to scene space.
    """

    camera_z: float
    conversion: ModelToSceneConversion

    def __init__(self,
                 camera_z: float = 2.0,
                 scene_x: float = 0.0,
                 scene_y: float = 0.0,
                 scene_z: float = 0.0,
                 scene_per_model: float = 1.0
                 ) -> None:
        self.camera_z = camera_z

        scene_origin: Point3D = scene_x * RIGHT + scene_y * UP + scene_z * OUT
        self.conversion = ModelToSceneConversion(scene_origin, scene_per_model)

    @abstractmethod
    def compute_u(self, model_point: Point3D) -> Vector3D:
        pass

    def project_point(self, model_point: Point3D) -> Point3D:
        """Projects the model point onto the camera plane and computes its parameter t along the projection line.

        Args:
            model_point: A point in model space.

        Returns:
            A NumPy array containing (x, y, mz) where (x, y, c) is the projection of the model point onto
                the camera plane z=c.

        Raises:
            TypeError: if model_point is not a NumPy array of float64 values.
            ValueError: if model_point is not a 3-vector
        """
        check_vector3_float64(model_point)
        u: Vector3D = self.compute_u(model_point)

        return self._project_point_along_u(model_point, u)

    def project_points(self, model_points: Point3D_Array) -> Point3D_Array:
        check_matrix_nx3_float64(model_points)

        projected_points: list[Point3D] = [self.project_point(model_point)
                                              for model_point in model_points]
        return np.array(projected_points, dtype=np.float64)

    def _project_point_along_u(self, model_point: Point3D, u: Vector3D) -> Point3D:
        """Projects the model point onto the camera plane along the direction given by the unit vector u.

        This is a protected method. It is the responsibility of callers to ensure that u is a unit vector.

        Args:
            model_point: A NumPy array containing a point (mx, my, mz) in model space.
            u: A NumPy array containing a unit direction vector.

        Returns:
            A NumPy array containing (x, y, mz) where (x, y, c) is the projection of the model point onto
                the camera plane z=c.

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

        p: Point3D = np.array((x, y, m_z), dtype=np.float64)

        return self.conversion.convert_model_to_scene(p)

    def polygon_t(self, polygon: Planar, x: float, y: float) -> float:
        """
        Compute the t parameter of the point in model space that projects to (x, y, c)
        on the camera plane.
        Args:
            polygon: the plane in model space defined by the convex planar polygon.
            x: the x-coordinate of the projected point in scene space.
            y: the y-coordinate of the projected point in scene space.

        Returns:
            the t-parameter of the point in model space.

        Let u be the unit vector that defines the direction of the light ray.
        Let s = (x, y, z) be a point in scene space where z is not given.
        Let p = (p_x, p_y, c) be the corresponding point on the camera plane.
        Let m be the point in the polygon in model space that projects to p.
        We have:
        m = p + t * u
        for some parameter t.

        Let b be any base point in the plane defined by the polygon.
        Let n be any nonzero vector normal to the plane of the polygon.
        Any model point m that lies on the plane satisfies:
        (m - b) @ n = 0
        where here @ means dot product.

        Therefore (p + t * u - b) @ n = 0.

        We can solve for t as follows:
        t = (b - p) @ n / u @ n
        """

        # we are not given the z-coordinate of the point in scene space so set it to 0.0
        scene_point: Point3D = np.array([x, y, 0.0], dtype=np.float64)
        p: Point3D = self.conversion.convert_scene_to_model(scene_point)
        # we want the corresponding point in model space to lie on the camera plane
        p[2] = self.camera_z

        unit_u: Vector3D = self.compute_u(p)
        b: Point3D = polygon.get_point()
        n: Vector3D = polygon.get_normal()
        t: float = np.dot(b - p, n) / np.dot(unit_u, n)

        return t


class PerspectiveProjection(Projection):
    """This class models a perspective projection.

    Attributes:
        camera_z: A float that specifies the position of the camera plane.
        viewpoint: A 3d point that specifies the position of the viewpoint in model space.
    """
    viewpoint: Point3D

    def __init__(self, viewpoint: Point3D, **kwargs) -> None:
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

    def compute_u(self, model_point: Point3D) -> Vector3D:
        check_vector3_float64(model_point)

        # compute the unit vector u pointing from the model point to the viewpoint
        direction: Vector3D = self.viewpoint - model_point
        norm: np.floating = np.linalg.norm(direction)
        if np.isclose(norm, 0.0):
            raise ValueError('model point is too close to viewpoint')
        u: Vector3D = direction / norm

        return u


class OrthographicProjection(Projection):
    """This class models an orthographic projection.

    Attributes:
        u: A unit vector that specifies the direction of the projection.
    """

    u: Vector3D

    def __init__(self, u: Vector3D, **kwargs) -> None:
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

    def compute_u(self, model_point: Point3D) -> Vector3D:
        check_vector3_float64(model_point)

        return self.u


def mk_standard_orthographic_projection() -> OrthographicProjection:
    direction: Vector3D = np.array([1.5, 1, 5], dtype=np.float64)
    u: Vector3D = direction / np.linalg.norm(direction)
    projection: OrthographicProjection = OrthographicProjection(
        u,
        camera_z=1.0,
        scene_x=2.0,
        scene_y=-3.0,
        scene_z=0.0,
        scene_per_model=0.5
    )
    return projection
