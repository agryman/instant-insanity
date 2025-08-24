from typing import Self

import numpy as np
from manim.typing import Vector3D
from scipy.spatial.transform import Rotation

from instant_insanity.core.geometry_types import Vector, Vertex, VertexPath
from instant_insanity.core.type_check import check_array_float64

def rotation_matrix_about_line(p: Vertex, u: Vector, theta: float) -> np.ndarray:
    """Computes the rotation matrix around an arbitrary line in 3D.

    Args:
        p: A 3-element array representing a point on the axis of rotation.
        u: A 3-element unit vector along the axis of rotation.
        theta: The angle of rotation in radians, counterclockwise using the right-hand rule.

    Returns:
        np.ndarray: A 4x4 homogeneous rotation matrix.
    """
    check_array_float64(p, "p", 1, 3)
    check_array_float64(u, "u", 1, 3)

    norm_u: np.floating = np.linalg.norm(u)
    if not np.isclose(norm_u, 1.0):
        raise ValueError('u must be a unit vector')

    # Compute skew-symmetric matrix of u
    ux: float
    uy: float
    uz: float
    ux, uy, uz = u
    k_mat3: np.ndarray = np.array([
        [0, -uz, uy],
        [uz, 0, -ux],
        [-uy, ux, 0]
    ], dtype=np.float64)

    # Rodrigues' rotation formula for rotation around u through origin
    rot_mat3: np.ndarray = np.eye(3) + np.sin(theta) * k_mat3 + (1 - np.cos(theta)) * k_mat3 @ k_mat3

    # Build homogeneous rotation matrix around axis through point p
    t_mat: np.ndarray = np.eye(4, dtype=np.float64)
    #t_mat[:3, :3] = rot_mat3
    t_mat[:3, 3] = -p

    t_inv: np.ndarray = np.eye(4, dtype=np.float64)
    t_inv[:3, 3] = p

    rot_mat: np.ndarray = np.eye(4, dtype=np.float64)
    rot_mat[:3, :3] = rot_mat3

    # Complete transformation: translate to origin, rotate, translate back
    rotation_matrix: np.ndarray = t_inv @ rot_mat @ t_mat

    return rotation_matrix


def apply_linear_transform(mat: np.ndarray, v: VertexPath) -> np.ndarray:
    """Apply a 4×4 transformation matrix to an array of n 3D vectors.

    Args:
        mat: A NumPy array of shape (4, 4) representing a linear transformation.
        v: A NumPy array of shape (n, 3), each row a 3D vector.

    Returns:
        A NumPy array of shape (n, 3) with the transformed 3D vectors.
    """
    if mat.shape != (4, 4):
        raise ValueError('mat must be of shape (4, 4)')
    if v.ndim != 2 or v.shape[1] != 3:
        raise ValueError('v must be of shape (n, 3)')

    # Convert to homogeneous coordinates by appending a column of ones
    n: int = v.shape[0]
    v_hom: np.ndarray = np.hstack([v, np.ones((n, 1), dtype=v.dtype)])

    # Apply transformation
    v_transformed: np.ndarray = v_hom @ mat.T

    # Return only the x, y, z components
    return v_transformed[:, :3]


def transform_vertex_path(rotation: Vector, translation: Vector, vertex_path: VertexPath) -> np.ndarray:
    """
    Transform the vertices by applying a rotation followed by a translation.

    Let R be a rotation, let T be a translation, and let V be a vertex.
    The transformed vertex is R(V) + T.

    Args:
        rotation: a rotation 3-vector.
        translation: a translation 3-vector.
        vertex_path: a matrix of n 3-vectors.

    Returns:
        the matrix of n transformed 3-vectors.
    """
    rot = Rotation.from_rotvec(rotation)
    return rot.apply(vertex_path) + translation


class RigidMotion:
    rotation: Vector3D
    translation: Vector3D

    def __init__(self, rotation: Vector3D, translation: Vector3D):
        self.rotation = rotation
        self.translation = translation

    def transform_path(self, path_0: VertexPath) -> VertexPath:
        path: VertexPath = transform_vertex_path(self.rotation,
                                                 self.translation,
                                                 path_0)
        return path

    def mk_at(self, alpha: float) -> Self:
        """
        Makes a copy of the rigid motion at the given alpha.

        Args:
            alpha: the interpolation parameter.

        Returns:
            the new rigid motion at the given alpha.
        """
        alpha_rotation: Vector3D = alpha * self.rotation
        alpha_translation: Vector3D = alpha * self.translation

        return RigidMotion(alpha_rotation, alpha_translation)
