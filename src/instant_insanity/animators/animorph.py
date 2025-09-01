"""This module defines Animorph."""

from abc import ABC, abstractmethod
from typing import Any, Callable, TypeAlias

import numpy as np
from manim import Mobject, Animation, ValueTracker, Scene
from manim.typing import Point3D

Updater: TypeAlias = Callable[[Any], object]


def lerp(a_0: np.ndarray, a_1: np.ndarray, alpha: float) -> np.ndarray:
    """
    Compute the linear interpolation between two arrays.
    Args:
        a_0: the array at alpha = 0
        a_1: the array at alpha = 1
        alpha: the interpolation parameter, usually between 0 and 1.

    Returns:
        the interpolated array.
    """
    return (1.0 - alpha) * a_0 + alpha * a_1


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
    alpha: float
    mobject: Mobject

    def __init__(self, mobject: Mobject):
        self.alpha = 0.0
        self.mobject = mobject

    @abstractmethod
    def morph_to(self, alpha: float) -> None:
        """Morphs the mobject to the given state."""
        assert 0.0 <= alpha <= 1.0
        self.alpha = alpha

    def play(self, scene: Scene, start_alpha: float = 0.0, end_alpha: float = 1.0, run_time: float = 1.0,
             **kwargs) -> None:
        """
        Plays the animation.
        Args:
            scene: the Scene that contains the animation.
            start_alpha: the starting value of alpha for the animation, between 0 and 1 inclusive.
            end_alpha: the ending value of the alpha parameter, between 0 and 1 inclusive.
            run_time: the runtime of the animation, a positive number.

        Returns:

        """
        assert 0.0 <= start_alpha <= 1.0
        assert 0.0 <= end_alpha <= 1.0
        assert run_time > 0.0
        alpha_tracker = ValueTracker(start_alpha)
        updater: Updater = lambda mobject: self.morph_to(alpha_tracker.get_value())
        self.mobject.add_updater(updater)
        scene.play(alpha_tracker.animate.set_value(end_alpha), run_time=run_time, **kwargs)
        self.mobject.remove_updater(updater)


class MoveToAnimorph(Animorph):
    """
    This class is a simple Animorph that moves the mobject to the given end position.
    This mainly for testing the Animorph framework.
    """
    start_point: Point3D
    end_point: Point3D

    def __init__(self, mobject: Mobject, end_point: Point3D):
        super().__init__(mobject)
        self.start_point = mobject.get_center()
        self.end_point = end_point

    def morph_to(self, alpha: float) -> None:
        super().morph_to(alpha)
        alpha_position: Point3D = self.start_point + alpha * (self.end_point - self.start_point)
        self.mobject.move_to(alpha_position)


class AnimorphAnimation(Animation):
    """
    An animation that morphs an Animorph.
    This is simply an adapter class that adapts Animorph to the Animation class.

    Attributes:
        animorph: the Animorph instance.
    """
    animorph: Animorph

    def __init__(self, animorph: Animorph):
        super().__init__(animorph.mobject)
        self.animorph = animorph

    def interpolate_mobject(self, alpha: float) -> None:
        self.animorph.morph_to(alpha)
