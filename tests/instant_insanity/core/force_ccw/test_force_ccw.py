import numpy as np
import pytest
from manim import Polygon, BLUE, ORANGE

from instant_insanity.core.force_ccw import force_ccw, is_ccw_vertices


def test_force_ccw_keeps_ccw_polygon_unchanged():
    # Triangle in CCW order
    p = Polygon([0, 0, 0], [2, 0, 0], [0, 1, 0], color=BLUE)
    before_id = id(p)
    before_vertices = p.get_vertices().copy()

    # Sanity: it starts CCW
    assert is_ccw_vertices(before_vertices) is True

    force_ccw(p)

    after_vertices = p.get_vertices()
    assert id(p) == before_id, 'Object identity must be preserved'
    # Geometry unchanged
    np.testing.assert_allclose(after_vertices, before_vertices, rtol=0, atol=0)
    assert is_ccw_vertices(after_vertices) is True
    # Style preserved
    assert p.get_color() == BLUE


def test_force_ccw_reverses_cw_polygon_in_place():
    # Same triangle but CW order
    p = Polygon([0, 0, 0], [0, 1, 0], [2, 0, 0], color=ORANGE)
    before_id = id(p)
    before_vertices = p.get_vertices().copy()

    # Sanity: it starts CW
    assert is_ccw_vertices(before_vertices) is False

    force_ccw(p)

    after_vertices = p.get_vertices()
    assert id(p) == before_id, 'Object identity must be preserved'
    # Now CCW
    assert is_ccw_vertices(after_vertices) is True
    # Geometry equals the reversal of the original vertex order
    np.testing.assert_allclose(after_vertices, before_vertices[::-1], rtol=0, atol=0)
    # Style preserved
    assert p.get_color() == ORANGE


def test_force_ccw_preserves_stroke_and_fill():
    p = Polygon([0, 0, 0], [2, 0, 0], [1, -1, 0])
    p.set_stroke(width=7, opacity=0.6)
    p.set_fill(color=BLUE, opacity=0.3)
    p.set_z_index(42)

    force_ccw(p)

    # Stroke/fill/z-index should be unchanged (we updated points in place)
    assert p.get_stroke_width() == 7
    assert np.isclose(p.get_stroke_opacity(), 0.6)
    assert p.get_fill_color() == BLUE
    assert np.isclose(p.get_fill_opacity(), 0.3)
    assert p.z_index == 42


@pytest.mark.parametrize(
    'verts_ccw, expected_ccw',
    [
        ([(0, 0, 0), (3, 0, 0), (3, 2, 0), (0, 2, 0)], True),   # rectangle CCW
        ([(0, 0, 0), (0, 2, 0), (3, 2, 0), (3, 0, 0)], False),  # rectangle CW
        ([(1, 1, 0), (3, 1.5, 0), (2.5, 3.5, 0), (0.5, 2.5, 0)], True),  # convex quad CCW
    ],
)
def test_parametric_cases(verts_ccw, expected_ccw):
    p = Polygon(*verts_ccw)
    # Check starting orientation
    assert is_ccw_vertices(p.get_vertices()) is expected_ccw
    # After forcing CCW, orientation must be CCW
    force_ccw(p)
    assert is_ccw_vertices(p.get_vertices()) is True