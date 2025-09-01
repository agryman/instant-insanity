from manim import *

from instant_insanity.animators.cube_animators import CubeRigidMotionAnimorph
from instant_insanity.core.cube import FacePlane, FACE_PLANE_TO_VERTEX_PATH
from instant_insanity.core.geometry_types import SortedPolygonIdToPolygonMapping, PolygonId
from instant_insanity.core.projection import PerspectiveProjection
from instant_insanity.core.puzzle import PuzzleCubeSpec, FaceLabel
from instant_insanity.mobjects.coloured_cube import TEST_PUZZLE_CUBE_SPEC
from instant_insanity.mobjects.puzzle_cube_3d import PuzzleCube3D

FRONT_ID: PolygonId = PuzzleCube3D.name_to_id(FaceLabel.X)
BACK_ID: PolygonId = PuzzleCube3D.name_to_id(FaceLabel.X_PRIME)
RIGHT_ID: PolygonId = PuzzleCube3D.name_to_id(FaceLabel.Y)
LEFT_ID: PolygonId = PuzzleCube3D.name_to_id(FaceLabel.Y_PRIME)
TOP_ID: PolygonId = PuzzleCube3D.name_to_id(FaceLabel.Z)
BOTTOM_ID: PolygonId = PuzzleCube3D.name_to_id(FaceLabel.Z_PRIME)


def test_three_d_puzzle_cube():
    # create a perspective projection
    camera_z: float = 2.0
    viewpoint: np.ndarray = np.array([2, 2, 6], dtype=np.float64)
    projection: PerspectiveProjection = PerspectiveProjection(viewpoint, camera_z=camera_z)

    # use the colours from the test cube
    cube_spec: PuzzleCubeSpec = TEST_PUZZLE_CUBE_SPEC
    three_d_puzzle_cube: PuzzleCube3D = PuzzleCube3D(projection, cube_spec)

    id_to_scene_polygon: SortedPolygonIdToPolygonMapping = three_d_puzzle_cube.id_to_scene_polygon
    sorted_ids: list[PolygonId] = list(id_to_scene_polygon.keys())

    # the front, right, and top faces should be visible

    front: int = sorted_ids.index(FRONT_ID)
    back: int = sorted_ids.index(BACK_ID)
    assert back < front

    right: int = sorted_ids.index(RIGHT_ID)
    left: int = sorted_ids.index(LEFT_ID)
    assert left < right

    top: int = sorted_ids.index(TOP_ID)
    bottom: int = sorted_ids.index(BOTTOM_ID)
    assert bottom < top

def test_translation():
    camera_z: float = 2.0
    viewpoint: np.ndarray = np.array([0, 0, 6], dtype=np.float64)
    projection: PerspectiveProjection = PerspectiveProjection(viewpoint, camera_z=camera_z)

    # use the colours from the test cube
    cube_spec: PuzzleCubeSpec = TEST_PUZZLE_CUBE_SPEC
    cube: PuzzleCube3D = PuzzleCube3D(projection, cube_spec)
    id_to_scene_polygon_before = cube.id_to_scene_polygon.copy()
    right_polygon_before = id_to_scene_polygon_before[RIGHT_ID]
    actual_vertices_before = right_polygon_before.get_vertices()

    model_vertices_before = FACE_PLANE_TO_VERTEX_PATH[FacePlane.RIGHT]
    expected_vertices_before = projection.project_points(model_vertices_before)
    assert np.allclose(actual_vertices_before, expected_vertices_before)

    # move the cube to the left
    rotation: np.ndarray = ORIGIN
    translation: np.ndarray = 7 * LEFT
    animorph: CubeRigidMotionAnimorph = CubeRigidMotionAnimorph(cube, rotation, translation)
    animorph.morph_to(1.0)

    id_to_scene_polygon_after = cube.id_to_scene_polygon
    right_polygon_after = id_to_scene_polygon_after[RIGHT_ID]
    actual_vertices_after = right_polygon_after.get_vertices()

    model_vertices_after = FACE_PLANE_TO_VERTEX_PATH[FacePlane.RIGHT] + translation
    expected_vertices_after = projection.project_points(model_vertices_after)
    assert np.allclose(actual_vertices_after, expected_vertices_after)

    assert len(id_to_scene_polygon_before) == len(id_to_scene_polygon_after)

def test_polygon_ids():
    for face_label in FaceLabel:
        polygon_id = PuzzleCube3D.name_to_id(face_label)
        face_label_2 = PuzzleCube3D.id_to_name(polygon_id)
        assert face_label_2 == face_label
        polygon_id_2 = PuzzleCube3D.name_to_id(face_label_2)
        assert polygon_id_2 == polygon_id
