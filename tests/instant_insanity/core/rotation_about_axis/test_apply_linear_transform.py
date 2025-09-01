import math
import numpy as np
import pytest
from instant_insanity.core.transformation import rotation_matrix_about_line, apply_linear_transform

def test_identity():
    mat: np.ndarray = np.eye(4, 4, dtype=np.float64)
    v: np.ndarray = np.eye(4, 3, dtype=np.float64)
    actual: np.ndarray = apply_linear_transform(mat, v)
    expected: np.ndarray = v
    assert np.allclose(actual, expected)

def test_rotate_about_z_90():
    p: np.ndarray = np.zeros(3, dtype=np.float64)
    u: np.ndarray = np.array([0, 0, 1], dtype=np.float64)
    theta: float = np.pi / 2.0
    mat: np.ndarray = rotation_matrix_about_line(p, u, theta)
    v: np.ndarray = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float64)
    actual: np.ndarray = apply_linear_transform(mat, v)
    expected: np.ndarray = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]], dtype=np.float64)
    assert np.allclose(actual, expected)
