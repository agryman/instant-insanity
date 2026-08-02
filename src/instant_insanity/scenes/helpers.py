from manim import Scene

from instant_insanity.animators.puzzle_3d_animators import Puzzle3DAnimorph
from instant_insanity.mobjects.puzzle_3d import Puzzle3D


def morph_and_checkpoint(
        scene: Scene,
        animorph: Puzzle3DAnimorph,
        run_time: float = 1.0,
        wait_time: float = 0.5
) -> None:
    """
    This method conceals the puzzle, morphs it, and then checkpoints it.
    It is the generic puzzle animation sequence.
    Args:
        scene: The scene to animate
        animorph: the Puzzle3D animorph
        run_time: the run time of the animation
        wait_time: the wait time after the animation
    """
    puzzle3d: Puzzle3D = animorph.get_puzzle3d()
    puzzle3d.conceal_polygons()
    animorph.play(scene, run_time=run_time)
    puzzle3d.checkpoint()
    scene.wait(wait_time)
