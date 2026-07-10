from typing import cast

from manim import tempconfig, PI, UP, DOWN, LEFT, RIGHT, IN, OUT
from manim.typing import Vector3D
from manim_voiceover import VoiceoverScene

from instant_insanity.animators.puzzle_3d_animators import (Puzzle3DAnimorph,
                                                            Puzzle3DCubeRotationAnimorph, Puzzle3DSetCubeGapAnimorph)
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC, PuzzleCubeNumber
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, mk_standard_puzzle3d, DEFAULT_BUFF
from instant_insanity.scenes.coordinate_grid import GridMixin

voiceover_text_1: str = """
The Instant Insanity puzzle consists of four cubes whose faces are coloured either red, white, blue, or green.
The goal of the puzzle is to arrange the cubes in a row so that no colour is
repeated along each of the four sides.
"""

voiceover_text_2: str = """
As its name suggests, Instant Insanity is very challenging to solve simply by trial and error
because there is a huge number of possible ways to arrange the cubes.
The Winning Moves box claims that there are eighty-two thousand nine hundred and forty-four combinations.

The surprising and delightful thing about Instant Insanity is that you can solve it very quickly 
using an elegant method based on some simple concepts from the branch of mathematics known as graph theory.

This video introduces graph theory and shows how to use it to solve Instant Insanity.
If you enjoy puzzles, and know some high school mathematics, then this video is for you.
"""

voiceover_text_3: str = """
One day in 1968, a university professor visited Arthur's high school and gave a guest lecture on graph theory.
He finished the lecture by showing how to apply graph theory to quickly solve Instant Insanity.
Arthur was very impressed by this demonstration of the power of graph theory and 
often used it for thinking about technical problems later in his career.
"""

voiceover_text_4: str = """
Fast forward to the present where we now have a wealth of excellent math videos on YouTube.
Several of them explain the solution to Instant Insanity but, in Arthur's opinion,
none of them fully exploit the potential of animation to clarify the concepts.
It occurred to Arthur that a compelling animation of the graph theory solution to Instant Insanity
might resonate with the current generation of young math enthusiasts
and perhaps inspire them to explore the subject further.
"""

class IntroductionScene2(GridMixin, VoiceoverScene):
    """
    This scene shows the puzzle cubes and explains the goal of the puzzle.
    """

    puzzle3d: Puzzle3D
    initial_gap: float
    min_gap: float

    def morph_and_checkpoint(self, animorph: Puzzle3DAnimorph) -> None:
        """
        This method conceals the puzzle, morphs it, and then checkpoints it.
        It is the generic puzzle animation sequence.
        Args:
            animorph: the animorph
        """
        self.puzzle3d.conceal_polygons()
        animorph.play(self, run_time=1.0)
        self.puzzle3d.checkpoint()
        self.wait()

    def describe_puzzle(self):
        with self.voiceover(text="""
        The Instant Insanity puzzle consists of four cubes whose faces are coloured 
        red, white, blue, or green.
        """) as tracker:
            voiceover_wait(self, tracker)

        with self.voiceover(text="""
        Let's rotate the puzzle so we can see the colours of all the faces.
        """) as tracker:
            voiceover_wait(self, tracker)

        self.wait()

        rotation_axes: list[Vector3D] = [RIGHT, DOWN]
        rotation_voiceovers: list[str] = [
            "First, we'll rotate the cubes around the horizontal axis.",
            "Next, we'll rotate each cube around its vertical axis."
        ]

        rotation_axis: Vector3D
        rotation_voiceover: str
        for rotation_axis, rotation_voiceover in zip(rotation_axes, rotation_voiceovers):
            with self.voiceover(text=rotation_voiceover) as tracker:
                voiceover_wait(self, tracker)
            # rotate the puzzle
            rotation: Vector3D = cast(Vector3D, rotation_axis * PI / 2.0)
            rotation_animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(self.puzzle3d, rotation)
            n: int
            for n in range(4):
                self.morph_and_checkpoint(rotation_animorph)

        with self.voiceover(text="""
            Now you've seen all the faces of all the cubes.
            You're ready to be told the goal of the puzzle.
            """) as tracker:
            voiceover_wait(self, tracker)

        self.wait()

    def describe_goal(self):
        with self.voiceover(text="""
            The puzzle challenges you to arrange the cubes in a row so that no colour is
            repeated along each of the four sides.
            """) as tracker:
            voiceover_wait(self, tracker)

        with self.voiceover(text="""
            Let's move the cubes together so they form a row.
            """) as tracker:
            voiceover_wait(self, tracker)

        # set the cube gap
        gap_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(self.puzzle3d, self.min_gap)
        self.morph_and_checkpoint(gap_animorph)

        self.wait()

        with self.voiceover(text="""
            As you can see, the front faces are green, red, white, and blue so 
            this combination of colours satisfies the goal of the puzzle.
            We need to check the top, back, and bottom faces.
            """) as tracker:
            voiceover_wait(self, tracker)

        with self.voiceover(text="""
            Rotate the row so that the top side becomes the front side.
            """) as tracker:
            voiceover_wait(self, tracker)

        right_rotation: Vector3D = cast(Vector3D, RIGHT * PI / 2.0)
        right_rotation_animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(self.puzzle3d, right_rotation)
        self.morph_and_checkpoint(right_rotation_animorph)

        with self.voiceover(text="""
            Here the faces are red, white, green, and blue so 
            this combination of colours also satisfies the goal of the puzzle.
            """) as tracker:
            voiceover_wait(self, tracker)

        with self.voiceover(text="""
            Rotate again.
            """) as tracker:
            voiceover_wait(self, tracker)
        self.morph_and_checkpoint(right_rotation_animorph)

        with self.voiceover(text="""
            Here the faces are white, green, red, and red.
            The colour red is repeated so 
            this combination does not satisfy the goal of the puzzle.
            """) as tracker:
            voiceover_wait(self, tracker)

        with self.voiceover(text="""
            Rotate one more time.
            """) as tracker:
            voiceover_wait(self, tracker)
        self.morph_and_checkpoint(right_rotation_animorph)

        with self.voiceover(text="""
            Here the faces are red, green, red, and white.
            Once again, the colour red is repeated so 
            this combination also does not satisfy the goal of the puzzle.
            """) as tracker:
            voiceover_wait(self, tracker)

        self.wait()

        with self.voiceover(text="""
            One more rotation brings us back to the starting position.
            """) as tracker:
            voiceover_wait(self, tracker)
        self.morph_and_checkpoint(right_rotation_animorph)

        self.wait()

        with self.voiceover(text="""
            You now know the rules of Instant Insanity.
            Simple, aren't they?
            Although the rules are simple, it's very challenging to find the solution. 
            There are thousands of ways to arrange the cubes but only one solution. 
            At this point, you may want to pause the video and
            try to solve the puzzle for yourself so you can see how challenging it is. 
            You can buy the puzzle online, or you can make one from cardboard.
            """) as tracker:
            voiceover_wait(self, tracker)

        self.wait()

    def exhibit_solution(self):
        with self.voiceover(text="""
            If you tried to solve the puzzle yourself but couldn't find a solution,
            you might be wondering if a solution actually exists.
            Yes, it exists and we'll exhibit it next to prove that.
            Start by spreading out the cubes again so we can rotate them freely.
            """) as tracker:
            voiceover_wait(self, tracker)

        gap_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(self.puzzle3d, self.initial_gap)
        self.morph_and_checkpoint(gap_animorph)
        self.wait()

        with self.voiceover(text="""
            Now we'll rotate each cube into the orientation that solves the puzzle.
            """) as tracker:
            voiceover_wait(self, tracker)

        solution_rotation_axes: dict[PuzzleCubeNumber, list[Vector3D]] = {
            PuzzleCubeNumber.ONE: [OUT],
            PuzzleCubeNumber.TWO: [OUT, OUT],
            PuzzleCubeNumber.THREE: [DOWN, OUT, OUT],
            PuzzleCubeNumber.FOUR: [OUT, OUT],
        }

        cube_number: PuzzleCubeNumber
        for cube_number in PuzzleCubeNumber:
            key_cube_number: PuzzleCubeNumber
            mask: dict[PuzzleCubeNumber, bool] = {
                key_cube_number: key_cube_number == cube_number for key_cube_number in PuzzleCubeNumber
            }
            with self.voiceover(text=f"Rotate cube {cube_number}.") as tracker:
                voiceover_wait(self, tracker, 2.0)
            cube_rotation_axes: list[Vector3D] = solution_rotation_axes[cube_number]
            cube_rotation_axis: Vector3D
            for cube_rotation_axis in cube_rotation_axes:
                rotation: Vector3D = cast(Vector3D, cube_rotation_axis * PI / 2.0)
                animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(self.puzzle3d, rotation, mask)
                self.morph_and_checkpoint(animorph)

        with self.voiceover(text="""
            Now let's bring the cubes back together and check each of the four sides.
            """) as tracker:
            voiceover_wait(self, tracker)

        gap_animorph = Puzzle3DSetCubeGapAnimorph(self.puzzle3d, self.min_gap)
        self.morph_and_checkpoint(gap_animorph)
        self.wait()

        with self.voiceover(text="""
            We'll rotate the row along its horizontal axis to confirm that each side contains all four colours.
            """) as tracker:
            voiceover_wait(self, tracker)

        # rotate the puzzle
        rotation: Vector3D = cast(Vector3D, RIGHT * PI / 2.0)
        rotation_animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(self.puzzle3d, rotation)
        solution_texts: list[str] = [
            "No colour is repeated on the front side.",
            "No repeats here either.",
            "Still looking good.",
            "Eureka!"
        ]
        n: int
        for n in range(4):
            with self.voiceover(text=solution_texts[n])as tracker:
                voiceover_wait(self, tracker)
            self.morph_and_checkpoint(rotation_animorph)

        with self.voiceover(text="""
            No colour was repeated on any of the four sides.
            This arrangement of the cubes therefore solves the puzzle.
            """) as tracker:
            voiceover_wait(self, tracker)

        with self.voiceover(text="""
            Next we'll show an ingenious approach to solving the puzzle.
            This approach makes use of techniques from the branch of mathematics called graph theory.
            We'll start by explaining a few key concepts from graph theory and 
            then apply them to solving the puzzle.
            """) as tracker:
            voiceover_wait(self, tracker)

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

        self.describe_puzzle()
        self.describe_goal()
        self.exhibit_solution()


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = IntroductionScene2()
        scene.render()
