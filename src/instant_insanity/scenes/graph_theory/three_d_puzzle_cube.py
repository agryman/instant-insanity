import numpy as np

from manim import Polygon, ManimColor, GREEN, BLUE, Scene, ORIGIN, LEFT, tempconfig, RIGHT, PI, LineJointType, FadeIn, \
    FadeOut

from instant_insanity.core.geometry_types import Vector, PolygonId, SortedPolygonIdToPolygonMapping
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FaceName
from instant_insanity.core.projection import Projection, PerspectiveProjection
from instant_insanity.core.puzzle import PuzzleCubeSpec
from instant_insanity.mobjects.three_d_puzzle_cube import ThreeDPuzzleCube
from instant_insanity.scenes.coloured_cube import TEST_PUZZLE_CUBE_SPEC
from instant_insanity.animators.cube_animators import CubeRigidMotionAnimator
from instant_insanity.scenes.coordinate_grid import GridMixin


class TestCubeRigidMotionAnimator(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        camera_z: float = 8.0
        viewpoint: np.ndarray = np.array([5, 5, 20], dtype=np.float64)
        projection: Projection = PerspectiveProjection(viewpoint, camera_z=camera_z)

        cube_spec: PuzzleCubeSpec = TEST_PUZZLE_CUBE_SPEC
        cube: ThreeDPuzzleCube = ThreeDPuzzleCube(projection, cube_spec)

        # set up the rigid motion animation
        rotation: Vector = ORIGIN
        translation: Vector = 7 * LEFT  # + DOWN
        animator: CubeRigidMotionAnimator = CubeRigidMotionAnimator(cube, rotation, translation)

        # draw the outlines of the front and right faces at some points in the animation
        names: list[FaceName] = [FaceName.FRONT, FaceName.RIGHT]
        colours: list[ManimColor] = [BLUE, GREEN]
        alpha: float
        for alpha in [0.0, 0.5, 1.0]:
            animator.interpolate(alpha)
            alpha_id_to_scene_polygon: SortedPolygonIdToPolygonMapping = cube.id_to_scene_polygon
            name: FaceName
            colour: ManimColor
            for name, colour in zip(names, colours):
                polygon_id: PolygonId = ThreeDPuzzleCube.name_to_id(name)
                alpha_polygon: Polygon = alpha_id_to_scene_polygon[polygon_id]
                alpha_vertices: np.ndarray = alpha_polygon.get_vertices()
                alpha_polygon_outline: Polygon = Polygon(*alpha_vertices,
                                                         stroke_color=colour,
                                                         joint_type=LineJointType.ROUND)
                self.add(alpha_polygon_outline)
        self.wait(1.0)

        # move the cube to the animation start
        animator.interpolate(0.0)
        self.play(FadeIn(cube))
        self.wait(1.0)

        # self.remove(three_d_puzzle_cube)
        cube.remove(*cube.submobjects)
        #self.wait(1.0)

        # animate movement of the cube to the left
        # updater: Updater = animator.mk_updater()
        # cube.add_updater(updater)
        # tracker: ValueTracker = cube.tracker
        # self.play(tracker.animate.set_value(1.0), run_time=3.0)
        # cube.remove_updater(updater)
        animator.play(self, alpha=0.75, run_time=3.0)
        cube.remove(*cube.submobjects)

        animator.play(self, alpha=0.25, run_time=2.0)
        cube.remove(*cube.submobjects)

        animator.play(self, alpha=0.0, run_time=1.0)
        cube.remove(*cube.submobjects)

        # reset and clear
        animator.interpolate(0.0)
        #cube.tracker.set_value(0.0)
        self.wait(1.0)
        cube.remove(*cube.submobjects)

        # rotate the cube.
        rotation = RIGHT * 2 * PI
        translation = ORIGIN
        animator = CubeRigidMotionAnimator(cube, rotation, translation)
        animator.play(self, run_time=4.0)

        self.play(FadeOut(cube))
        self.wait(1.0)
        cube.remove(*cube.submobjects)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = TestCubeRigidMotionAnimator()
        scene.render()
