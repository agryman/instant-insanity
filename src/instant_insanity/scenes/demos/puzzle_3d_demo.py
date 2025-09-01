import numpy as np

from manim.typing import Point3D, Vector3D
from manim import Scene, tempconfig, LEFT, RIGHT, UP, DOWN, IN, OUT

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.projection import Projection, PerspectiveProjection
from instant_insanity.core.puzzle import PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC, Puzzle
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, DEFAULT_CUBE_ONE_CENTRE, DEFAULT_CUBE_CENTRE_DELTA, \
    DEFAULT_CUBE_SIDE_LENGTH
from instant_insanity.scenes.coordinate_grid import GridMixin


class Puzzle3DDemo(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        # create a projection
        scene_x: float = 0.0
        scene_y: float = -1.5
        camera_z: float = 2.0
        viewpoint: np.ndarray = np.array([0, 2, 6], dtype=np.float64)
        projection: Projection = PerspectiveProjection(viewpoint,
                                                       scene_x=scene_x,
                                                       scene_y=scene_y,
                                                       camera_z=camera_z)

        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        puzzle: Puzzle = Puzzle(puzzle_spec)

        buff: float = DEFAULT_CUBE_SIDE_LENGTH / 4
        cube_one_centre: Point3D = 1.5 * (DEFAULT_CUBE_SIDE_LENGTH + buff) * LEFT + 2 * IN
        cube_centre_delta: Vector3D = (DEFAULT_CUBE_SIDE_LENGTH + buff) * RIGHT
        puzzle3d: Puzzle3D = Puzzle3D(projection, puzzle, cube_one_centre, cube_centre_delta)

        self.add(puzzle3d)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = Puzzle3DDemo()
        scene.render()

