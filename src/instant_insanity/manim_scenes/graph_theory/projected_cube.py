"""
This scene displays a projected cube.
The cube is first constructed in 3D model space where it may be
rotated, translated, unfolded, exploded, or otherwise animated.
The result is a set of 3D, convex, planar polygons.
This set is then projected onto the 2D scene space.
Next, the polygons are sorted into the correct depth order
so that when they are drawn, those in front will be drawn
after those behind.
Finally, the polygons are converted into Manim Polygons
and added to the scene.
"""

from manim import *

from instant_insanity.core.cube import FaceName, FACE_NAME_TO_VERTICES
from instant_insanity.core.projection import PerspectiveProjection
from instant_insanity.core.puzzle import PuzzleCubeSpec, PuzzleCube, FaceColour
from instant_insanity.manim_scenes.coloured_cube import TEST_PUZZLE_CUBE_SPEC, MANIM_COLOUR_MAP


class ProjectedCube(Scene):
    def construct(self):
        # create a perspective projection
        camera_z: float = 0
        viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
        projection: PerspectiveProjection = PerspectiveProjection(camera_z, viewpoint)

        # use the colours from the test cube
        cube_spec: PuzzleCubeSpec = TEST_PUZZLE_CUBE_SPEC
        puzzle_cube: PuzzleCube = PuzzleCube(cube_spec)

        # create a Polygon for each projected face of the standard cube
        face_name_to_polygon: dict[FaceName, Polygon] = {}
        for name in FaceName:
            model_vertices: np.ndarray = FACE_NAME_TO_VERTICES[name]
            vertices: np.ndarray = projection.project_points(model_vertices)
            colour_name: FaceColour = puzzle_cube.faces[name]
            colour: ManimColor = MANIM_COLOUR_MAP[colour_name]
            polygon: Polygon = Polygon(*vertices, fill_color=colour,
                                       fill_opacity=1.0, stroke_color=BLACK, stroke_width=1.0)
            face_name_to_polygon[name] = polygon

        # create a directed graph whose nodes are the polygons
        # and whose edges are the constraints that node x is behind node y

        cube: VGroup = VGroup(
            face_name_to_polygon[FaceName.BACK],
            face_name_to_polygon[FaceName.LEFT],
            face_name_to_polygon[FaceName.BOTTOM],
            face_name_to_polygon[FaceName.RIGHT],
            face_name_to_polygon[FaceName.TOP],
            face_name_to_polygon[FaceName.FRONT])
        self.add(cube)

my_config: dict = {
    "background_color": WHITE,
    "preview": True
}

with tempconfig(my_config):
    scene = ProjectedCube()
    scene.render()
