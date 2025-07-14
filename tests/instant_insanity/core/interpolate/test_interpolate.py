import numpy as np
import pytest
from instant_insanity.core.interpolate import interpolate  # Replace with actual module name if needed

def test_basic_interpolation():
    x = interpolate(0.0, 1.0, 5)
    expected = np.array([
        0.0,
        0.15625,
        0.5,
        0.84375,
        1.0
    ])
    np.testing.assert_allclose(x, expected, rtol=1e-8, atol=1e-10)

def test_start_and_end_values():
    x0, x1, n = -3.0, 7.0, 10
    x = interpolate(x0, x1, n)
    assert pytest.approx(x[0], rel=1e-12) == x0
    assert pytest.approx(x[-1], rel=1e-12) == x1

def test_monotonicity():
    # Ensure the values increase smoothly for x0 < x1
    x = interpolate(2.0, 5.0, 100)
    assert np.all(np.diff(x) >= 0)

def test_flat_curve():
    # If x0 == x1, all values should be equal
    x = interpolate(4.2, 4.2, 10)
    expected = np.full(10, 4.2)
    np.testing.assert_array_almost_equal(x, expected)

def test_invalid_n():
    with pytest.raises(ValueError):
        interpolate(0.0, 1.0, 1)