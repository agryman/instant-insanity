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
import numpy as np
from scipy.spatial.transform import Rotation as R
from manim import *

from instant_insanity.core.cube import FaceName, FACE_NAME_TO_VERTICES
from instant_insanity.core.depth_sort import DepthSort
from instant_insanity.core.projection import PerspectiveProjection
from instant_insanity.core.puzzle import PuzzleCubeSpec, PuzzleCube, FaceColour
from instant_insanity.manim_scenes.coloured_cube import TEST_PUZZLE_CUBE_SPEC, MANIM_COLOUR_MAP


def transform_vertices(rotation, translation, vertices) -> np.ndarray:
    """
    Transform the vertices by applying a rotation followed by a translation.

    Let R be a rotation, let T be a translation, and let V be a vertex.
    The transformed vertex is R(V) + T.

    Args:
        rotation: a rotation 3-vector.
        translation: a translation 3-vector.
        vertices: a matrix of n 3-vectors.

    Returns:
        the matrix of n transformed 3-vectors.
    """
    rot = R.from_rotvec(rotation)
    return rot.apply(vertices) + translation


class ProjectedCube(Scene):
    def construct(self):
        # create a perspective projection
        camera_z: float = 0
        viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
        projection: PerspectiveProjection = PerspectiveProjection(camera_z, viewpoint)
        depth_sorter: DepthSort = DepthSort(projection)

        # use the colours from the test cube
        cube_spec: PuzzleCubeSpec = TEST_PUZZLE_CUBE_SPEC
        puzzle_cube: PuzzleCube = PuzzleCube(cube_spec)

        def mk_polygons(alpha: float) -> list[Polygon]:
            """Make the cube corresponding the value of alpha in the animation."""
            translation_vector: np.ndarray = np.array([2, 3, -4], dtype=np.float64)
            alpha_translation: np.ndarray = 0.0 * translation_vector

            rotation_vector: np.ndarray = np.array([1.0, 0.0, 0.0], dtype=np.float64)
            alpha_rotation: np.ndarray = alpha * rotation_vector * 2.0 * np.pi

            # create a dict of the transformed vertices
            transformed_vertices_dict: dict[str, np.ndarray] = {}
            name: FaceName
            for name in FaceName:
                model_vertices: np.ndarray = FACE_NAME_TO_VERTICES[name]
                transformed_vertices: np.ndarray = transform_vertices(alpha_rotation, alpha_translation, model_vertices)
                transformed_vertices_dict[name.value] = transformed_vertices

            # project the transformed vertices onto the scene and depth-sort them
            sorted_names: list[str]
            scene_vertices_dict: dict[str, np.ndarray]
            sorted_names, scene_vertices_dict = depth_sorter.depth_sort(transformed_vertices_dict)

            # create a Manim Polygon for each projected face of the cube
            polygon_list: list[Polygon] = []
            name_str: str
            for name_str in sorted_names:
                # create a Manim Polygon
                scene_vertices: np.ndarray = scene_vertices_dict[name_str]
                name = FaceName(name_str)
                colour_name: FaceColour = puzzle_cube.faces[name]
                colour: ManimColor = MANIM_COLOUR_MAP[colour_name]
                polygon: Polygon = Polygon(
                    *scene_vertices,
                    fill_color=colour,
                    fill_opacity=1.0,
                    stroke_color=BLACK,
                    stroke_width=1.0
                )
                polygon_list.append(polygon)

            return polygon_list

        # we are going to create new polygon mobjects during the animation
        # so put them in a VGroup which will be updated for each frame
        polygons: list[Polygon] = mk_polygons(0.0)
        vgroup: VGroup = VGroup(*polygons)
        self.add(vgroup)
        self.wait(1.0)

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
        self.play(tracker.animate.set_value(1.0), run_time=4.0)

        self.wait(1.0)

my_config: dict = {
    "background_color": WHITE,
    "disable_caching": True,
    "preview": True
}

with tempconfig(my_config):
    scene = ProjectedCube()
    scene.render()
