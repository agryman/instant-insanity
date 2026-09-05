from manim import Scene, tempconfig

from instant_insanity_core.animorphs.puzzle_3d_animorphs import Puzzle3DSetCubeGapAnimorph
from kwargs_xyz_core.config import LINEN_CONFIG
from manim_cairo3d.projection import Projection, mk_standard_orthographic_projection
from instant_insanity_core.puzzle import WINNING_MOVES_PUZZLE_SPEC
from instant_insanity_core.mobjects.puzzle_3d import PuzzleSpec, Puzzle3D, mk_standard_puzzle3d, DEFAULT_BUFF
from instant_insanity_core.coordinate_grid import GridMixin


class Puzzle3DSetCubeGapAnimorphDemo(GridMixin, Scene):
    """
    This class demonstrates how to play a puzzle 3d cube rotation.
    """
    def construct(self):
        self.add_grid(True)

        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        projection: Projection = mk_standard_orthographic_projection()
        puzzle3d: Puzzle3D = mk_standard_puzzle3d(puzzle_spec, projection, centre=True)
        self.add(puzzle3d)
        self.wait()

        initial_gap: float = puzzle3d.get_cube_gap()
        min_gap: float = DEFAULT_BUFF

        # set the cube gap
        target_gap: float
        for target_gap in [min_gap, initial_gap]:
            animorph = Puzzle3DSetCubeGapAnimorph(puzzle3d, target_gap)
            puzzle3d.conceal_polygons()
            animorph.play(self, run_time=1.0)
            self.wait()
            puzzle3d.checkpoint()

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = Puzzle3DSetCubeGapAnimorphDemo()
        scene.render()
