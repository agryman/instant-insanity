import pytest
import numpy as np
from instant_insanity.core.type_check import check_vector3_float64, check_matrix_nx3_float64

# -------- Tests for check_vector3_float64 --------

def test_valid_vector3_float64():
    v = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    check_vector3_float64(v)  # Should not raise

@pytest.mark.parametrize("v", [
    [1.0, 2.0, 3.0],                      # not a numpy array
    np.array([1, 2, 3], dtype=np.int32),  # wrong dtype
    np.array([[1.0, 2.0, 3.0]], dtype=np.float64),  # wrong ndim
    np.array([1.0, 2.0], dtype=np.float64),         # wrong length
])
def test_invalid_vector3_float64(v):
    with pytest.raises((TypeError, ValueError)):
        check_vector3_float64(v)

# -------- Tests for check_matrix_nx3_float64 --------

def test_valid_matrix_nx3_float64():
    m = np.array([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0]], dtype=np.float64)
    check_matrix_nx3_float64(m)  # Should not raise

@pytest.mark.parametrize("m", [
    [[1.0, 2.0, 3.0]],                         # not a numpy array
    np.array([[1.0, 2.0, 3.0]], dtype=np.float32),  # wrong dtype
    np.array([1.0, 2.0, 3.0], dtype=np.float64),    # wrong ndim
    np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float64),  # wrong shape
])
def test_invalid_matrix_nx3_float64(m):
    with pytest.raises((TypeError, ValueError)):
        check_matrix_nx3_float64(m)