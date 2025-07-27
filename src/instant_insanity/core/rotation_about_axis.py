import numpy as np
from instant_insanity.core.type_check import check_array_float64

def rotation_matrix_about_line(p: np.ndarray, u: np.ndarray, theta: float) -> np.ndarray:
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
