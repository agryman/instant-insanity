import numpy as np
import pytest
from instant_insanity.core.geometry import get_translation  # replace with actual module name

def test_get_translation_identity():
    v1 = np.array([[0.0, 0.0, 0.0],
                   [1.0, 0.0, 0.0],
                   [0.0, 1.0, 0.0],
                   [0.0, 0.0, 1.0]], dtype=np.float64)
    v2 = v1.copy()
    t = get_translation(v1, v2)
    assert np.allclose(t, np.zeros(3))

def test_get_translation_simple_translation():
    v1 = np.array([[0.0, 0.0, 0.0],
                   [1.0, 0.0, 0.0],
                   [0.0, 1.0, 0.0],
                   [0.0, 0.0, 1.0]], dtype=np.float64)
    translation = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    v2 = v1 + translation
    t = get_translation(v1, v2)
    assert np.allclose(t, translation)

def test_get_translation_with_floating_point_tolerance():
    v1 = np.array([[1.0, 2.0, 3.0],
                   [4.0, 5.0, 6.0],
                   [7.0, 8.0, 9.0],
                   [10.0, 11.0, 12.0]], dtype=np.float64)
    translation = np.array([0.1, -0.2, 0.3], dtype=np.float64)
    v2 = v1 + translation
    # Introduce a tiny floating-point noise within tolerance
    v2[2, 1] += 1e-12
    t = get_translation(v1, v2)
    assert np.allclose(t, translation)

def test_get_translation_not_a_translation():
    v1 = np.array([[0.0, 0.0, 0.0],
                   [1.0, 0.0, 0.0],
                   [0.0, 1.0, 0.0],
                   [0.0, 0.0, 1.0]], dtype=np.float64)
    # Change only one point inconsistently
    v2 = v1.copy()
    v2[1] += np.array([1.0, 2.0, 3.0])
    with pytest.raises(ValueError):
        get_translation(v1, v2)

def test_get_translation_invalid_shape():
    v1 = np.zeros((4, 3), dtype=np.float64)
    v2 = np.zeros((3, 3), dtype=np.float64)  # invalid shape
    with pytest.raises(ValueError):
        get_translation(v1, v2)
