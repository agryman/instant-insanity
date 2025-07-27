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
        # create a triangle
        model_vertices: np.ndarray = np.array([
            [0, 0, -1],
            [1, 0, -2],
            [1, 1, -3]
        ], dtype=np.float64)

        # create a perspective projection
        camera_z: float = 0
        viewpoint: np.ndarray = np.array([0, 0, 10], dtype=np.float64)
        projection: PerspectiveProjection = PerspectiveProjection(camera_z, viewpoint)

        # project the vertices
        scene_vertices: np.ndarray = np.array([
            projection.project_point(model_vertex) for model_vertex in model_vertices
        ])

        # create a manim polygon
        triangle = Polygon(*scene_vertices, fill_color=RED, stroke_color=BLACK, stroke_width=2, fill_opacity=1)
        self.add(triangle)

my_config: dict = {
    "background_color": WHITE,
    "preview": True
}

with tempconfig(my_config):
    scene = ThreeDSceneEmulation()
    scene.render()
