from manim import *

from instant_insanity.animators.cube_animators import CubeRigidMotionAnimorph
from instant_insanity.core.cube import FacePlane, FACE_PLANE_TO_VERTEX_PATH
from instant_insanity.core.geometry_types import SortedPolygonKeyToPolygonMapping
from instant_insanity.core.projection import PerspectiveProjection
from instant_insanity.core.puzzle import PuzzleCubeSpec, FaceLabel
from instant_insanity.mobjects.coloured_cube import TEST_PUZZLE_CUBE_SPEC
from instant_insanity.mobjects.puzzle_cube_3d import PuzzleCube3D

FRONT_FACE: FaceLabel = FaceLabel.X
BACK_FACE: FaceLabel = FaceLabel.X_PRIME
RIGHT_FACE: FaceLabel = FaceLabel.Y
LEFT_FACE: FaceLabel = FaceLabel.Y_PRIME
TOP_FACE: FaceLabel = FaceLabel.Z
BOTTOM_FACE: FaceLabel = FaceLabel.Z_PRIME


def test_three_d_puzzle_cube():
    # create a perspective projection
    camera_z: float = 2.0
    viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
    projection: PerspectiveProjection = PerspectiveProjection(viewpoint, camera_z=camera_z)

    # use the colours from the test cube
    cube_spec: PuzzleCubeSpec = TEST_PUZZLE_CUBE_SPEC
    three_d_puzzle_cube: PuzzleCube3D = PuzzleCube3D(projection, cube_spec)

    key_to_scene_polygon: SortedPolygonKeyToPolygonMapping[FaceLabel] = three_d_puzzle_cube.key_to_scene_polygon
    sorted_keys: list[FaceLabel] = list(key_to_scene_polygon.keys())

    # the front, right, and top faces should be visible

    front: int = sorted_keys.index(FRONT_FACE)
    back: int = sorted_keys.index(BACK_FACE)
    assert back < front

    right: int = sorted_keys.index(RIGHT_FACE)
    left: int = sorted_keys.index(LEFT_FACE)
    assert left < right

    top: int = sorted_keys.index(TOP_FACE)
    bottom: int = sorted_keys.index(BOTTOM_FACE)
    assert bottom < top

def test_translation():
    camera_z: float = 2.0
    viewpoint: np.ndarray = np.array([0, 0, 6], dtype=np.float64)
    projection: PerspectiveProjection = PerspectiveProjection(viewpoint, camera_z=camera_z)

    # use the colours from the test cube
    cube_spec: PuzzleCubeSpec = TEST_PUZZLE_CUBE_SPEC
    cube: PuzzleCube3D = PuzzleCube3D(projection, cube_spec)
    key_to_scene_polygon_before = cube.key_to_scene_polygon.copy()
    right_polygon_before = key_to_scene_polygon_before[RIGHT_FACE]
    actual_vertices_before = right_polygon_before.get_vertices()

    model_vertices_before = FACE_PLANE_TO_VERTEX_PATH[FacePlane.RIGHT]
    expected_vertices_before = projection.project_points(model_vertices_before)
    assert np.allclose(actual_vertices_before, expected_vertices_before)

    # move the cube to the left
    rotation: np.ndarray = ORIGIN
    translation: np.ndarray = 7 * LEFT
    animorph: CubeRigidMotionAnimorph = CubeRigidMotionAnimorph(cube, rotation, translation)
    animorph.morph_to(1.0)

    key_to_scene_polygon_after = cube.key_to_scene_polygon
    right_polygon_after = key_to_scene_polygon_after[RIGHT_FACE]
    actual_vertices_after = right_polygon_after.get_vertices()

    model_vertices_after = FACE_PLANE_TO_VERTEX_PATH[FacePlane.RIGHT] + translation
    expected_vertices_after = projection.project_points(model_vertices_after)
    assert np.allclose(actual_vertices_after, expected_vertices_after)

    assert len(key_to_scene_polygon_before) == len(key_to_scene_polygon_after)

def test_polygon_keys():
    # Test that all face labels are valid keys
    camera_z: float = 2.0
    viewpoint: np.ndarray = np.array([0, 0, 6], dtype=np.float64)
    projection: PerspectiveProjection = PerspectiveProjection(viewpoint, camera_z=camera_z)
    cube_spec: PuzzleCubeSpec = TEST_PUZZLE_CUBE_SPEC
    cube: PuzzleCube3D = PuzzleCube3D(projection, cube_spec)
    
    # Verify all face labels are present as keys
    for face_label in FaceLabel:
        assert face_label in cube.key_to_scene_polygon
        polygon_settings = cube.get_polygon_settings(face_label)
        assert 'fill_color' in polygon_settings
