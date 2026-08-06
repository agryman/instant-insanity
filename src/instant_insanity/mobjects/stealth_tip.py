"""
This module makes a stealth arrow tip mobject that can be added to a cubic Bézier curve
to indicate the direction of the edge.
"""
from dataclasses import dataclass

import numpy as np
from manim import CubicBezier, StealthTip, BLACK
from manim.typing import Point3D, Vector3D, Point3D_Array

from instant_insanity.core.puzzle import PuzzleCubeNumber

type CubeEdgeTip = dict[PuzzleCubeNumber, EdgeTip]

@dataclass
class EdgeTip:
    curve: CubicBezier
    forward: bool
    tip: StealthTip


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

    points: Point3D_Array = curve.points
    assert len(points) == 4

    p0: Point3D = points[0]
    p1: Point3D = points[1]
    p2: Point3D = points[2]
    p3: Point3D = points[3]

    pt: Point3D = (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3
    vt: Vector3D = 3 * (1 - t) ** 2 * (p1 - p0) + 6 * (1 - t) * t * (p2 - p1) + 3 * t ** 2 * (p3 - p2)

    return pt, vt


def find_node_boundary_parameter(curve: CubicBezier,
                                 node_radius: float,
                                 forward: bool = True,
                                 step: float = 0.01,
                                 iterations: int = 60) -> float:
    """
    Find the curve parameter at which the curve crosses the boundary of the node dot
    that it ends on.

    The curve is assumed to end at the centre of the node, so the distance from that
    centre is 0 at the end of the curve and grows as the parameter moves into the curve.
    This finds the first crossing of the node radius, which is the point at which the
    curve emerges from the dot.

    A loop starts and ends at the same node, so the distance is not monotonic along the
    whole curve. Searching outwards from the end of the curve finds the correct crossing
    for a loop as well as for a curve that joins two distinct nodes.

    Args:
        curve: the cubic Bézier curve.
        node_radius: the radius of the node dot.
        forward: a boolean flag indicating the direction of the curve.
        step: the sampling step used to bracket the crossing.
        iterations: the number of bisection steps used to refine the crossing.

    Returns:
        the curve parameter at the crossing.
    """
    points: Point3D_Array = curve.points
    assert len(points) == 4

    node_centre: Point3D = points[3] if forward else points[0]

    def parameter_at(s: float) -> float:
        """Convert a distance s travelled inwards from the end into a curve parameter."""
        return 1.0 - s if forward else s

    def distance_at(s: float) -> float:
        p: Point3D
        p, _ = get_cubic_bezier_point_tangent(curve, parameter_at(s))
        return float(np.linalg.norm(p - node_centre))

    # bracket the crossing by sampling inwards from the end of the curve.
    s_inside: float = 0.0
    s_outside: float = 0.0
    while s_outside < 1.0:
        s_outside = min(s_outside + step, 1.0)
        if distance_at(s_outside) >= node_radius:
            break
    else:
        # the whole curve lies within the node dot, so give up and use the far end.
        return parameter_at(1.0)

    # bisect between the bracketing parameters.
    for _ in range(iterations):
        s_middle: float = 0.5 * (s_inside + s_outside)
        if distance_at(s_middle) < node_radius:
            s_inside = s_middle
        else:
            s_outside = s_middle

    return parameter_at(0.5 * (s_inside + s_outside))


def mk_stealth_tip_at_node_boundary(curve: CubicBezier,
                                    node_radius: float,
                                    forward: bool = True,
                                    scale: float = 1.0,
                                    width_ratio: float = 1.0) -> StealthTip:
    """
    Makes a stealth arrow tip whose point touches the boundary of the node dot that the
    curve ends on, aligned with the tangent of the curve at that point of contact.

    Unlike mk_stealth_tip_from_cubic_bezier, which centres the tip on the curve at a
    parameter set back from the end, this places the point of the arrow itself on the
    dot, so the whole tip sits outside the dot and points into it.

    Args:
        curve: the cubic Bézier curve.
        node_radius: the radius of the node dot that the curve ends on.
        forward: a boolean flag indicating the direction of the curve.
        scale: the scaling factor for the tip, which scales it uniformly.
        width_ratio: the factor to narrow the tip by, across its axis only.
            A value of 1.0 leaves the tip at its default proportions.

    Returns:
        the stealth tip mobject correctly positioned and rotated to touch the node dot.
    """
    t: float = find_node_boundary_parameter(curve, node_radius, forward)
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

    # narrow the tip while its axis still lies along the x axis, so that stretching in y
    # is a stretch across the tip. this must happen before the rotation, since stretch
    # works on the world axes. it leaves the point and the base of the tip untouched,
    # because both lie on the x axis, and so it changes neither the length nor tip_point.
    tip.stretch(width_ratio, dim=1)

    tip.rotate(theta)

    # put the point of the arrow on the boundary of the dot, rather than its centre.
    tip.shift(p - tip.tip_point)

    return tip


def mk_stealth_tip_from_cubic_bezier(curve: CubicBezier,
                                     forward: bool = True,
                                     t_buff: float = 0.5,
                                     scale: float = 1.0) -> StealthTip:
    """
    Makes a stealth arrow tip that lies on top of a cubic Bézier curve to indicate the direction of the edge.
    The centre of the tip is set back from the end of the curve.

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
