import numpy as np
from instant_insanity.animators.animorph import lerp

def test_lerp():
    a_0 = np.array([1.0, 0.0, 0.5], dtype=np.float64)
    a_1 = np.array([0.0, 1.0, 0.5], dtype=np.float64)
    alpha = 0.25
    expected = np.array([0.75, 0.25, 0.5], dtype=np.float64)
    actual = lerp(a_0, a_1, alpha)
    assert np.allclose(actual, expected)
