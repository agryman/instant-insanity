"""
This module emulates a 3d scene by using a 2d scene together with
a transformation that projects the 3d model space onto the 2d scene space.
The 3d scene consists of a set of convex, planar polygons.
They are projected to 2d polygons and then sorted into an order
where overlapping projections are drawn correctly.
This means that if polygon A appears to be behind polygon B,
then polygon A is rendered before polygon B.
"""

import numpy as np
from manim import *
from manim.typing import Vector3D, Point3D_Array
from sympy import Point3D

from instant_insanity.core.projection import PerspectiveProjection

class ThreeDSceneEmulation(Scene):
    def construct(self):

        # create a perspective projection
        camera_z: float = 0
        #viewpoint: np.ndarray = np.array([0, 0, 10], dtype=np.float64)
        viewpoint: Point3D = np.array([2, 2, 6], dtype=np.float64)
        projection: PerspectiveProjection = PerspectiveProjection(viewpoint, camera_z=camera_z)

        def mk_polygons(alpha: float) -> list[Polygon]:
            """Makes the triangle corresponding to the animation parameter alpha"""

            translation_vector: Vector3D = np.array([2, 3, -4], dtype=np.float64)
            alpha_translation: Vector3D = alpha * translation_vector

            # create a triangle
            model_vertices: Point3D_Array = np.array([
                [0, 0, -1],
                [1, 0, -2],
                [1, 1, -3]
            ], dtype=np.float64)
            transformed_vertices: Point3D_Array = model_vertices + alpha_translation

            # project the vertices
            scene_vertices: Point3D_Array = projection.project_points(transformed_vertices)

            # create a manim polygon
            polygon: Polygon = Polygon(
                *scene_vertices,
                fill_color=RED,
                fill_opacity=1.0,
                stroke_color=BLACK,
                stroke_width=2.0
            )

            return [polygon]

        # we are going to create new polygon mobjects during the animation
        # so put them in a VGroup which will be updated for each frame
        polygons: list[Polygon] = mk_polygons(0.0)
        vgroup: VGroup = VGroup(*polygons)
        self.add(vgroup)
        elapsed_time: float = 1.0
        self.wait(elapsed_time)

        vgroup.remove(*vgroup.submobjects)

        # the tracker parameterizes the animation
        tracker: ValueTracker = ValueTracker(0)

        def updater(vgroup: Mobject) -> Mobject:
            alpha: float = tracker.get_value()
            polygons: list[Polygon] = mk_polygons(alpha)
            vgroup.remove(*vgroup.submobjects)
            vgroup.add(*polygons)
            return vgroup

        vgroup.add_updater(updater)
        self.play(tracker.animate.set_value(1.0), run_time=elapsed_time)

        self.wait(elapsed_time)


my_config: dict = {
    "background_color": WHITE,
    "disable_caching": True,
    "preview": True
}

with tempconfig(my_config):
    scene = ThreeDSceneEmulation()
    scene.render()
