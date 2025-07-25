import numpy as np
import pytest
from shapely.errors import GEOSException

from instant_insanity.core.convex_planar_polygon import check_convex_polygon


def test_valid_triangle():
    points = np.array([[0, 0], [1, 0], [0, 1]])
    check_convex_polygon(points)


def test_valid_square():
    points = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
    check_convex_polygon(points)


def test_valid_pentagon():
    points = np.array([[0, 0], [2, 0], [3, 1], [1, 3], [-1, 1]])
    check_convex_polygon(points)


def test_too_few_points():
    points = np.array([[0, 0], [1, 1]])
    with pytest.raises(ValueError, match='at least 3 points'):
        check_convex_polygon(points)


def test_self_intersecting_polygon():
    points = np.array([[0, 0], [2, 2], [0, 2], [2, 0]])
    with pytest.raises(ValueError, match='Self-intersection'):
        check_convex_polygon(points)


def test_concave_polygon():
    points = np.array([[0, 0], [2, 0], [1, 1], [2, 2], [0, 2]])
    with pytest.raises(ValueError, match='not convex'):
        check_convex_polygon(points)


def test_malformed_input_wrong_shape():
    points = np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]])  # shape (3, 3)
    with pytest.raises((ValueError, GEOSException, TypeError)):
        check_convex_polygon(points)


def test_malformed_input_non_numeric():
    points = np.array([['a', 'b'], ['c', 'd'], ['e', 'f']])
    with pytest.raises((ValueError, GEOSException, TypeError)):
        check_convex_polygon(points)