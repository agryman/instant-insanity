from manim import tempconfig, RIGHT, UP, BLACK, Text, Polygon, DOWN, LEFT, OUT, IN, ORIGIN
from manim.typing import Point3D, Vector3D
from manim_voiceover import VoiceoverScene
from scipy.spatial.transform import Rotation

from instant_insanity.animators.cube_animators import CubeRigidMotionAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import OrthographicProjection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import FaceLabel
from instant_insanity.mobjects.coloured_cube import TEST_PUZZLE_CUBE_SPEC
from instant_insanity.mobjects.puzzle_cube_3d import PuzzleCube3D
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.subscene import SubsceneMixin


class CombinatoricsScene1(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        voiceover: str

        voiceover = """
        Our goal is to compute the total number of cube orientations.
        A cube has six faces so one of them must be on the front side.
        Each face is adjacent to four other faces so one of them must be on the top side.
        Therefore, we can orient a cube by specifying its front and top faces.
        This gives a total of 6 times 4 equals 24 possible orientations.
        """
        self.say(voiceover)

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
                self.wait(1.0)

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
                front_polygon: Polygon = cube3d.key_to_scene_polygon[front_label]
                text.next_to(front_polygon, DOWN, buff=0.15)
                self.add(text)

        self.wait(1.0)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = CombinatoricsScene1()
        scene.render()
