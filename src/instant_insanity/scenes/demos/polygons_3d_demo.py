import numpy as np
from isosurfaces.isosurface import TETRAHEDRON_TABLE

from manim import (Scene, tempconfig, ORIGIN, RIGHT, LEFT, UP, OUT,
                   RED, GREEN, BLUE, YELLOW, BLACK, PI, ManimColor, PURPLE)

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.geometry_types import (Vertex, VertexPath, PolygonId, PolygonIdToVertexPathMapping,
                                                  as_vertex, as_vertex_path)
from instant_insanity.core.projection import Projection, PerspectiveProjection
from instant_insanity.core.transformation import transform_vertex_path
from instant_insanity.mobjects.polygons_3d import Polygons3D
from instant_insanity.scenes.coordinate_grid import GridMixin

# create the vertex paths for a tetrahedron
O: Vertex = as_vertex(ORIGIN)
X: Vertex = as_vertex(RIGHT)
Y: Vertex = as_vertex(UP)
Z: Vertex = as_vertex(OUT)

OXY: VertexPath = as_vertex_path([O, X, Y])
OXZ: VertexPath = as_vertex_path([O, X, Z])
OYZ: VertexPath = as_vertex_path([O, Y, Z])
XYZ: VertexPath = as_vertex_path([X, Y, Z])

OXY_ID: PolygonId = PolygonId('oxy')
OXZ_ID: PolygonId = PolygonId('oxz')
OYZ_ID: PolygonId = PolygonId('oyz')
XYZ_ID: PolygonId = PolygonId('xyz')

TETRAHEDRON_ID_TO_MODEL_PATH_0: PolygonIdToVertexPathMapping = {
    OXY_ID: OXY,
    OXZ_ID: OXZ,
    OYZ_ID: OYZ,
    XYZ_ID: XYZ,
}

TETRAHEDRON_ID_TO_COLOUR: dict[PolygonId, ManimColor] = {
    OXY_ID: RED,
    OXZ_ID: GREEN,
    OYZ_ID: BLUE,
    XYZ_ID: PURPLE,
}

DEFAULT_TETRAHEDRON_SETTINGS: dict = {
    'fill_opacity': 1.0,
    'fill_color': YELLOW,
    'stroke_width': 1.0,
    'stroke_color': BLACK
}


class Tetrahedron3D(Polygons3D):
    def __init__(self,
                 projection: Projection,
                 id_to_model_path_0: PolygonIdToVertexPathMapping) -> None:
        super().__init__(projection, id_to_model_path_0)

    def get_polygon_settings(self, polygon_id: PolygonId) -> dict:
        polygon_settings: dict = DEFAULT_TETRAHEDRON_SETTINGS.copy()
        colour: ManimColor = TETRAHEDRON_ID_TO_COLOUR[polygon_id]
        polygon_settings['fill_color'] = colour

        return polygon_settings


class Polygons3DDemo(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        # create a projection
        camera_z: float = 2.0
        viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
        projection: Projection = PerspectiveProjection(viewpoint, camera_z=camera_z)

        tetrahedron: Tetrahedron3D = Tetrahedron3D(projection, TETRAHEDRON_ID_TO_MODEL_PATH_0)

        self.add(tetrahedron)
        self.wait()


        self.remove(tetrahedron)
        self.wait()

        # transform the model paths and update the polygons object
        rotation: np.ndarray = np.array(RIGHT * PI / 2.0, dtype=np.float64)
        translation: np.ndarray = np.array(LEFT * 4, dtype=np.float64)
        id_to_model_path: PolygonIdToVertexPathMapping = {
            polygon_id: transform_vertex_path(rotation, translation, model_path)
            for polygon_id, model_path in tetrahedron.id_to_model_path_0.items()
        }
        tetrahedron.set_id_to_model_path(id_to_model_path)

        self.add(tetrahedron)
        self.wait()


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = Polygons3DDemo()
        scene.render()
