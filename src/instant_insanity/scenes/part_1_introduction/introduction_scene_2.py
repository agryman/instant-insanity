from typing import cast, Sequence

from manim import tempconfig, PI, DOWN, RIGHT, OUT, Mobject, FadeIn, ORIGIN, FadeOut
from manim.typing import Vector3D
from manim_voiceover import VoiceoverScene

from instant_insanity.animators.puzzle_3d_animators import Puzzle3DCubeRotationAnimorph, Puzzle3DSetCubeGapAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import PuzzleSpec, WINNING_MOVES_PUZZLE_SPEC, PuzzleCubeNumber, WINNING_MOVES_PUZZLE
from instant_insanity.mobjects.opposite_face_graph import EdgeToSubgraphMapping, OppositeFaceGraph
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, mk_standard_puzzle3d, DEFAULT_BUFF
from instant_insanity.mobjects.puzzle_face_labeller import PuzzleFaceLabeller
# from instant_insanity.scenes import discussion
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin, PAGE_HEIGHT
from instant_insanity.scenes.helpers import morph_and_checkpoint
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene

INTRODUCTION = "introduction"
ROTATION_RUNTIME: float = 0.5
ROTATION_WAIT_TIME: float = 0.1
IMAGE_HEIGHT: float = 6.0


class IntroductionScene2(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    """
    This scene shows the puzzle cubes and explains the goal of the puzzle.
    It leads into the graph theory scenes.
    """

    puzzle3d: Puzzle3D
    initial_gap: float
    min_gap: float
    puzzle_face_labeller: PuzzleFaceLabeller

    def subscene_1_describe_puzzle(self):
        if self.skip(self.subscene_1_describe_puzzle):
            return

        voiceover: str

        voiceover = """
        The Instant Insanity puzzle consists of four cubes whose faces are coloured 
        red, white, blue, or green.
        """
        self.say(voiceover)

    def subscene_2_describe_goal(self):
        if self.skip(self.subscene_2_describe_goal):
            return

        voiceover: str

        voiceover = """
        The puzzle challenges us to arrange the cubes in a row so that 
        each side contains all four colours.
        
        Let's see if this arrangement is a solution.
        """
        self.say(voiceover)

        # set the cube gap
        gap_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(self.puzzle3d, self.min_gap)
        morph_and_checkpoint(self, gap_animorph, run_time=ROTATION_RUNTIME, wait_time=ROTATION_WAIT_TIME)

        voiceover = """
        The front side looks good.
        """
        self.say(voiceover)

        right_rotation: Vector3D = cast(Vector3D, RIGHT * PI / 2.0)
        right_rotation_animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(self.puzzle3d, right_rotation)
        morph_and_checkpoint(self, right_rotation_animorph, run_time=ROTATION_RUNTIME, wait_time=ROTATION_WAIT_TIME)

        voiceover = """
        So does the top side.
        """
        self.say(voiceover)

        morph_and_checkpoint(self, right_rotation_animorph, run_time=ROTATION_RUNTIME, wait_time=ROTATION_WAIT_TIME)

        voiceover = """
        The back side repeats red so this arrangement is not a solution.
        """
        self.say(voiceover)

        morph_and_checkpoint(self, right_rotation_animorph, run_time=ROTATION_RUNTIME, wait_time=ROTATION_WAIT_TIME)

        voiceover = """
        The bottom side also repeats red.
        Only two of the four sides satisfy the goal.
        """
        self.say(voiceover)

        morph_and_checkpoint(self, right_rotation_animorph, run_time=ROTATION_RUNTIME, wait_time=ROTATION_WAIT_TIME)

        gap_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(self.puzzle3d, self.initial_gap)
        morph_and_checkpoint(self, gap_animorph)

        voiceover = """
        The rules of Instant Insanity are simple, aren't they?
        Our starting arrangement is not a solution so
        we have to rotate individual cubes until we get four colours on each side.
        How hard could that be?
        """
        self.say(voiceover)

    def subscene_3_instant_insanity_box_front(self) -> None:
        if self.skip(self.subscene_3_instant_insanity_box_front):
            return

        subpackages: str = INTRODUCTION
        image_height: float = PAGE_HEIGHT
        image_filename: str = "instant-insanity-box-front.png"
        image_voiceover: str = """
        Here's the Instant Insanity box.
        """

        annotated_filenames: list[str] = [
            "instant-insanity-box-front-greyscale-82944-wide.png",
        ]
        annotated_voiceovers: list[str] = [
            """
            It claims there are eighty-two thousand nine hundred
            and forty-four combinations so we can't possibly try every one of them.
            We need a more intelligent search strategy.
            """,
        ]

        self.remove(self.puzzle3d)
        self.discuss_and_zoom_image(
            subpackages,
            image_filename,
            image_height,
            image_voiceover,
            annotated_filenames,
            annotated_voiceovers
        )
        self.add(self.puzzle3d)

    def subscene_4_lead_into_graph_theory(self):
        if self.skip(self.subscene_4_lead_into_graph_theory):
            return

        voiceover: str
        # set the cube gap
        gap_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(self.puzzle3d, self.initial_gap)
        morph_and_checkpoint(self, gap_animorph)

        voiceover = """
        One day a university professor visited Arthur's high school and 
        gave an introductory lecture on graph theory.
        He ended the lecture by showing an ingenious graph-theoretic solution to Instant Insanity.
        """
        self.say(voiceover)

        voiceover = """
        Labelling the faces of the cubes makes it easier to describe the graph that represents the puzzle.
        """
        self.say(voiceover)

        # show the labels
        self.puzzle_face_labeller.update_puzzle_texts()
        voiceover = """
        We'll refer to the cubes as one through four from left to right.
        Label the front, right, and top cube faces in the starting arrangement as ex, wy, and zed.
        Add primes to the labels of the corresponding opposite faces.
        For example, the front face of cube 1 is labelled 1 ex which is opposite face 1 ex prime.
        """
        self.say(voiceover)

        # hide the labels
        self.puzzle_face_labeller.remove_puzzle_texts()
        self.remove(self.puzzle3d)

        # create the full Winning Moves opposite-face graph
        full_subgraph: EdgeToSubgraphMapping = OppositeFaceGraph.mk_subgraph_for_flag(True)
        wm_graph: OppositeFaceGraph = OppositeFaceGraph(WINNING_MOVES_PUZZLE, ORIGIN)
        wm_graph.set_subgraph(full_subgraph)

        self.play(FadeIn(wm_graph))
        voiceover = """
        Here's the graph that represents the puzzle.
        We call it the opposite-face graph.
        """
        self.say(voiceover)

        voiceover = """
        A graph is a set of dots connected by lines.
        We call the dots nodes and lines edges.
        The nodes of this graph represent the four face colours.
        The edges connect pairs of opposite faces.
        The edges are labelled with the cube number and the face label letter.
        For example, the edge labelled 1 ex represents the ex and ex prime pair of faces in cube 1.
        One face of this pair is green and the other is white.
        There are four cubes and each cube has three pairs of opposite faces so
        altogether the graph has twelve edges.
        
        If you enjoy solving puzzles, and are curious about graph theory, then this video is for you.
        """
        self.say(voiceover)
        self.play(FadeOut(wm_graph))

        topic: Mobject = self.mk_topic("Instant Insanity - A Puzzling Introduction to Graph Theory")
        discussion = """        
        Welcome to: Instant Insanity - A Puzzling Introduction to Graph Theory!
        """
        self.discuss_mobject(topic, discussion)

        self.add(self.puzzle3d)
        self.wait()

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

        self.puzzle_face_labeller = PuzzleFaceLabeller(self, self.puzzle3d)

        self.subscene_1_describe_puzzle()
        self.subscene_2_describe_goal()
        self.subscene_3_instant_insanity_box_front()
        self.subscene_4_lead_into_graph_theory()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            self.subscene_1_describe_puzzle,
            self.subscene_2_describe_goal,
            self.subscene_3_instant_insanity_box_front,
            self.subscene_4_lead_into_graph_theory,
        ]


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = IntroductionScene2()
        scene.render()
