"""
This module implements the TrackedPolygon class.
"""
from manim import Polygon

from instant_insanity.core.geometry_types import VertexPath
from instant_insanity.mobjects.tracked_vgroup import TrackedVGroup


class TrackedPolygon(TrackedVGroup):
    """
    A TrackedPolygon is a TrackedVGroup that contains a single Polygon.

    The Polygon object may change during the course of the animation.
    In this initial implementation, the Polygon identity does not change.
    Only its vertices.

    Attributes:
        polygon: The current Polygon object.
    """
    polygon: Polygon

    def __init__(self, polygon: Polygon, **kwargs):
        super().__init__(**kwargs)
        self.polygon = polygon
        self.add(polygon)

    def update_polygon(self, vertex_path: VertexPath):
        self.polygon.set_points_as_corners(vertex_path)
