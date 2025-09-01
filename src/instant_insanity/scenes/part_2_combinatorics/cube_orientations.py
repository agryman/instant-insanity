from math import degrees

from manim import Scene, tempconfig, RIGHT, UP, BLACK, Text, Polygon, DOWN, LEFT, OUT, IN, ORIGIN
from manim.typing import Point3D, Vector3D
from scipy.spatial.transform import Rotation

from instant_insanity.animators.cube_animators import CubeRigidMotionAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FacePlane
from instant_insanity.core.geometry_types import PolygonId, VertexPath
from instant_insanity.core.projection import OrthographicProjection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import FaceLabel, PuzzleCube
from instant_insanity.mobjects.coloured_cube import TEST_PUZZLE_CUBE_SPEC
from instant_insanity.mobjects.puzzle_cube_3d import PuzzleCube3D
from instant_insanity.scenes.coordinate_grid import GridMixin


class CubeOrientations(GridMixin, Scene):
    def construct(self):
        self.add_grid(False)

        front_to_tops_str: dict[FaceLabel, str] = {
            FaceLabel.X: "z,y,z',y'",
            FaceLabel.Y: "z,x,z',x'",
            FaceLabel.Z: "x',y',x,y",
            FaceLabel.X_PRIME: "z,y',z',y",
            FaceLabel.Y_PRIME: "z,x,z',x'",
            FaceLabel.Z_PRIME: "x,y,x',y'",
        }

        to_front_rotations: dict[FaceLabel, Rotation] = {
            FaceLabel.X: Rotation.identity(),
            FaceLabel.Y: Rotation.from_rotvec(90 * DOWN, degrees=True),
            FaceLabel.Z: Rotation.from_rotvec(90 * RIGHT, degrees=True),
            FaceLabel.X_PRIME: Rotation.from_rotvec(180 * UP, degrees=True),
            FaceLabel.Y_PRIME: Rotation.from_rotvec(90 * UP, degrees=True),
            FaceLabel.Z_PRIME: Rotation.from_rotvec(90 * LEFT, degrees=True),
        }

        to_top_rotations: list[Rotation] = [
            Rotation.identity(),
            Rotation.from_rotvec(90 * OUT, degrees=True),
            Rotation.from_rotvec(180 * OUT, degrees=True),
            Rotation.from_rotvec(90 * IN, degrees=True),
        ]

        top_str: str
        tops_str: str
        front_label: FaceLabel
        front_to_top_list: dict[FaceLabel, list[FaceLabel]] = {
            front_label : [FaceLabel(top)
                           for top in tops_str.split(',')
                           ] for front_label, tops_str in front_to_tops_str.items()
        }

        front_top_to_cube: dict[tuple[FaceLabel, FaceLabel], PuzzleCube3D] = {}
        projection: OrthographicProjection = mk_standard_orthographic_projection()
        col: int
        for col, front_label in enumerate(front_to_top_list.keys()):
            to_front_rotation: Rotation = to_front_rotations[front_label]
            delta_x: float = 4.0
            x_0: float = -2.5 * delta_x + 1.5
            x_col: float = x_0 + col * delta_x

            row: int
            top_label: FaceLabel
            for row, top_label in enumerate(front_to_top_list[front_label]):
                to_top_rotation: Rotation = to_top_rotations[row]
                delta_y: float = 4.0
                y_0: float = 1.5 * delta_y - 3.0
                y_row: float = y_0 - row * delta_y
                cube_centre: Point3D = x_col * RIGHT + y_row * UP
                cube3d: PuzzleCube3D = PuzzleCube3D(projection, TEST_PUZZLE_CUBE_SPEC, cube_centre)
                front_top_to_cube[(front_label, top_label)] = cube3d
                self.add(cube3d)

                # orient the cube using two rotations

                # translate the cube to the origin
                centre_to_origin: CubeRigidMotionAnimorph = CubeRigidMotionAnimorph(cube3d,
                                                                             ORIGIN,
                                                                             -1.0 * cube_centre)
                centre_to_origin.morph_to(1.0)
                cube3d.checkpoint()

                # rotate the cube to target front face
                front_rotation: Vector3D = Rotation.as_rotvec(to_front_rotation)
                front_animorph: CubeRigidMotionAnimorph = CubeRigidMotionAnimorph(cube3d,
                                                                                  front_rotation,
                                                                                  ORIGIN)
                front_animorph.morph_to(1.0)
                cube3d.checkpoint()

                # rotate the cube to the target top face, leaving the front face in place
                top_rotation: Vector3D = Rotation.as_rotvec(to_top_rotation)
                top_animorph: CubeRigidMotionAnimorph = CubeRigidMotionAnimorph(cube3d,
                                                                                top_rotation,
                                                                                ORIGIN)
                top_animorph.morph_to(1.0)
                cube3d.checkpoint()

                # translate the cube to the origin
                origin_to_centre: CubeRigidMotionAnimorph = CubeRigidMotionAnimorph(cube3d,
                                                                             ORIGIN,
                                                                             cube_centre)
                origin_to_centre.morph_to(1.0)
                cube3d.checkpoint()

                # add a text label
                label = front_label.value + top_label.value
                text: Text = Text(label, color=BLACK, font_size=18, font='sans-serif')
                front_id: PolygonId = PuzzleCube3D.name_to_id(front_label)
                front_polygon: Polygon = cube3d.id_to_scene_polygon[front_id]
                text.next_to(front_polygon, DOWN, buff=0.15)
                self.add(text)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = CubeOrientations()
        scene.render()
