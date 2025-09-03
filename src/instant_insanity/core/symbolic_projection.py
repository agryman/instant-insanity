"""
This module implements a symbolic version of the projection of points in model space onto
the camera plane.

Refer to projection.md for the math.

We use SymPy datatypes instead of NumPy.
The two main types are:
Scalar: real numbers, modelled as Expr
Vector: real vectors in 3D space modelled Matrix with shape (3,1), e.g. as column vectors
"""

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Protocol

from sympy import Expr, Matrix, sqrt, S, Rational, Integer

type Scalar = Expr
type Vector = Matrix

# define the unit vectors
UNIT_I: Vector = Matrix([S.One, S.Zero, S.Zero])
UNIT_J: Vector = Matrix([S.Zero, S.One, S.Zero])
UNIT_K: Vector = Matrix([S.Zero, S.Zero, S.One])


class Planar(Protocol):
    """
    A planar region is defined by giving any base point b on it and a nonzero normal vector n.
    The plane consists of all the points p that satisfy (p - b) @ n = 0.
    """

    def get_point(self) -> Vector:
        """
        Gets any point on the plane.

        Returns:
            A base point on the plane.
        """
        ...

    def get_normal(self) -> Vector:
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
    scene_origin: Vector
    scene_per_model: Scalar

    def __post_init__(self) -> None:
        assert isinstance(self.scene_origin, Matrix)
        assert self.scene_origin.shape == (3, 1)

        assert isinstance(self.scene_per_model, Expr)
        assert self.scene_per_model.is_positive

    def convert_model_to_scene(self, model_point: Vector) -> Vector:
        """
        Converts a point in model space to a point in scene space.
        Args:
            model_point: the point in model space to convert.

        Returns:
            the point in scene space.
        """
        assert isinstance(model_point, Matrix)
        assert model_point.shape == (3, 1)

        return (model_point - self.scene_origin) * self.scene_per_model

    def convert_scene_to_model(self, scene_point: Vector) -> Vector:
        """
        Converts a point in scene space to a point in model space.
        Args:
            scene_point: the point in scene space to convert.

        Returns:
            the point in model space.
        """
        assert isinstance(scene_point, Matrix)
        assert scene_point.shape == (3, 1)

        return scene_point / self.scene_per_model + self.scene_origin


class Projection(ABC):
    """
    This is the abstract base class for projections.

    Attributes:
        scene_x: The x-offset to subtract from the projection onto the camera plane.
        scene_y: The y-offset to subtract from the projection onto the camera plane.
        camera_z: The z coordinate c of the camera plane.
        scale: the scale factor to convert model coordinates to camera coordinates.

    """

    scene_x: Scalar
    scene_y: Scalar
    camera_z: Scalar
    scale: Scalar
    conversion: ModelToSceneConversion

    def __init__(self,
                 scene_x: Scalar = S.Zero,
                 scene_y: Scalar = S.Zero,
                 camera_z: Scalar = S.Zero,
                 scale: Scalar = S.One) -> None:
        self.scene_x = scene_x
        self.scene_y = scene_y
        self.camera_z = camera_z
        self.scale = scale

        scene_origin: Vector = scene_x * UNIT_I + scene_y * UNIT_J + camera_z * UNIT_K
        scene_per_model: Scalar = scale
        self.conversion = ModelToSceneConversion(scene_origin, scene_per_model)

    @abstractmethod
    def compute_u(self, model_point: Vector) -> Vector:
        pass

    def project_point(self, model_point: Vector) -> Vector:
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
        assert isinstance(model_point, Matrix)
        u: Vector = self.compute_u(model_point)

        return self._project_point_along_u(model_point, u)

    def project_points(self, model_points: Matrix) -> Matrix:
        assert isinstance(model_points, Matrix)

        projected_points: Matrix = Matrix([self.project_point(model_point)
                                           for model_point in model_points])
        return projected_points.T

    def _project_point_along_u(self, model_point: Vector, u: Vector) -> Vector:
        """Projects the model point onto the camera plane along the direction given by the unit vector u.

        This is a protected method. It is the responsibility of callers to ensure that u is a unit vector.

        Args:
            model_point: A Vector containing a point (mx, my, mz) in model space.
            u: A Vector containing a unit direction vector.

        Returns:
            A Vector containing (x, y, mz) where (x, y, c) is the projection of the model point onto
                the camera plane z=c.

        Raises:
            TypeError: if model_point is not a Vector.
            ValueError: if model_point is not a 3-vector or the z-component of u is too small.
        """
        u_x: Scalar
        u_y: Scalar
        u_z: Scalar
        u_x, u_y, u_z = u

        m_x: Scalar
        m_y: Scalar
        m_z: Scalar
        m_x, m_y, m_z = model_point

        c: Scalar = self.camera_z

        t: Scalar = (m_z - c) / u_z
        x: Scalar = m_x - t * u_x - self.scene_x
        y: Scalar = m_y - t * u_y - self.scene_y

        return self.scale * Matrix([x, y, m_z])

    def polygon_t(self, polygon: Planar, x: Scalar, y: Scalar) -> float:
        """
        Compute the t parameter of the point in model space that projects to (x, y, c)
        on the camera plane.
        Args:
            polygon: the plane in model space defined by the convex planar polygon.
            x: the x coordinate of the projected point.
            y: the y coordinate of the projected point.

        Returns:
            the parameter t of the point in model space.

        Let u be the unit vector that defines the direction of the light ray.
        Let p = (x, y, c) be a point on the camera plane.
        Let m be the point in model space that projects to (x, y).
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
        p: Vector = Matrix([
            x / self.scale + self.scene_x,
            y / self.scale + self.scene_y,
            self.camera_z
        ])
        unit_u: Vector = self.compute_u(p)
        b: Vector = polygon.get_point()
        n: Vector = polygon.get_normal()
        t: float = ((b - p).T * n) / (unit_u.T * n)

        return t


class PerspectiveProjection(Projection):
    """This class models a perspective projection.

    Attributes:
        camera_z: A float that specifies the position of the camera plane.
        viewpoint: A 3d point that specifies the position of the viewpoint in model space.
    """
    viewpoint: Vector

    def __init__(self, viewpoint: Vector, **kwargs) -> None:
        """Initialize the projection.

        Args:
            viewpoint: The position of the viewpoint.

        Raises:
            TypeError: if viewpoint is not an NumPy array of type float64.
            ValueError: if viewpoint is not a 3-vector.

        """
        assert isinstance(viewpoint, Matrix)
        assert viewpoint.shape == (3, 1)

        super().__init__(**kwargs)
        self.viewpoint = viewpoint

    def compute_u(self, model_point: Vector) -> Vector:
        assert isinstance(model_point, Matrix)
        assert model_point.shape == (3, 1)

        # compute the unit vector u pointing from the model point to the viewpoint
        direction: Vector = self.viewpoint - model_point
        norm: Scalar = sqrt(direction.T * direction)
        u: Vector = direction / norm

        return u


class OrthographicProjection(Projection):
    """This class models an orthographic projection.

    Attributes:
        u: A unit vector that specifies the direction of the projection.
    """

    u: Vector

    def __init__(self, u: Vector, **kwargs) -> None:
        """Initializes an orthographic projection object.

        Args:
            u: A unit vector that specifies the direction of the projection.

        Raises:
            TypeError: if u is not a NumPy array of float64 values.
            ValueError: if u is not a unit 3-vector or its z-component is too small.
        """
        assert isinstance(u, Matrix)
        assert u.shape == (3, 1)

        super().__init__(**kwargs)

        norm2: Scalar = u.T * u
        assert norm2 == S.One

        u_z: Scalar
        _, _, u_z = u
        if u_z == S.Zero:
            raise ValueError('unit vector z-component is zero')

        self.u = u

    def compute_u(self, model_point: Vector) -> Vector:
        assert isinstance(model_point, Matrix)
        assert model_point.shape == (3, 1)

        return self.u


def mk_standard_orthographic_projection() -> OrthographicProjection:
    direction: Vector = Matrix([Rational(3, 2), S.One, Integer(5)])
    u: Vector = direction / sqrt(direction.T * direction)
    projection: OrthographicProjection = OrthographicProjection(u,
                                                                scale=Rational(1, 2),
                                                                scene_x=Integer(2),
                                                                scene_y=Integer(-3),
                                                                camera_z=S.One)
    return projection
