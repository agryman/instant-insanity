from manim import *

from instant_insanity.core.cube import FaceName, FACE_NAME_TO_VERTICES
from instant_insanity.core.projection import PerspectiveProjection
from instant_insanity.core.puzzle import PuzzleCubeSpec
from instant_insanity.manim_scenes.coloured_cube import TEST_PUZZLE_CUBE_SPEC
from instant_insanity.manim_scenes.graph_theory.three_d_puzzle_cube import ThreeDPuzzleCube, CubeRigidMotionAnimation


def test_three_d_puzzle_cube():
    # create a perspective projection
    camera_z: float = 2.0
    viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
    projection: PerspectiveProjection = PerspectiveProjection(viewpoint, camera_z=camera_z)

    # use the colours from the test cube
    cube_spec: PuzzleCubeSpec = TEST_PUZZLE_CUBE_SPEC
    three_d_puzzle_cube: ThreeDPuzzleCube = ThreeDPuzzleCube(projection, cube_spec)

    polygon_dict = three_d_puzzle_cube.polygon_dict
    sorted_faces = list(polygon_dict.keys())

    # the front, right, and top faces should be visible

    front = sorted_faces.index(FaceName.FRONT)
    back = sorted_faces.index(FaceName.BACK)
    assert back < front

    right = sorted_faces.index(FaceName.RIGHT)
    left = sorted_faces.index(FaceName.LEFT)
    assert left < right

    top = sorted_faces.index(FaceName.TOP)
    bottom = sorted_faces.index(FaceName.BOTTOM)
    assert bottom < top

def test_translation():
    camera_z: float = 2.0
    viewpoint: np.ndarray = np.array([0, 0, 6], dtype=np.float64)
    projection: PerspectiveProjection = PerspectiveProjection(viewpoint, camera_z=camera_z)

    # use the colours from the test cube
    cube_spec: PuzzleCubeSpec = TEST_PUZZLE_CUBE_SPEC
    three_d_puzzle_cube: ThreeDPuzzleCube = ThreeDPuzzleCube(projection, cube_spec)
    polygons_before = three_d_puzzle_cube.polygon_dict.copy()
    right_before = polygons_before[FaceName.RIGHT]
    actual_vertices_before = right_before.get_vertices()

    model_vertices_before = FACE_NAME_TO_VERTICES[FaceName.RIGHT]
    expected_vertices_before = projection.project_points(model_vertices_before)
    assert np.allclose(actual_vertices_before, expected_vertices_before)

    # move the cube to the left
    rotation: np.ndarray = ORIGIN
    translation: np.ndarray = 7 * LEFT
    animation: Animation = CubeRigidMotionAnimation(three_d_puzzle_cube, rotation, translation)
    animation.interpolate_mobject(1.0)

    polygons_after = three_d_puzzle_cube.polygon_dict
    right_after = polygons_after[FaceName.RIGHT]
    actual_vertices_after = right_after.get_vertices()

    model_vertices_after = FACE_NAME_TO_VERTICES[FaceName.RIGHT] + translation
    expected_vertices_after = projection.project_points(model_vertices_after)
    assert np.allclose(actual_vertices_after, expected_vertices_after)

    assert len(polygons_before) == len(polygons_after)
