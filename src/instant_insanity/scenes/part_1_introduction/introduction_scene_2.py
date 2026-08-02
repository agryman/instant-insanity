from typing import cast, Sequence

from manim import tempconfig, PI, DOWN, RIGHT, OUT, Mobject
from manim.typing import Vector3D
from manim_voiceover import VoiceoverScene

from instant_insanity.animators.puzzle_3d_animators import Puzzle3DCubeRotationAnimorph, Puzzle3DSetCubeGapAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC, PuzzleCubeNumber
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, mk_standard_puzzle3d, DEFAULT_BUFF
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.helpers import morph_and_checkpoint
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene

INTRODUCTION = "introduction"
ROTATION_RUNTIME: float = 0.75
ROTATION_WAIT_TIME: float = 0.25
IMAGE_HEIGHT: float = 6.0


class IntroductionScene2(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    """
    This scene shows the puzzle cubes, explains the goal of the puzzle, and exhibits the solution.
    It leads in to the graph theory scenes.
    """

    puzzle3d: Puzzle3D
    initial_gap: float
    min_gap: float

    def subscene_1_describe_puzzle(self):
        if self.skip(self.subscene_1_describe_puzzle):
            return

        voiceover: str

        voiceover = """
        The Instant Insanity puzzle consists of four cubes whose faces are coloured 
        red, white, blue, or green.
        """
        self.say(voiceover)

        voiceover = """
        Let's rotate the puzzle so we can see the colours of all the faces.
        """
        self.say(voiceover)
        self.wait()

        rotation_axes: list[Vector3D] = [RIGHT, DOWN]
        rotation_voiceovers: list[str] = [
            "First, we'll rotate the cubes around their horizontal axis.",
            "Next, we'll rotate each cube around its vertical axis."
        ]

        rotation_axis: Vector3D
        rotation_voiceover: str
        for rotation_axis, rotation_voiceover in zip(rotation_axes, rotation_voiceovers):
            self.say(rotation_voiceover)
            # rotate the puzzle
            rotation: Vector3D = cast(Vector3D, rotation_axis * PI / 2.0)
            rotation_animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(self.puzzle3d, rotation)
            n: int
            for n in range(4):
                morph_and_checkpoint(self, rotation_animorph)

        voiceover = """
        Now you've seen all the faces of all the cubes.
        We'll state the goal of the puzzle next.
        """
        self.say(voiceover)

    def subscene_2_describe_goal(self):
        if self.skip(self.subscene_2_describe_goal):
            return

        voiceover: str

        voiceover = """
        The puzzle challenges you to arrange the cubes in a row so that no colour is
        repeated along each of the four sides.
        """
        self.say(voiceover)

        voiceover = """
        Let's move the cubes together so they form a row.
        """
        self.say(voiceover)

        # set the cube gap
        gap_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(self.puzzle3d, self.min_gap)
        morph_and_checkpoint(self, gap_animorph)

        voiceover = """
        As you can see, the front side has all four colours so
        it satisfies the goal of the puzzle.
        We need to check the top, back, and bottom sides.
        """
        self.say(voiceover)

        voiceover = """
        Rotate the row so that the top side becomes the front side.
        """
        self.say(voiceover)

        right_rotation: Vector3D = cast(Vector3D, RIGHT * PI / 2.0)
        right_rotation_animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(self.puzzle3d, right_rotation)
        morph_and_checkpoint(self, right_rotation_animorph)

        voiceover = """
        Again we have all four colours so 
        this side also satisfies the goal of the puzzle.
        """
        self.say(voiceover)

        voiceover = """
        Rotate again.
        """
        self.say(voiceover)
        morph_and_checkpoint(self, right_rotation_animorph)

        voiceover = """
        Now the colour red is repeated so 
        this side does not satisfy the goal of the puzzle.
        """
        self.say(voiceover)

        voiceover = """
        Rotate one more time.
        """
        self.say(voiceover)
        morph_and_checkpoint(self, right_rotation_animorph)

        voiceover = """
        Once again, the colour red is repeated so 
        this side also does not satisfy the goal of the puzzle.
        """
        self.say(voiceover)

        voiceover = """
        One more rotation brings us back to the starting position.
        """
        self.say(voiceover)
        morph_and_checkpoint(self, right_rotation_animorph)

        gap_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(self.puzzle3d, self.initial_gap)
        morph_and_checkpoint(self, gap_animorph)

        voiceover = """
        You now know the rules of Instant Insanity.
        Simple, aren't they?
        """
        self.say(voiceover)

    def subscene_3_show_box_front(self):
        if self.skip(self.subscene_3_show_box_front):
            return

        self.remove(self.puzzle3d)
        image: Mobject = self.get_image("instant-insanity-box-front.png", INTRODUCTION, IMAGE_HEIGHT)
        discussion:str = """
        Although the goal is simple to state, it's very challenging to find the solution. 
        The Instant Insanity box claims there are eighty-two thousand nine hundred
        and forty-four combinations, but only one solution. 
        """
        self.discuss_mobject(image, discussion)
        self.add(self.puzzle3d)

    def subscene_4_exhibit_solution(self):
        if self.skip(self.subscene_4_exhibit_solution):
            return

        voiceover: str

        voiceover = """
        Looking ahead, we are going to find the following essentially unique solution.
        We'll rotate each cube its starting orientation into its solution orientation.
        """
        self.say(voiceover)

        solution_rotation_axes: dict[PuzzleCubeNumber, list[Vector3D]] = {
            PuzzleCubeNumber.ONE: [OUT],
            PuzzleCubeNumber.TWO: [OUT, OUT],
            PuzzleCubeNumber.THREE: [DOWN, OUT, OUT],
            PuzzleCubeNumber.FOUR: [OUT, OUT],
        }

        rotation: Vector3D
        cube_number: PuzzleCubeNumber
        for cube_number in PuzzleCubeNumber:
            key_cube_number: PuzzleCubeNumber
            mask: dict[PuzzleCubeNumber, bool] = {
                key_cube_number: key_cube_number == cube_number for key_cube_number in PuzzleCubeNumber
            }

            voiceover = f"Rotate cube {cube_number}."
            self.say(voiceover)

            cube_rotation_axes: list[Vector3D] = solution_rotation_axes[cube_number]
            cube_rotation_axis: Vector3D
            for cube_rotation_axis in cube_rotation_axes:
                rotation = cast(Vector3D, cube_rotation_axis * PI / 2.0)
                animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(self.puzzle3d, rotation, mask)
                morph_and_checkpoint(self, animorph, run_time=ROTATION_RUNTIME, wait_time=ROTATION_WAIT_TIME)

        voiceover = """
        Now let's confirm that this arrangement is in fact the solution.
        """
        self.say(voiceover)

        gap_animorph = Puzzle3DSetCubeGapAnimorph(self.puzzle3d, self.min_gap)
        morph_and_checkpoint(self, gap_animorph)
        self.wait()

        # rotate the puzzle
        rotation = cast(Vector3D, RIGHT * PI / 2.0)
        rotation_animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(self.puzzle3d, rotation)
        solution_texts: list[str] = [
            "No colour is repeated on the front side.",
            "No repeats here either.",
            "Still looking good.",
            "Eureka!",
        ]
        for voiceover in solution_texts:
            self.say(voiceover)
            morph_and_checkpoint(self, rotation_animorph, run_time = ROTATION_RUNTIME, wait_time = ROTATION_WAIT_TIME)

        voiceover = """
            As claimed, this arrangement solves the puzzle.
        """
        self.say(voiceover)

        # set the cube gap
        gap_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(self.puzzle3d, self.initial_gap)
        morph_and_checkpoint(self, gap_animorph)


        voiceover = """
        Next we'll show an ingenious approach to finding the solution
        that uses ideas from the branch of mathematics called graph theory.
        Don't worry if you've never heard of graph theory.
        We'll explain all the necessary concepts and then apply them to finding the solution.
        If you enjoy solving puzzles then this video is for you.
        Welcome to: A Puzzling Introduction to Graph Theory!
        """
        self.say(voiceover)

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        # create and display the 3D puzzle
        puzzle_spec: PuzzleSpec = WINNING_MOVES_PUZZLE_SPEC
        projection: Projection = mk_standard_orthographic_projection()

        self.puzzle3d = mk_standard_puzzle3d(puzzle_spec, projection, centre=True)
        self.initial_gap = self.puzzle3d.get_cube_gap()
        self.min_gap = DEFAULT_BUFF
        self.add(self.puzzle3d)

        self.subscene_1_describe_puzzle()
        self.subscene_2_describe_goal()
        self.subscene_3_show_box_front()
        self.subscene_4_exhibit_solution()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            # self.subscene_1_describe_puzzle,
            # self.subscene_2_describe_goal,
            # self.subscene_3_show_box_front,
            # self.subscene_4_exhibit_solution,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = IntroductionScene2()
        scene.render()
