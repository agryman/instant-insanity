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
from instant_insanity.core.projection import PerspectiveProjection

class ThreeDSceneEmulation(Scene):
    def construct(self):

        # create a perspective projection
        camera_z: float = 0
        viewpoint: np.ndarray = np.array([0, 0, 10], dtype=np.float64)
        projection: PerspectiveProjection = PerspectiveProjection(camera_z, viewpoint)

        # create a triangle
        model_vertices: np.ndarray = np.array([
            [0, 0, -1],
            [1, 0, -2],
            [1, 1, -3]
        ], dtype=np.float64)

        translation_vector: np.ndarray = np.array([2, 3, -4], dtype=np.float64)

        def mk_triangle(alpha: float) -> Polygon:
            """Makes the triangle corresponding to the animation parameter alpha"""

            translated_vertices: np.ndarray = model_vertices + alpha * translation_vector

            # project the vertices
            scene_vertices: np.ndarray = np.array([
                projection.project_point(vertex) for vertex in translated_vertices
            ])

            # create a manim polygon
            triangle: Polygon = Polygon(
                *scene_vertices,
                fill_color=RED,
                stroke_color=BLACK,
                stroke_width=2,
                fill_opacity=1)

            return triangle

        # we are going to create new triangle objects during the animation
        # so put them in a VGroup which will be updated for each frame
        polygons: VGroup = VGroup(mk_triangle(0.0))

        # the tracker parameterizes the animation
        tracker: ValueTracker = ValueTracker(0)

        def updater(vgroup: Mobject) -> Mobject:
            vgroup.remove(*vgroup.submobjects)
            alpha: float = tracker.get_value()
            triangle: Polygon = mk_triangle(alpha)
            vgroup.add(triangle)
            return vgroup

        self.add(polygons)
        self.wait(2.0)

        polygons.add_updater(updater)
        polygons.remove(*polygons.submobjects)

        self.play(tracker.animate.set_value(1.0), run_time=2)
        self.wait(2.0)


my_config: dict = {
    "background_color": WHITE,
    "preview": True
}

with tempconfig(my_config):
    scene = ThreeDSceneEmulation()
    scene.render()
