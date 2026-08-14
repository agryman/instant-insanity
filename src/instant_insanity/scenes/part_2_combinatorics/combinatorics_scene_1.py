from typing import Sequence, cast

from manim import tempconfig, RIGHT, BLACK, Text, DOWN, OUT, Mobject, FadeIn, Indicate, PI, FadeOut
from manim.typing import Vector3D
from manim_voiceover import VoiceoverScene

from instant_insanity.animators.puzzle_3d_animators import Puzzle3DCubeRotationAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FacePlane
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import mk_standard_orthographic_projection, Projection
from instant_insanity.core.puzzle import PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC, PuzzleCubeNumber
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, mk_standard_puzzle3d
from instant_insanity.mobjects.puzzle_face_labeller import PuzzleFaceLabeller
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin, INDICATE_SCALE_FACTOR, INDICATE_TEXT_COLOUR
from instant_insanity.scenes.helpers import morph_and_checkpoint
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene


class CombinatoricsScene1(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):

    puzzle3d: Puzzle3D
    puzzle_face_labeller: PuzzleFaceLabeller

    def rotate_to_solution(self) -> None:

        # create the labels for the puzzle and add them to the scene
        for cube_number in PuzzleCubeNumber:
            self.puzzle_face_labeller.update_cube_texts(cube_number)

        # self.wait(3.0)
        #
        # self.say("Now rotate the cubes into the solution and confirm that the rotated labels are correct.")

        solution_rotation_axes: dict[PuzzleCubeNumber, list[Vector3D]] = {
            PuzzleCubeNumber.ONE: [OUT],
            PuzzleCubeNumber.TWO: [OUT, OUT],
            PuzzleCubeNumber.THREE: [DOWN, OUT, OUT],
            PuzzleCubeNumber.FOUR: [OUT, OUT],
        }

        rotation: Vector3D
        for cube_number in PuzzleCubeNumber:
            key_cube_number: PuzzleCubeNumber
            mask: dict[PuzzleCubeNumber, bool] = {
                key_cube_number: key_cube_number == cube_number for key_cube_number in PuzzleCubeNumber
            }
            # with self.voiceover(text=f"Rotate cube {cube_number}.") as tracker:
            #     voiceover_wait(self, tracker, 2.0)

            cube_rotation_axes: list[Vector3D] = solution_rotation_axes[cube_number]
            cube_rotation_axis: Vector3D
            for cube_rotation_axis in cube_rotation_axes:

                # remove the Text labels from the scene before rotating the cube
                self.puzzle_face_labeller.remove_cube_texts(cube_number)

                # rotate the cube
                rotation = cast(Vector3D, cube_rotation_axis * PI / 2.0)
                animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(self.puzzle3d, rotation, mask)
                morph_and_checkpoint(self, animorph, run_time=1.0, wait_time=0.25)

                # rotate the cube plane-to-label mapping
                self.puzzle_face_labeller.rotate_plane_to_label_mapping(cube_number, cube_rotation_axis)

                # create the Text labels for the rotated cube and add them to the scene
                self.puzzle_face_labeller.update_cube_texts(cube_number)
                #
                # self.wait(2.0)
        # self.wait(3.0)

    def indicate_face_label(self, cube: PuzzleCubeNumber, plane: FacePlane) -> None:
        face_label: Text = self.puzzle_face_labeller.get_face_label(cube, plane)
        self.play(Indicate(face_label, scale_factor=INDICATE_SCALE_FACTOR, color=INDICATE_TEXT_COLOUR))

    def subscene_0_set_up_solution(self) -> None:
        if self.skip(self.subscene_0_set_up_solution):
            return

        voiceover: str
        voiceover = """
        Here's the starting arrangement of the puzzle.
        Let's rotate it into the solution.
        """
        self.say(voiceover)

    def subscene_1_how_many_arrangements(self) -> None:
        if self.skip(self.subscene_1_how_many_arrangements):
            return

        topic: Mobject = self.mk_topic("How many ways can we arrange the four cubes?")
        voiceover: str = """
        How many ways can we arrange the four cubes?
        Let's count them.
        """
        self.discuss_mobject(topic, voiceover)

    def subscene_2_count_cube_orientations(self) -> None:
        if self.skip(self.subscene_2_count_cube_orientations):
            return

        voiceover: str
        voiceover = """
        We can label a cube orientation by specifying its front and top face labels.
        For example, consider cube one.
        Its front face is ex.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.ONE, FacePlane.FRONT)

        voiceover = "Its top face is wy."
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.ONE, FacePlane.TOP)

        voiceover = """
        Therefore the orientation of cube one is ex wy.
        
        In general, the front face can be any of the six faces.
        However, the top face must be adjacent to the front face so there are only four possibilities.
        So for each of the six possible front faces there are four possible top
        faces giving a total of 24 possible orientations for the cube. 
        """
        topic: Mobject = self.mk_topic(r"$6$ front faces $ \times\ 4$ top faces $ = 24$ orientations")
        self.discuss_mobject(topic, voiceover)


    def subscene_3_count_cube_arrangements(self) -> None:
        if self.skip(self.subscene_3_count_cube_arrangements):
            return

        topic: Mobject = self.mk_topic(r"$24 \times 24 \times 24 \times 24 = 331{,}776$ arrangements")
        voiceover: str = """
        An arrangement consists of four orientations, one for each of the four cubes.
        We can freely choose each orientation.
        Therefore, there are 331 thousand 776 possible arrangements of four cubes.
        """
        self.discuss_mobject(topic, voiceover)

    def subscene_4_horizontal_quarter_turns(self) -> None:
        if self.skip(self.subscene_4_horizontal_quarter_turns):
            return

        topic: Mobject = self.mk_topic(r"$82{,}944 = \frac{331{,}776}{4}$")
        topic.move_to(DOWN)
        self.play(FadeIn(topic))

        voiceover: str = """
        The Instant Insanity box claims that there are 82 thousand 944 combinations which is
        only one quarter of 331 thousand 776.
        This difference is explained by considering some arrangements to be essentially the same.
        Given any arrangement, we can rotate it along its horizontal axis by 90 degrees to obtain a
        different, but essentially equivalent, arrangement. 
        If we started with a solution then its 90 degree
        rotation is another, essentially equivalent, solution.
        This rotation is said to be a symmetry of the set of solutions since it sends solutions to solutions.
        """
        # self.discuss_mobject(topic, voiceover)
        self.say(voiceover)

        voiceover = """
        We can apply this 90 degree rotation four times
        to obtain a set of four essentially equivalent arrangements.
        """
        self.say(voiceover)

        for _ in range(4):
            self.puzzle_face_labeller.rotate_puzzle_ccw_90(RIGHT)
            self.wait(1.0)

        voiceover = """
        By regarding these rotations of arrangements to be essentially equivalent we reduce 331 thousand 776
        by a factor of 4 giving us 82 thousand 944 as claimed by the Instant Insanity box.
        """
        # self.discuss_mobject(topic, voiceover)
        self.say(voiceover)

        self.play(FadeOut(topic))

    def subscene_5_vertical_half_turns(self) -> None:
        if self.skip(self.subscene_5_vertical_half_turns):
            return

        topic: Mobject = self.mk_topic(r"$41{,}472 = \frac{82{,}944}{2} $")
        topic.move_to(DOWN)
        self.play(FadeIn(topic))

        voiceover: str
        voiceover = """
        However, there is another symmetry to consider.
        If we rotate each cube by 180 degrees about the vertical axis then the top and bottom sides don't change
        but the front and back sides get swapped. If we started with a solution then this 180 degree rotation
        gives us another solution. 
        """
        self.say(voiceover)

        voiceover = """
        We can perform this 180 degree rotation twice to obtain a 
        pair of essentially equivalent arrangements. 
        We therefore need to reduce 82 thousand 944 by a factor of two giving us 41 thousand 472 essentially distinct
        arrangements.
        """
        self.say(voiceover)

        for _ in range(2):
            self.puzzle_face_labeller.rotate_puzzle_ccw_90(DOWN)
            self.puzzle_face_labeller.rotate_puzzle_ccw_90(DOWN)
            self.wait(1.0)

        voiceover = """
        This analysis shows that the true number of essentially distinct arrangements is 
        in fact 41 thousand 472 as Carteblanche claimed.
        """
        self.say(voiceover)
        self.play(FadeOut(topic))

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        # show the puzzle
        projection: Projection = mk_standard_orthographic_projection()
        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        self.puzzle3d: Puzzle3D = mk_standard_puzzle3d(puzzle_spec, projection)
        self.add(self.puzzle3d)
        self.puzzle_face_labeller = PuzzleFaceLabeller(self, self.puzzle3d)

        # create the labels for the puzzle and add them to the scene
        self.puzzle_face_labeller.update_puzzle_texts()
        self.wait(1.0)

        self.subscene_0_set_up_solution()
        self.puzzle_face_labeller.remove_puzzle_texts()
        self.rotate_to_solution()

        self.subscene_1_how_many_arrangements()
        self.subscene_2_count_cube_orientations()
        self.subscene_3_count_cube_arrangements()
        self.subscene_4_horizontal_quarter_turns()
        self.subscene_5_vertical_half_turns()

        self.wait(1.0)

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            self.subscene_0_set_up_solution,
            self.subscene_1_how_many_arrangements,
            self.subscene_2_count_cube_orientations,
            self.subscene_3_count_cube_arrangements,
            self.subscene_4_horizontal_quarter_turns,
            self.subscene_5_vertical_half_turns,
        ]

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = CombinatoricsScene1()
        scene.render()
