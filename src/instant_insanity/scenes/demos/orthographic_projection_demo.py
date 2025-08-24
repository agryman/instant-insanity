import numpy as np

from manim.typing import Vector3D
from manim import Scene, Polygon, Text, tempconfig, DOWN, BLACK

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FaceName
from instant_insanity.core.geometry_types import PolygonId
from instant_insanity.core.projection import OrthographicProjection
from instant_insanity.core.puzzle import PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC, Puzzle, PuzzleCube, PuzzleCubeNumber, \
    PuzzleCubeSpec
from instant_insanity.mobjects.puzzle_cube_3d import PuzzleCube3D
from instant_insanity.scenes.coordinate_grid import GridMixin


class OrthographicProjectionDemo(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        # create an orthographic projection that foreshortens the edges
        direction: Vector3D = np.array([1.5, 1, 5], dtype=np.float64)
        u: Vector3D = direction / np.linalg.norm(direction)
        projection:OrthographicProjection = OrthographicProjection(u)

        # create the cube object
        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        puzzle: Puzzle = Puzzle(puzzle_spec)
        cube_number: PuzzleCubeNumber = PuzzleCubeNumber.ONE
        puzzle_cube: PuzzleCube = puzzle.number_to_cube[cube_number]
        cube_spec: PuzzleCubeSpec = puzzle_cube.cube_spec
        cube: PuzzleCube3D = PuzzleCube3D(projection, cube_spec)
        self.add(cube)

        # find the scene coordinates of the centre of the front face
        front_id: PolygonId = PuzzleCube3D.name_to_id(FaceName.FRONT)
        front_face: Polygon = cube.id_to_scene_polygon[front_id]
        centre: np.ndarray = front_face.get_center()
        centre_str: str = f'front face centre = ({centre[0]:.2f}, {centre[1]:.2f}, {centre[2]:.2f})'
        centre_text: Text = Text(centre_str, color=BLACK)
        centre_text.move_to(1.5 * DOWN)
        self.add(centre_text)

        direction_str: str = f'projection direction = ({direction[0]:.2f}, {direction[1]:.2f}, {direction[2]:.2f})'
        direction_text: Text = Text(direction_str, color=BLACK)
        direction_text.move_to(2.5 * DOWN)
        self.add(direction_text)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = OrthographicProjectionDemo()
        scene.render()
