from typing import Any

from manim import VGroup, ValueTracker


class TrackedVGroup(VGroup):
    """
    This class is a VGroup with a ValueTracker.

    Attributes:
        tracker: the ValueTracker
    """
    tracker: ValueTracker

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.tracker = ValueTracker(0.0)
