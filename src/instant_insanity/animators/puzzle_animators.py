from manim import Mobject
from manim.typing import Vector3D

from instant_insanity.animators.animorph import Animorph
from instant_insanity.core.puzzle import PuzzleCubeNumber
from instant_insanity.mobjects.puzzle_3d import Puzzle3D


class PuzzleAnimorph(Animorph):
    """
    This is the abstract base class for Puzzle3D animorphs.
    """

    def __init__(self, puzzle: Puzzle3D) -> None:
        if not isinstance(puzzle, Puzzle3D):
            raise TypeError(f'Expected a Puzzle3D but got {type(puzzle)}')
        super().__init__(puzzle)

    def get_puzzle(self) -> Puzzle3D:
        mobject: Mobject = self.mobject
        assert isinstance(mobject, Puzzle3D)
        puzzle: Puzzle3D = mobject
        return puzzle

class PuzzleRigidMotionAnimorph(PuzzleAnimorph):
    """
    This class applies a rigid motion to the entire puzzle.

    Attributes:
        rotation: the rotation vector.
        translation: the translation vector.
    """
    rotation: Vector3D
    translation: Vector3D

    def __init__(self, puzzle: Puzzle3D,
                 rotation: Vector3D,
                 translation: Vector3D) -> None:
        super().__init__(puzzle)
        self.rotation = rotation
        self.translation = translation

class IndividualCubeAnimorph(PuzzleAnimorph):
    """
    This subclass animates an individual cube within the puzzle.

    Attributes:
        cube_number: the individual cube being animated.
    """
    cube_number: PuzzleCubeNumber

    def __init__(self, puzzle: Puzzle3D, cube_number: PuzzleCubeNumber) -> None:
        super().__init__(puzzle)
        self.cube_number = cube_number


