"""This module defines Animorph."""

from abc import ABC, abstractmethod
from manim import Mobject, Animation, ValueTracker

from instant_insanity.animators.tracked_vgroup_animator import TrackedVGroupAnimator


class Animorph(ABC):
    """A visual object that interpolates between two states.

    An Animorph represents a visual object whose appearance can be
    continuously morphed between two states. The interpolation is
    controlled by the parameter `alpha`, with values in the range
    [0, 1].

    - When `alpha=0.0`, the object is in its initial state.
    - When `alpha=1.0`, the object is in its final state.
    - Intermediate values of `alpha` smoothly blend between the two.

    This class provides a convenient abstraction for educational
    animations where smooth visual transitions illustrate underlying
    concepts.

    Attributes:
        mobject: The animation mobject.
        alpha: Interpolation parameter in [0, 1] that controls
            the morphing between the two visual states.
    """
    mobject: Mobject
    alpha: float

    def __init__(self, mobject: Mobject):
        self.mobject = mobject
        self.alpha_tracker = ValueTracker()

    @abstractmethod
    def morph_to(self, alpha: float) -> None:
        """Morphs the mobject to the given state."""
        self.alpha = alpha

class AnimorphAnimation(Animation):
    """
    An animation that morphs an Animorph.

    Attributes:
        animorph:
    """
    animorph: Animorph
    def __init__(self, animorph: Animorph):
        super().__init__(animorph.mobject)
        self.animorph = animorph

    def interpolate_mobject(self, alpha: float) -> None:
        self.animorph.morph_to(alpha)

class AnimorphAnimator(TrackedVGroupAnimator):
    pass