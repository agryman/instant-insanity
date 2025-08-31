import numpy as np

from manim import Polygon, ManimColor, GREEN, BLUE, Scene, ORIGIN, LEFT, tempconfig, RIGHT, PI, LineJointType, FadeIn, \
    FadeOut, ValueTracker, UP

from instant_insanity.animators.animorph import Updater
from instant_insanity.animators.polygons_3d_animator import RigidMotionPolygons3DAnimorph, Polygons3DAnimorph
from instant_insanity.core.geometry_types import Vector, PolygonId, SortedPolygonIdToPolygonMapping
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FacePlane
from instant_insanity.core.projection import Projection, PerspectiveProjection
from instant_insanity.core.puzzle import PuzzleCubeSpec
from instant_insanity.mobjects.puzzle_cube_3d import PuzzleCube3D
from instant_insanity.scenes.coloured_cube import TEST_PUZZLE_CUBE_SPEC
from instant_insanity.animators.cube_animators import CubeRigidMotionAnimorph
from instant_insanity.scenes.coordinate_grid import GridMixin


class CubeRigidMotionAnimorphDemo(GridMixin, Scene):
    def construct(self):
        self.add_grid(False)

        camera_z: float = 8.0
        viewpoint: np.ndarray = np.array([5, 5, 20], dtype=np.float64)
        projection: Projection = PerspectiveProjection(viewpoint, camera_z=camera_z)

        cube_spec: PuzzleCubeSpec = TEST_PUZZLE_CUBE_SPEC
        cube: PuzzleCube3D = PuzzleCube3D(projection, cube_spec)

        # set up the rigid motion animation
        rotation: Vector = ORIGIN
        translation: Vector = 7 * LEFT  # + DOWN
        animorph: CubeRigidMotionAnimorph = CubeRigidMotionAnimorph(cube, rotation, translation)

        # draw the outlines of the front and right faces at some points in the animation
        names: list[FacePlane] = [FacePlane.FRONT, FacePlane.RIGHT]
        colours: list[ManimColor] = [BLUE, GREEN]
        alpha: float
        for alpha in [0.0, 0.5, 1.0]:
            animorph.morph_to(alpha)
            id_to_scene_polygon: SortedPolygonIdToPolygonMapping = cube.id_to_scene_polygon
            name: FacePlane
            colour: ManimColor
            for name, colour in zip(names, colours):
                polygon_id: PolygonId = PuzzleCube3D.name_to_id(name)
                polygon: Polygon = id_to_scene_polygon[polygon_id]
                vertices: np.ndarray = polygon.get_vertices()
                alpha_polygon_outline: Polygon = Polygon(*vertices,
                                                         stroke_color=colour,
                                                         joint_type=LineJointType.ROUND)
                self.add(alpha_polygon_outline)
        self.wait()

        # move the cube to the animation start
        animorph.morph_to(0.0)
        self.play(FadeIn(cube))
        self.wait()

        alpha_tracker: ValueTracker = ValueTracker(0.0)
        updater: Updater = lambda m: animorph.morph_to(alpha_tracker.get_value())
        cube.add_updater(updater)
        for end_alpha in [0.75, 0.25, 0.0]:
            cube.conceal_polygons()
            self.play(alpha_tracker.animate.set_value(end_alpha))
            self.wait()
        cube.remove_updater(updater)

        # reset and clear
        animorph.morph_to(0.0)
        self.wait()

        # rotate the cube.
        rotation = RIGHT * 2 * PI
        translation = ORIGIN
        animorph = CubeRigidMotionAnimorph(cube, rotation, translation)
        cube.conceal_polygons()
        animorph.play(self, run_time=2.0)

        # rotate again using a different animorph
        rotation = UP * 2 * PI
        translation = ORIGIN
        moveable_polygon_ids: set[PolygonId] = set(cube.id_to_scene_polygon.keys())
        p3danimorph: Polygons3DAnimorph
        p3danimorph = RigidMotionPolygons3DAnimorph(cube,
                                                 rotation,
                                                 translation,
                                                 moveable_polygon_ids)
        cube.conceal_polygons()
        p3danimorph.play(self, run_time=2.0)

        self.play(FadeOut(cube))
        self.wait()

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = CubeRigidMotionAnimorphDemo()
        scene.render()
