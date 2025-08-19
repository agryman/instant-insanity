"""
The class morphs the outline of polygon into a dot.
"""
import math

import numpy as np
from manim import Polygon, Dot, PI, RIGHT, UP
from manim.typing import Point3D

from instant_insanity.animators.tracked_vgroup_animator import TrackedVGroupAnimator
from instant_insanity.core.force_ccw import force_ccw
from instant_insanity.core.geometry_types import VertexPath
from instant_insanity.core.plane import xy_polar
from instant_insanity.mobjects.tracked_polygon import TrackedPolygon
from instant_insanity.mobjects.tracked_vgroup import TrackedVGroup

DEFAULT_MINIMUM_SECTOR_COUNT: int = 12

class PolygonToDotAnimator(TrackedVGroupAnimator):
    """
    Morphs the outline of polygon into a dot.

    Attributes:
        dot: the target dot.
        dot_centre: the center of the dot.
        dot_radius: the radius of the dot.
        polygon_centre: the center of the initial polygon.
        w0_theta: the angles of w0, the refined vertices relative to polygon_centre.
        w0_radius: the radii of w0.
    """
    dot: Dot
    dot_centre: Point3D
    dot_radius: float
    polygon_centre: Point3D
    w0_theta: np.ndarray
    w0_radius: np.ndarray

    def __init__(self, tracked_polygon: TrackedPolygon, dot: Dot, minimum_sector_count=DEFAULT_MINIMUM_SECTOR_COUNT) :
        assert isinstance(tracked_polygon, TrackedPolygon)
        super().__init__(tracked_polygon)

        polygon: Polygon = tracked_polygon.polygon
        force_ccw(polygon)

        polygon_centre: Point3D = polygon.get_center() # (3,)
        v: VertexPath = polygon.get_vertices() # (m,3)
        v0: VertexPath = v - polygon_centre # (m,3)

        v0_radius: np.ndarray # (m,)
        v0_theta: np.ndarray # (m,)
        v0_radius, v0_theta = xy_polar(v0)

        delta_v0: np.ndarray = np.roll(v0, -1, axis=0) - v0 # (m,3)
        delta_v0_theta: np.ndarray = np.roll(v0_theta, -1) - v0_theta # (m,)
        delta_v0_theta = np.mod(delta_v0_theta, 2 * np.pi)

        delta_theta_max: float = 2.0 * PI / minimum_sector_count # maximum allowed sector angle
        w0_list: list[np.ndarray] = [] # list of refined vertices on edge i
        i: int
        v0_i: np.ndarray
        # refine each edge of the polygon
        for i, v0_i in enumerate(v0):

            # the angle subtended by edge i
            delta_v0_theta_i: float = float(delta_v0_theta[i])

            # the number of segments on this edge, n_i >= 1
            n_i: int = math.ceil(delta_v0_theta_i / delta_theta_max)

            # the t parameter step size for each subsector on this edge
            t_step_i: float = 1.0 / n_i

            # the t parameter array for this edge
            t_array_i: np.ndarray = t_step_i * np.arange(n_i) # (n_i,)

            # the change in the initial vertex for this edge
            delta_w0_i: np.ndarray = np.outer(t_array_i, delta_v0[i]) # (n_i, 3)

            # the array of refined vertices along this edge
            w0_i: np.ndarray = v0_i + delta_w0_i # (n_i, 3)
            w0_list.append(w0_i)

        # the refined vertex path
        w0: np.ndarray = np.vstack(w0_list) # (n_0 + n_1 + ..., 3)
        w0_radius: np.ndarray
        w0_theta: np.ndarray
        w0_radius, w0_theta = xy_polar(w0)

        w: np.ndarray = w0 + polygon_centre

        # update the polygon
        PolygonToDotAnimator.update_polygon(polygon, w)

        # set the object attributes
        self.polygon_centre = polygon_centre
        self.dot = dot
        self.dot_centre = dot.get_center()
        self.dot_radius = dot.radius
        self.w0_radius = w0_radius
        self.w0_theta = w0_theta

    @staticmethod
    def update_polygon(polygon, w):
        polygon.set_points_as_corners(w)
        polygon.close_path()

    def interpolate(self, alpha: float) -> None:
        super().interpolate(alpha)

        tracked_vgroup: TrackedVGroup = self.tracked_vgroup
        assert isinstance(tracked_vgroup, TrackedPolygon)
        tracked_polygon: TrackedPolygon = tracked_vgroup
        polygon: Polygon = tracked_polygon.polygon

        w0_radius_alpha: np.ndarray = (1.0 - alpha) * self.w0_radius +  alpha * self.dot_radius # (m,)
        w0_x_alpha: np.ndarray = w0_radius_alpha * np.cos(self.w0_theta) # (m,)
        w0_y_alpha: np.ndarray = w0_radius_alpha * np.sin(self.w0_theta) # (m,)
        w0_alpha: np.ndarray = np.outer(w0_x_alpha, RIGHT) + np.outer(w0_y_alpha, UP) # (m,3)

        centre_alpha: np.ndarray = (1.0 - alpha) * self.polygon_centre + alpha * self.dot_centre # (3,)
        w_alpha: np.ndarray = w0_alpha + centre_alpha # (m,3)

        PolygonToDotAnimator.update_polygon(polygon, w_alpha)
