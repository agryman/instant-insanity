from abc import ABC, abstractmethod
from typing import Any, TypeAlias, Callable

from manim import Mobject, ValueTracker, Scene

from instant_insanity.mobjects.tracked_vgroup import TrackedVGroup

Updater: TypeAlias = Callable[[Any], object]


class TrackedVGroupAnimator(ABC):
    tracked_vgroup: TrackedVGroup

    def __init__(self, tracked_vgroup: Mobject) -> None:
        assert isinstance(tracked_vgroup, TrackedVGroup)
        self.tracked_vgroup = tracked_vgroup

    def mk_updater(self) -> Updater:
        """
        Make a nontime-based updater function for the animation.

        Returns:
            An updater for the animation.
        """

        def updater(tracked_vgroup: Mobject) -> object:
            """
            Updates the TrackedVGroup instance to its current alpha parameter.

            Args:
                tracked_vgroup: the TrackedVGroup that is being animated.

            Returns:
                the TrackedVGroup.
            """
            assert isinstance(tracked_vgroup, TrackedVGroup)
            tracked_vgroup.remove(*tracked_vgroup.submobjects)
            tracker: ValueTracker = tracked_vgroup.tracker
            alpha: float = tracker.get_value()
            self.interpolate(alpha)
            return tracked_vgroup

        return updater

    def play(self, scene: Scene, alpha: float = 1.0, run_time: float = 1.0) -> None:
        """
        Plays the animation.
        Args:
            scene: the Scene that contains the animation.
            alpha: the maximum value of the alpha parameter, between 0 and 1 inclusive.
            run_time: the runtime of the animation.

        Returns:

        """
        assert 0.0 <= alpha <= 1.0
        updater: Updater = self.mk_updater()
        tracked_vgroup: TrackedVGroup = self.tracked_vgroup
        tracked_vgroup.add_updater(updater)
        tracker: ValueTracker = tracked_vgroup.tracker
        scene.play(tracker.animate.set_value(alpha), run_time=run_time)
        tracked_vgroup.remove_updater(updater)


    @abstractmethod
    def interpolate(self, alpha: float) -> None:
        tracked_vgroup: TrackedVGroup = self.tracked_vgroup
        tracker: ValueTracker = tracked_vgroup.tracker
        tracker.set_value(alpha)
