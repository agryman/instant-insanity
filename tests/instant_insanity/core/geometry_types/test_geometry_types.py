import numpy as np
import pytest

from instant_insanity.core.geometry_types import *

def test_is_vertex_true():
    v = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    assert is_vertex(v)

def test_is_vertex_false_wrong_dtype():
    v = np.array([1, 2, 3], dtype=np.int64)
    assert not is_vertex(v)

def test_is_vertex_false_wrong_shape():
    v = np.array([[1.0, 2.0, 3.0]], dtype=np.float64)
    assert not is_vertex(v)

def test_check_vertex_success():
    v = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    check_vertex(v)  # no exception

def test_check_vertex_type_error():
    with pytest.raises(TypeError):
        check_vertex([0.0, 0.0, 0.0])  # not an ndarray

def test_check_vertex_value_error_dtype():
    with pytest.raises(ValueError):
        check_vertex(np.array([0, 0, 0], dtype=np.int32))

def test_check_vertex_value_error_shape():
    with pytest.raises(ValueError):
        check_vertex(np.array([[0.0, 0.0, 0.0]], dtype=np.float64))

def test_is_vertex_path_true():
    vp = np.array([[0.0, 0.0, 0.0],
                   [1.0, 0.0, 0.0],
                   [0.0, 1.0, 0.0]], dtype=np.float64)
    assert is_vertex_path(vp)

def test_is_vertex_path_false_too_few_rows():
    vp = np.array([[0.0, 0.0, 0.0],
                   [1.0, 0.0, 0.0]], dtype=np.float64)
    assert not is_vertex_path(vp)

def test_is_vertex_path_false_wrong_cols():
    vp = np.array([[0.0, 0.0],
                   [1.0, 0.0],
                   [0.0, 1.0]], dtype=np.float64)
    assert not is_vertex_path(vp)

def test_check_vertex_path_success():
    vp = np.array([[0.0, 0.0, 0.0],
                   [1.0, 0.0, 0.0],
                   [0.0, 1.0, 0.0]], dtype=np.float64)
    check_vertex_path(vp)  # no exception

def test_check_vertex_path_type_error():
    with pytest.raises(TypeError):
        check_vertex_path([[0.0, 0.0, 0.0],
                           [1.0, 0.0, 0.0],
                           [0.0, 1.0, 0.0]])  # not an ndarray

def test_check_vertex_path_value_error_dtype():
    vp = np.array([[0, 0, 0],
                   [1, 0, 0],
                   [0, 1, 0]], dtype=np.int32)
    with pytest.raises(ValueError):
        check_vertex_path(vp)

def test_check_vertex_path_value_error_ndim():
    vp = np.array([[[0.0, 0.0, 0.0]],
                   [[1.0, 0.0, 0.0]],
                   [[0.0, 1.0, 0.0]]], dtype=np.float64)
    with pytest.raises(ValueError):
        check_vertex_path(vp)

def test_check_vertex_path_value_error_cols():
    vp = np.array([[0.0, 0.0],
                   [1.0, 0.0],
                   [0.0, 1.0]], dtype=np.float64)
    with pytest.raises(ValueError):
        check_vertex_path(vp)

def test_check_vertex_path_value_error_rows():
    vp = np.array([[0.0, 0.0, 0.0],
                   [1.0, 0.0, 0.0]], dtype=np.float64)
    with pytest.raises(ValueError):
        check_vertex_path(vp)

def test_as_vertex_success():
    v = as_vertex([1, 2, 3])
    assert v.dtype == np.float64 and v.shape == (3,)

def test_as_vertex_path_success():
    vp = as_vertex_path([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    assert vp.dtype == np.float64 and vp.shape == (3, 3)
