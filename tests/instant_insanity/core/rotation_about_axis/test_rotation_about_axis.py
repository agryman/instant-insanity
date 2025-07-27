import math
import numpy as np
import pytest
from instant_insanity.core.rotation_about_axis import rotation_matrix_about_line

def test_rotation_matrix_identity():
    p = np.array([0, 0, 0], dtype=np.float64)
    u = np.array([1, 0, 0], dtype=np.float64)
    theta = 0.0
    expected = np.eye(4, dtype=np.float64)
    assert np.allclose(rotation_matrix_about_line(p, u, theta), expected)

def test_rotation_matrix_about_z_axis():
    p = np.array([0, 0, 0], dtype=np.float64)
    u = np.array([0, 0, 1], dtype=np.float64)
    theta = np.pi / 2
    actual = rotation_matrix_about_line(p, u, theta)
    expected = np.array([
        [0, -1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ], dtype=np.float64)
    assert np.allclose(actual, expected)

def test_rotation_matrix_invalid_shape():
    p = np.array([0, 0], dtype=np.float64)
    u = np.array([0, 0, 1], dtype=np.float64)
    theta = 0.0
    with pytest.raises(ValueError):
        rotation_matrix_about_line(p, u, theta)

def test_rotation_matrix_non_unit_vector():
    p = np.array([0, 0, 0], dtype=np.float64)
    u = np.array([0, 0, 10], dtype=np.float64)
    theta = 0.0
    with pytest.raises(ValueError):
        rotation_matrix_about_line(p, u, theta)

@pytest.mark.parametrize('p, u, v, theta, expected', [
    # Rotate around Z-axis at origin by 90 degrees
    (np.array([0, 0, 0]), np.array([0, 0, 1]), np.array([1, 0, 0]), np.pi / 2, np.array([0, 1, 0])),

    # Rotate around X-axis at origin by 180 degrees
    (np.array([0, 0, 0]), np.array([1, 0, 0]), np.array([0, 1, 0]), np.pi, np.array([0, -1, 0])),

    # Rotate around Y-axis at origin by 90 degrees
    (np.array([0, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1]), np.pi / 2, np.array([1, 0, 0])),

    # Rotate around arbitrary axis through point (1,0,0) by 90 degrees
    (np.array([1, 0, 0]), np.array([0, 0, 1]), np.array([2, 0, 0]), np.pi / 2, np.array([1, 1, 0])),

    # Rotate point coinciding with axis, should remain unchanged
    (np.array([1, 2, 3]), np.array([0, 1, 0]), np.array([1, 5, 3]), np.pi / 3, np.array([1, 5, 3])),
])
def test_rotation_matrix_applied_to_point(p, u, v, theta, expected):
    p = p.astype(np.float64)
    u = u.astype(np.float64)
    v = v.astype(np.float64)
    R = rotation_matrix_about_line(p, u, theta)
    v_homogeneous = np.append(v, 1)
    rotated_v = R @ v_homogeneous
    assert np.allclose(rotated_v[:3], expected)

@pytest.mark.parametrize('v3, expected_rot_v3', [
    ([1, 1, 1], [1, 1, 1]),
    ([-1, -1, -1], [-1, -1, -1]),
    ([1, -1, 1], [1, 1, -1]),
    ([1, 1, -1], [-1, 1, 1]),
    ([-1, 1, 1], [1, -1, 1]),
])
def test_one_third_rotation_about_main_diagonal_of_cube(v3, expected_rot_v3):
    p = np.array([0, 0, 0], dtype=np.float64)
    u = np.array([1, 1, 1], dtype=np.float64) / math.sqrt(3)
    theta = 2 * np.pi / 3
    rot4 = rotation_matrix_about_line(p, u, theta)
    v4 = np.append(v3, 1)
    actual_rot_v4 = rot4 @ v4
    actual_rot_v3 = actual_rot_v4[:3]
    assert np.allclose(actual_rot_v3, expected_rot_v3)

@pytest.mark.parametrize('v3, expected_rot_v3', [
    ([1, -1, 1], [1, -1, 1]),
    ([1, -1, -1], [3, -1, 1]),
    ([1, 1, -1], [3, 1, 1]),
    ([1, 1, 1], [1, 1, 1]),
])
def test_unfold_left_face_of_cube(v3, expected_rot_v3):
    p = np.array([1, 1, 1], dtype=np.float64)
    u = np.array([0, -1, 0], dtype=np.float64)
    theta = np.pi / 2
    rot4 = rotation_matrix_about_line(p, u, theta)
    v3 = np.array([1, -1, 1], dtype=np.float64)
    v4 = np.append(v3, 1)
    actual_rot_v4 = rot4 @ v4
    actual_rot_v3 = actual_rot_v4[:3]
    expected_rot_v3 = np.array([1, -1, 1], dtype=np.float64)
    assert np.allclose(actual_rot_v3, expected_rot_v3)
