from abc import ABC, abstractmethod

from manim import Mobject

# a Picture is a Mobject
type Picture = Mobject

class ParameterSpace:
    """Empty base class representing a parameter space."""
    pass


class DrawFunction[P: ParameterSpace](ABC):
    """Generic abstract base for a draw function parameterized by a ParameterSpace subclass."""

    @abstractmethod
    def draw_picture(self, params: P) -> Picture:
        """
        Draw something using a parameter from the parameter space.

        Args:
            params: a point in the parameter space.

        Returns:
            the picture defined by the given params.

        Raises:
            NotImplementedError.
        """
        raise NotImplementedError


class ParameterPath[P: ParameterSpace](ABC):
    """
    Generic abstract base for a parameter path parameterized by a ParameterSpace subclass.
    """

    @abstractmethod
    def params_at(self, alpha: float) -> P:
        """
        Sample a parameter from the path at position alpha ∈ [0,1].

        Args:
            alpha: the path parameter.

        Returns:
            the point in parameter space corresponding to the given alpha.

        Raises:
            NotImplementedError.
        """
        raise NotImplementedError
