from abc import ABC

from manim import Mobject

from instant_insanity.animators.tracked_vgroup_animator import TrackedVGroupAnimator
from instant_insanity.mobjects.three_d_polygons import TrackedThreeDPolygons


class ThreeDPolygonsAnimator(TrackedVGroupAnimator, ABC):
    """
    This is the abstract base class for `ThreeDPolygons` animators.
    """
    def __init__(self, three_d_polygons: Mobject) -> None:
        if not isinstance(three_d_polygons, TrackedThreeDPolygons):
            raise TypeError(f'three_d_polygons must be of type ThreeDPolygons but got {type(three_d_polygons)}')
        super().__init__(three_d_polygons)
