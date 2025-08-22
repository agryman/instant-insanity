import numpy as np

from manim import (Scene, tempconfig, ORIGIN, RIGHT, LEFT, UP, OUT,
                   RED, GREEN, BLUE, YELLOW, BLACK, PI, ManimColor, PURPLE)

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.geometry_types import (Vertex, VertexPath, PolygonId, PolygonIdToVertexPathMapping,
                                                  as_vertex, as_vertex_path)
from instant_insanity.core.projection import Projection, PerspectiveProjection
from instant_insanity.core.transformation import transform_vertex_path
from instant_insanity.mobjects.three_d_polygons import ThreeDPolygons
from instant_insanity.scenes.coordinate_grid import GridMixin


class ThreeDPolygonsDemo(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        # create a projection
        camera_z: float = 2.0
        viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
        projection: Projection = PerspectiveProjection(viewpoint, camera_z=camera_z)

        # create the vertex paths for a tetrahedron
        o: Vertex = as_vertex(ORIGIN)
        x: Vertex = as_vertex(RIGHT)
        y: Vertex = as_vertex(UP)
        z: Vertex = as_vertex(OUT)

        oxy: VertexPath = as_vertex_path([o, x, y])
        oxz: VertexPath = as_vertex_path([o, x, z])
        oyz: VertexPath = as_vertex_path([o, y, z])
        xyz: VertexPath = as_vertex_path([x, y, z])

        oxy_id: PolygonId = PolygonId('oxy')
        oxz_id: PolygonId = PolygonId('oxz')
        oyz_id: PolygonId = PolygonId('oyz')
        xyz_id: PolygonId = PolygonId('xyz')

        id_to_model_path_0: PolygonIdToVertexPathMapping = {
            oxy_id: oxy,
            oxz_id: oxz,
            oyz_id: oyz,
            xyz_id: xyz,
        }

        id_to_colour: dict[PolygonId, ManimColor] = {
            oxy_id: RED,
            oxz_id: GREEN,
            oyz_id: BLUE,
            xyz_id: PURPLE,
        }

        polygon_defaults: dict = {
            'fill_opacity': 1.0,
            'fill_color': YELLOW,
            'stroke_width': 1.0,
            'stroke_color': BLACK
        }
        tetrahedron: ThreeDPolygons = ThreeDPolygons(projection,
                                                  id_to_model_path_0,
                                                  **polygon_defaults)

        def set_fill_color():
            for polygon_id, colour in id_to_colour.items():
                tetrahedron.id_to_scene_polygon[polygon_id].set_fill(colour)

        set_fill_color()

        # Have the faces been added to the tetrahedron? - NO!
        # TODO: the ThreeDPolygons constructor should add the Polygon objects to the VGroup
        self.add(*tetrahedron.id_to_scene_polygon.values())
        self.wait()

        self.remove(*tetrahedron.id_to_scene_polygon.values())
        self.wait()

        # transform the model paths and update the polygons object
        rotation: np.ndarray = np.array(RIGHT * PI / 2.0, dtype=np.float64)
        translation: np.ndarray = np.array(LEFT * 4, dtype=np.float64)
        id_to_model_path: PolygonIdToVertexPathMapping = {
            polygon_id : transform_vertex_path(rotation, translation, id_to_model_path_0[polygon_id])
            for polygon_id in id_to_model_path_0.keys()
        }
        tetrahedron.update_polygons(id_to_model_path, **polygon_defaults)
        set_fill_color()

        self.add(*tetrahedron.id_to_scene_polygon.values())
        self.wait()

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = ThreeDPolygonsDemo()
        scene.render()
