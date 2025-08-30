"""
This module makes a stealth arrow tip mobject that can be added to a cubic Bézier curve
to indicate the direction of the edge.
"""
import numpy as np
from manim import Mobject, CubicBezier, StealthTip, BLACK
from manim.typing import Point3D, Vector3D

def get_cubic_bezier_point_tangent(curve: CubicBezier, t: float) -> tuple[Point3D, Vector3D]:
    """
    Compute the point and its tangent on the cubic Bézier curve that corresponds to a parameter value t.

    B(t) = (1-t)^3 * P0 + 3*(1-t)^2 *t*P1 + 3*(1-t)*t^2 * P2 + t^3*P3

    B'(t) = 3*(1-t)^2*(P1 - P0) + 6*(1-t)*t*(P2 - P1) + 3*t^2*(P3 - P2)

    Args:
        curve: the cubic Bézier curve.
        t: the curve parameter 0 <= t <= 1.

    Returns:
        the point and its tangent on the cubic Bézier curve.
    """
    assert 0.0 <= t <= 1.0

    points: np.ndarray = curve.points
    assert len(points) == 4

    p0: Point3D = points[0]
    p1: Point3D = points[1]
    p2: Point3D = points[2]
    p3: Point3D = points[3]

    pt: Point3D = (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3
    vt: Vector3D = 3 * (1 - t) ** 2 * (p1 - p0) + 6 * (1 - t) * t * (p2 - p1) + 3 * t ** 2 * (p3 - p2)

    return pt, vt


def mk_stealth_tip_from_cubic_bezier(curve: CubicBezier,
                                     forward: bool = True,
                                     t_buff: float = 0.5,
                                     scale: float = 1.0) -> StealthTip:
    """
    Makes a stealth arrow tip that lies on top of a cubic Bézier curve to indicate the direction of the edge.
    The centre of the tip is set back from the end of the curver.

    Args:
        curve: the cubic Bézier curve.
        forward: a boolean flag indicating the direction of the curve.
        t_buff: the buffer for the parameter t. It should be positive if the curve ends on a dot.
        scale: the scaling factor for the tip.

    Returns:
        the stealth tip mobject correctly positioned and rotated to lie over one end of the curve.
    """
    t: float = 1.0 - t_buff if forward else t_buff
    p: Point3D
    v: Vector3D
    p, v = get_cubic_bezier_point_tangent(curve, t)
    u: Vector3D = v / np.linalg.norm(v)

    theta: float = float(np.atan2(u[1], u[0]))
    if not forward:
        theta += np.pi

    tip: StealthTip = StealthTip(
            length=0.25,
            fill_color=BLACK,
            fill_opacity=1.0,
            stroke_color=BLACK,
            stroke_width=1)
    tip.scale(scale)
    tip.rotate(theta)
    tip.move_to(p)

    return tip
