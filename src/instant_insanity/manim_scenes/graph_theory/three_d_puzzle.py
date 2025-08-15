"""
This module implements the ThreeDPuzzle class which is a group that consists
of four ThreeDPuzzleCube instances, all drawn using a common projection.
"""
from typing import TypeAlias

from manim import VGroup

from instant_insanity.core.projection import Projection
from instant_insanity.core.puzzle import Puzzle, PuzzleSpec, PuzzleCube, PuzzleCubeNumber
from instant_insanity.manim_scenes.graph_theory.three_d_puzzle_cube import ThreeDPuzzleCube

CubeNumberToCubeMapping: TypeAlias = dict[PuzzleCubeNumber, ThreeDPuzzleCube]

class ThreeDPuzzle(VGroup):
    """
    This class implements a 3D puzzle.
    The puzzle consists of four 3D puzzle cubes.
    The puzzle contains the flattened list of all the faces of the cubes.
    Since each cube has six faces, there are a total of 24 polygons in the puzzle.
    A face from one cube may obscure a face from another cube so the set of all faces
    must be depth-sorted as a whole.

    Attributes:
        projection: the projection from model space to scene space.
        puzzle_spec: the puzzle specification which gives the colours of all faces.
        puzzle: the Puzzle object defined by the puzzle specification.
        cube_to_mobject: the mapping from cube numbers to 3D cube objects
    """
    projection: Projection
    puzzle_spec: PuzzleSpec
    puzzle: Puzzle
    cube_to_mobject: CubeNumberToCubeMapping

    def __init__(self, projection: Projection, puzzle_spec: PuzzleSpec, **kwargs) -> None:
        super().__init__(**kwargs)
        self.projection = projection
        self.puzzle_spec = puzzle_spec
        self.puzzle = Puzzle(puzzle_spec)
        self.cube_to_mobject = {cube_number: ThreeDPuzzleCube(projection, puzzle_spec[cube_number])
                                for cube_number in PuzzleCubeNumber}