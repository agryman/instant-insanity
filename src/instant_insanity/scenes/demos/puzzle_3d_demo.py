import numpy as np

from manim.typing import Point3D, Vector3D
from manim import Scene, tempconfig, RIGHT, IN, UP

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.projection import Projection, PerspectiveProjection
from instant_insanity.core.puzzle import PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC, Puzzle
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, DEFAULT_CUBE_SIDE_LENGTH
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.part_3_graph_theory.construct_graph import ConstructGraph


class Puzzle3DDemo(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        # create a projection
        # viewpoint: np.ndarray = np.array([0, 2, 6], dtype=np.float64)
        # camera_z: float = 2.0
        # scene_x: float = -1.25
        # scene_y: float = -1.5
        # projection: Projection = PerspectiveProjection(
        #     viewpoint,
        #     camera_z=camera_z,
        #     scene_x=scene_x,
        #     scene_y=scene_y
        # )

        projection: Projection = ConstructGraph.mk_orthographic_projection()

        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        puzzle: Puzzle = Puzzle(puzzle_spec)

        # buff: float = DEFAULT_CUBE_SIDE_LENGTH / 4
        # puzzle_centre: Point3D = 2 * IN
        # cube_delta: Vector3D = (DEFAULT_CUBE_SIDE_LENGTH + buff) * RIGHT
        # puzzle3d: Puzzle3D = Puzzle3D(projection, puzzle, puzzle_centre, cube_delta)

        # create the 3D puzzle
        buff: float = DEFAULT_CUBE_SIDE_LENGTH * 2.0 * (np.sqrt(2.0) - 1.0)
        puzzle_centre: Point3D = 2 * IN + 4.5 * RIGHT + 1.0 * UP
        cube_delta: Vector3D = (DEFAULT_CUBE_SIDE_LENGTH + buff) * RIGHT
        puzzle3d: Puzzle3D = Puzzle3D(projection, puzzle, puzzle_centre, cube_delta)


        self.add(puzzle3d)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = Puzzle3DDemo()
        scene.render()

