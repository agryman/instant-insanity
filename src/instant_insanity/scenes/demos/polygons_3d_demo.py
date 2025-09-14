import numpy as np

from manim import (Scene, tempconfig, ORIGIN, RIGHT, LEFT, UP, OUT,
                   RED, GREEN, BLUE, YELLOW, BLACK, PI, ManimColor, PURPLE)

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.geometry_types import (Vertex, VertexPath, PolygonKeyToVertexPathMapping,
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

OXY_FACE: str = 'oxy'
OXZ_FACE: str = 'oxz'
OYZ_FACE: str = 'oyz'
XYZ_FACE: str = 'xyz'

TETRAHEDRON_KEY_TO_MODEL_PATH_0: PolygonKeyToVertexPathMapping[str] = {
    OXY_FACE: OXY,
    OXZ_FACE: OXZ,
    OYZ_FACE: OYZ,
    XYZ_FACE: XYZ,
}

TETRAHEDRON_KEY_TO_COLOUR: dict[str, ManimColor] = {
    OXY_FACE: RED,
    OXZ_FACE: GREEN,
    OYZ_FACE: BLUE,
    XYZ_FACE: PURPLE,
}

DEFAULT_TETRAHEDRON_SETTINGS: dict = {
    'fill_opacity': 1.0,
    'fill_color': YELLOW,
    'stroke_width': 1.0,
    'stroke_color': BLACK
}


class Tetrahedron3D(Polygons3D[str]):
    def __init__(self,
                 projection: Projection,
                 key_to_model_path_0: PolygonKeyToVertexPathMapping[str]) -> None:
        super().__init__(projection, key_to_model_path_0)

    def get_polygon_settings(self, face_key: str) -> dict:
        polygon_settings: dict = DEFAULT_TETRAHEDRON_SETTINGS.copy()
        colour: ManimColor = TETRAHEDRON_KEY_TO_COLOUR[face_key]
        polygon_settings['fill_color'] = colour

        return polygon_settings


class Polygons3DDemo(GridMixin, Scene):
    def construct(self):
        self.add_grid(True)

        # create a projection
        camera_z: float = 2.0
        viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
        projection: Projection = PerspectiveProjection(viewpoint, camera_z=camera_z)

        tetrahedron: Tetrahedron3D = Tetrahedron3D(projection, TETRAHEDRON_KEY_TO_MODEL_PATH_0)

        self.add(tetrahedron)
        self.wait()


        self.remove(tetrahedron)
        self.wait()

        # transform the model paths and update the polygons object
        rotation: np.ndarray = np.array(RIGHT * PI / 2.0, dtype=np.float64)
        translation: np.ndarray = np.array(LEFT * 4, dtype=np.float64)
        key_to_model_path: PolygonKeyToVertexPathMapping[str] = {
            face_key: transform_vertex_path(rotation, translation, model_path)
            for face_key, model_path in tetrahedron.key_to_model_path_0.items()
        }
        tetrahedron.set_key_to_model_path(key_to_model_path)

        self.add(tetrahedron)
        self.wait()


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = Polygons3DDemo()
        scene.render()
