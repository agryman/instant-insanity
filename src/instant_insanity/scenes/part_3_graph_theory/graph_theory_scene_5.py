"""
This module animates the conversion of the subgraphs into a solution of the puzzle.
The scene starts with the two subgraphs on the bottom half the of the frame and nothing
in the top half. The state of the scene is determined by the puzzle and the solution number.
Recall that Carteblanche's puzzle has two solutions.
"""
from typing import cast, Sequence

from manim import Scene, tempconfig, LEFT, DOWN, RIGHT, Tex, BLACK, FadeIn, PI, Text, Indicate, AnimationGroup, OUT
from manim.typing import Point3D, Vector3D
from manim_voiceover import VoiceoverScene, VoiceoverTracker
from typing_extensions import runtime

from instant_insanity.animators.puzzle_3d_animators import Puzzle3DSetCubeGapAnimorph, Puzzle3DCubeRotationAnimorph, \
    Puzzle3DAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FacePlane
from instant_insanity.core.cube_rotations import VisibleCubeTexts
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import Puzzle, WINNING_MOVES_PUZZLE, PuzzleCubeNumber, AxisLabel, PuzzleSpec, \
    WINNING_MOVES_PUZZLE_SPEC
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.mobjects import labelled_subgraph
from instant_insanity.mobjects.labelled_subgraph import LabelledSubgraph, LabelledSubgraphPair
from instant_insanity.mobjects.puzzle_face_labeller import PuzzleFaceLabeller
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, EdgeToSubgraphMapping, mk_edge_directions, \
    EdgeToMobjectMapping
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, DEFAULT_BUFF
from instant_insanity.mobjects.stealth_tip import CubeEdgeTip
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.helpers import morph_and_checkpoint
from instant_insanity.scenes.part_3_graph_theory.graph_theory_scene_3 import GraphTheoryScene3
from instant_insanity.scenes.subscene import SubsceneMixin, Subscene


class GraphTheoryScene5(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):
    """
    This scene shows how to convert the subgraph pair into puzzle solutions.
    """
    puzzle: Puzzle
    labelled_subgraph_pair: LabelledSubgraphPair
    puzzle_face_labeller: PuzzleFaceLabeller
    puzzle3d: Puzzle3D
    initial_gap: float
    min_gap: float

    def indicate_face_label(self, cube: PuzzleCubeNumber, plane: FacePlane) -> None:
        face_label: Text = self.puzzle_face_labeller.get_face_label(cube, plane)
        self.play(Indicate(face_label, scale_factor=2.0, color=BLACK))

    def indicate_edge_label(self, plane: FacePlane, cube: PuzzleCubeNumber, axis: AxisLabel) -> None:
        edge_label: Text = self.labelled_subgraph_pair.get_edge_label(plane, cube, axis)
        self.play(Indicate(edge_label, scale_factor=2.0, color=BLACK))

    def subscene_1_introduction(self) -> None:
        if self.skip(self.subscene_1_introduction):
            return

        voiceover: str = """
        Now we'll show how to convert these subgraphs 
        into the solution of the puzzle.
        """
        self.say(voiceover)
        self.wait()

    def subscene_2_show_puzzle(self) -> None:
        if self.skip(self.subscene_2_show_puzzle):
            return

        voiceover: str = """
        Here's the starting arrangement of the puzzle.
        """
        self.say(voiceover)
        self.wait()

    def subscene_3_describe_face_labels(self) -> None:
        if self.skip(self.subscene_3_describe_face_labels):
            return

        visible_planes: list[FacePlane] = [FacePlane.FRONT, FacePlane.RIGHT, FacePlane.TOP]

        plane_to_voiceover: dict[FacePlane, str] = {
            FacePlane.FRONT: "In this arrangement, each cube has face ex on the front side,",
            FacePlane.RIGHT: "face wy on the right side,",
            FacePlane.TOP: "and face zed on the top side.",
        }

        cube_to_visible_texts: dict[PuzzleCubeNumber, VisibleCubeTexts] = (
            self.puzzle_face_labeller.cube_to_visible_texts
        )

        plane: FacePlane
        n: PuzzleCubeNumber
        plane_to_texts: dict[FacePlane, list[Text]] = {
            plane: [
                cube_to_visible_texts[n].get_label(plane)
                for n in PuzzleCubeNumber
            ]
            for plane in visible_planes
        }

        for plane in visible_planes:
            voiceover: str = plane_to_voiceover[plane]
            texts: list[Text] = plane_to_texts[plane]
            text: Text
            indicate_texts: AnimationGroup = AnimationGroup(
                *[Indicate(text, scale_factor=2.0, color=BLACK) for text in texts],
                lag_ratio=0.15
            )
            self.say(voiceover)
            self.wait(0.5)
            self.play(indicate_texts, runtime=2.0)

        self.wait()

    def subscene_3b_roll_puzzle(self) -> None:
        if self.skip(self.subscene_3b_roll_puzzle):
            return

        voiceover: str = """
        The starting arrangement is not a solution.
        Let's roll it to show that some sides have repeated colours.
        """
        self.say(voiceover)
        self.puzzle_face_labeller.roll_puzzle()
        self.wait()

    def subscene_4_discuss_matching(self) -> None:
        if self.skip(self.subscene_4_discuss_matching):
            return

        voiceover: str
        voiceover = """
        We need to rotate each cube to match the orientaions given in the subgraphs.
        First we'll match the front-back subgraph.
        """
        self.say(voiceover)
        self.labelled_subgraph_pair.indicate_label(self, FacePlane.FRONT)

        voiceover = """
        Then we'll match the top-bottom subgraph.
        """
        self.say(voiceover)
        self.labelled_subgraph_pair.indicate_label(self, FacePlane.TOP)

        voiceover = """
        For each subgraph, we'll match the cubes one at a time, from left to right.
        """
        self.say(voiceover)
        self.wait()

    def subscene_4_discuss_front_cube_1(self) -> None:
        if self.skip(self.subscene_4_discuss_front_cube_1):
            return

        voiceover: str
        voiceover = """
        Let's start with the front-back subgraph. 
        """
        self.say(voiceover)
        self.labelled_subgraph_pair.indicate_label(self, FacePlane.FRONT)

        voiceover = """
        Look at edge 1 ex which connects green to white.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.FRONT, PuzzleCubeNumber.ONE, AxisLabel.X)

        voiceover = """
        This edge tells us that 
        we need face ex, which is green, on the front side and
        face ex prime, which is white, on the back side.

        Face ex of cube 1 is already on the front side.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.ONE, FacePlane.FRONT)

        voiceover = """
        Therefore, the starting orientation of cube 1
        matches the front-back subgraph so we don't need to rotate it.
        """
        self.say(voiceover)
        self.wait()

    def subscene_4_discuss_front_cube_2(self) -> None:
        if self.skip(self.subscene_4_discuss_front_cube_2):
            return

        voiceover: str
        voiceover = """
        Next consider edge 2 ex which connects red to green.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.FRONT, PuzzleCubeNumber.TWO, AxisLabel.X)

        voiceover = """
        We need face ex, which is red, on the front side and 
        face ex prime, which is green, on the back side.

        Face ex of cube 2 is already on the front side.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.TWO, FacePlane.FRONT)

        voiceover = """
        The starting orientation of cube 2 matches the front-back subgraph
        so we don't need to rotate it. 
        """
        self.say(voiceover)
        self.wait()

    def subscene_4_discuss_front_cube_3(self) -> None:
        if self.skip(self.subscene_4_discuss_front_cube_2):
            return

        voiceover: str = """
        Now look at edge 3 wy which connects white to blue.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.FRONT, PuzzleCubeNumber.THREE, AxisLabel.Y)

        voiceover: str = """
        We need face wy, which is white, on the front side and 
        face wy prime, which is blue, on the back side.

        Face ex of cube 3 is currently on the front side.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.THREE, FacePlane.FRONT)

        voiceover: str = """
        We therefore need to rotate face wy of cube 3 to the front side.
        """
        self.say(voiceover)
        self.wait()

    def subscene_4_discuss_front_cube_4(self) -> None:
        if self.skip(self.subscene_4_discuss_front_cube_4):
            return

        voiceover: str
        voiceover= """
        Wrapping up the front-back subgraph, 
        look at edge 4 ex which connects blue to red.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.FRONT, PuzzleCubeNumber.FOUR, AxisLabel.X)

        voiceover = """
        We need face ex, which is blue, on the front side and 
        face ex prime, which is red, on the back side.
        
        The front face of cube 4 is labelled ex.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.FOUR, FacePlane.FRONT)

        voiceover = """
        The starting orientation of cube 4 already matches the front-back subgraph
        so we don't need to rotate it.

        We have now completed matching the front and back sides
        to the front-back subgraph.
        
        Let's roll the puzzle so we can confirm that the front and back sides
        have no repeated colours
        """
        self.say(voiceover)
        self.puzzle_face_labeller.roll_puzzle()

        voiceover = """
        At this point we are halfway to the solution.
        It remains to match the top and bottom sides to the top-bottom subgraph.
        """
        self.say(voiceover)
        self.wait()

    def subscene_5_discuss_top_cube_1(self) -> None:
        if self.skip(self.subscene_5_discuss_top_cube_1):
            return

        voiceover: str
        voiceover = """
        Now let's work on the top-bottom subgraph.
        """
        self.say(voiceover)
        self.labelled_subgraph_pair.indicate_label(self, FacePlane.TOP)

        voiceover = """
        We'll match the top and bottom sides to the top-bottom subgraph by rotating the cubes.
        However, we'll only rotate the cubes about their front-back axes 
        so that we don't change the front and back sides.
        """
        self.say(voiceover)

        voiceover = """
        Look at edge 1 wy which connects blue to red.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.TOP, PuzzleCubeNumber.ONE, AxisLabel.Y)

        voiceover = """
        We need face wy, which is blue, on the top side and
        face wy prime, which is red, on the bottom side.
        
        Face zed of cube 1 is currently on the top side.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.ONE, FacePlane.TOP)

        voiceover = """
        We need to rotate face wy of cube 1 to the top side.
        """
        self.say(voiceover)
        self.wait()

    def subscene_5_discuss_top_cube_2(self) -> None:
        if self.skip(self.subscene_5_discuss_top_cube_2):
            return

        voiceover: str
        voiceover = """
        Now, look at edge 2 zed which connects green to white.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.TOP, PuzzleCubeNumber.TWO, AxisLabel.Z)

        voiceover = """
        We need face zed, which is white, on the bottom side and
        face zed prime, which is green, on the top side.

        Face zed of cube 2 is currently on the top side.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.TWO, FacePlane.TOP)

        voiceover = """
        We need to rotate face zed of cube 2 to the bottom side.
        """
        self.say(voiceover)
        self.wait()

    def subscene_5_discuss_top_cube_3(self) -> None:
        if self.skip(self.subscene_5_discuss_top_cube_3):
            return

        voiceover: str
        voiceover = """
        Next, look at edge 3 zed which connects red to green.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.TOP, PuzzleCubeNumber.THREE, AxisLabel.Z)

        voiceover = """
        We need face zed, which is green, on the bottom side and
        face zed prime, which is red, on the top side.

        Face zed of cube 3 is currently on the top side.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.THREE, FacePlane.TOP)

        voiceover = """
        We need to rotate face zed of cube 3 to the bottom side.
        """
        self.say(voiceover)
        self.wait()

    def subscene_5_discuss_top_cube_4(self) -> None:
        if self.skip(self.subscene_5_discuss_top_cube_4):
            return

        voiceover: str
        voiceover = """
        Finally, look at edge 4 zed which connects white to blue.
        """
        self.say(voiceover)
        self.indicate_edge_label(FacePlane.TOP, PuzzleCubeNumber.FOUR, AxisLabel.Z)

        voiceover = """
        We need face zed, which is blue, on the bottom side and
        face zed prime, which is white, on the top side.
    
        Face zed of cube 4 is currently on the top side.
        """
        self.say(voiceover)
        self.indicate_face_label(PuzzleCubeNumber.FOUR, FacePlane.TOP)

        voiceover = """
        We need to rotate face zed of cube 4 to the bottom side.
        """
        self.say(voiceover)
        self.wait()

    def subscene_6_conclusion(self) -> None:
        if self.skip(self.subscene_6_conclusion):
            return

        voiceover: str = """
        We've oriented all the cubes to match the subgraphs.
        Let's roll the cubes to confirm that we have solved the puzzle.
        """
        self.say(voiceover)
        self.puzzle_face_labeller.roll_puzzle()

        voiceover = """
        We have successfully converted the subgraphs into the solution.
        You now know some graph theory and how to use it
        to solve Instant Insanity!
        """
        self.say(voiceover)
        self.wait()

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        # recreate the final content of the previous scene
        puzzle: Puzzle =  WINNING_MOVES_PUZZLE
        self.puzzle = puzzle

        labelled_subgraph_pair: LabelledSubgraphPair = LabelledSubgraphPair(puzzle)
        self.labelled_subgraph_pair = labelled_subgraph_pair

        labelled_subgraph_pair.add_to_scene(self)
        labelled_subgraph_pair.add_solution_edges()
        labelled_subgraph_pair.add_edge_directions(self)

        self.subscene_1_introduction()

        # create and display the 3D puzzle
        projection: Projection = mk_standard_orthographic_projection()
        puzzle3d: Puzzle3D = GraphTheoryScene3.mk_puzzle3d(puzzle, projection)
        self.puzzle3d = puzzle3d
        self.add(puzzle3d)

        initial_gap: float = puzzle3d.get_cube_gap()
        self.initial_gap = initial_gap

        min_gap: float = DEFAULT_BUFF
        self.min_gap = min_gap

        # add the cube visible face labels
        puzzle_face_labeller: PuzzleFaceLabeller = PuzzleFaceLabeller(self, puzzle3d)
        self.puzzle_face_labeller = puzzle_face_labeller
        puzzle_face_labeller.update_puzzle_texts()
        self.wait(0.5)

        self.subscene_2_show_puzzle()

        self.subscene_3_describe_face_labels()

        self.subscene_3b_roll_puzzle()

        self.subscene_4_discuss_matching()

        self.subscene_4_discuss_front_cube_1()

        self.subscene_4_discuss_front_cube_2()

        self.subscene_4_discuss_front_cube_3()

        # rotate cube 3 by 90 degrees ccw about the DOWN axis.
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.THREE, DOWN)
        self.wait(2.0)

        self.subscene_4_discuss_front_cube_4()

        self.subscene_5_discuss_top_cube_1()
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.ONE, OUT)
        self.wait(2.0)

        self.subscene_5_discuss_top_cube_2()
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.TWO, OUT)
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.TWO, OUT)
        self.wait(2.0)

        self.subscene_5_discuss_top_cube_3()
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.THREE, OUT)
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.THREE, OUT)
        self.wait(2.0)

        self.subscene_5_discuss_top_cube_4()
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.FOUR, OUT)
        puzzle_face_labeller.rotate_cube_ccw_90(PuzzleCubeNumber.FOUR, OUT)
        self.wait(2.0)

        self.subscene_6_conclusion()

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            # self.subscene_1_introduction,
            # self.subscene_2_show_puzzle,
            # self.subscene_3_describe_face_labels,
            # self.subscene_3b_roll_puzzle,
            # self.subscene_4_discuss_matching,
            # self.subscene_4_discuss_front_cube_1,
            # self.subscene_4_discuss_front_cube_2,
            # self.subscene_4_discuss_front_cube_3,
            # self.subscene_4_discuss_front_cube_4,
            # self.subscene_5_discuss_top_cube_1,
            # self.subscene_5_discuss_top_cube_2,
            # self.subscene_5_discuss_top_cube_3,
            # self.subscene_5_discuss_top_cube_4,
            # self.subscene_6_conclusion,
        ]

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene5()
        scene.render()
