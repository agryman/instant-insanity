"""
This module animates the conversion of the subgraphs into a solution of the puzzle.
The scene starts with the two subgraphs on the bottom half the of the frame and nothing
in the top half. The state of the scene is determined by the puzzle and the solution number.
Recall that Carteblanche's puzzle has two solutions.
"""
from typing import cast

from manim import Scene, tempconfig, LEFT, DOWN, RIGHT, Tex, BLACK, FadeIn, PI
from manim.typing import Point3D, Vector3D
from manim_voiceover import VoiceoverScene

from instant_insanity.animators.puzzle_3d_animators import Puzzle3DSetCubeGapAnimorph, Puzzle3DCubeRotationAnimorph
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.cube import FacePlane
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.projection import Projection, mk_standard_orthographic_projection
from instant_insanity.core.puzzle import Puzzle, WINNING_MOVES_PUZZLE, PuzzleCubeNumber, AxisLabel, PuzzleSpec, \
    WINNING_MOVES_PUZZLE_SPEC
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, EdgeToSubgraphMapping, mk_edge_directions
from instant_insanity.mobjects.puzzle_3d import Puzzle3D, DEFAULT_BUFF
from instant_insanity.mobjects.stealth_tip import CubeEdgeTip
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.helpers import morph_and_checkpoint
from instant_insanity.scenes.part_3_graph_theory.graph_theory_scene_3 import GraphTheoryScene3
from instant_insanity.solvers.graph_solver import GraphSolver, Grid, GridValue


class GraphTheoryScene5(GridMixin, DiscussionMixin, VoiceoverScene):
    playlist: list[object]
    puzzle: Puzzle
    start_centre: Point3D
    end_centre: Point3D

    def skip(self, method: object) -> bool:
        return len(self.playlist) > 0 and method not in self.playlist

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)
        self.playlist = [
        ]

        puzzle: Puzzle =  WINNING_MOVES_PUZZLE
        front_graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, 4 * LEFT + 1.5 * DOWN)
        top_graph: OppositeFaceGraph = OppositeFaceGraph(puzzle, 4 * RIGHT + 1.5 * DOWN)

        subgraphs: dict[FacePlane, OppositeFaceGraph] = {
            FacePlane.FRONT: front_graph,
            FacePlane.TOP: top_graph,
        }

        front_text: Tex = Tex(r"front $\rightarrow$ back", color=BLACK, font_size=36)
        top_text: Tex = Tex(r"top $\rightarrow$ bottom", color=BLACK, font_size=36)

        front_text.next_to(front_graph, DOWN, buff=0.75)
        top_text.next_to(top_graph, DOWN, buff=0.75)

        self.add(front_graph, top_graph, front_text, top_text)

        graph_solver: GraphSolver = GraphSolver(puzzle)
        graph_solver.solve()
        solution: Grid = graph_solver.solutions[0]

        # compute the edges in the solution of each subgraph.
        for face_name, graph in subgraphs.items():
            edge_to_subgraph: EdgeToSubgraphMapping = graph.edge_to_subgraph.copy()
            for cube_number in PuzzleCubeNumber:
                grid_value: GridValue = solution[(face_name, cube_number)]
                assert isinstance(grid_value, AxisLabel)
                axis_label: AxisLabel = grid_value
                edge_to_subgraph[(cube_number, axis_label)] = True
            graph.set_subgraph(edge_to_subgraph)

        # assign directions to the edges of the subgraphs
        subgraph: OppositeFaceGraph
        for subgraph in (front_graph, top_graph):
            cube_edge_tips: CubeEdgeTip = mk_edge_directions(subgraph)
            for edge_tip in cube_edge_tips.values():
                self.add(edge_tip.tip)

        # wait to force a redraw of the final frame of the previous scene
        self.wait(0.5)

        voiceover: str = """
        The final step of the process is to convert these subgraphs
        into cube orientations which, by construction, will solve the puzzle.
        """
        self.say(voiceover)

        # create and display the 3D puzzle
        self.wait(0.5)
        projection: Projection = mk_standard_orthographic_projection()
        puzzle3d: Puzzle3D = GraphTheoryScene3.mk_puzzle3d(puzzle, projection)
        self.add(puzzle3d)
        self.wait(0.5)
        voiceover = """
        Here's the puzzle with its cubes in their starting positions.
        Recall that this arrangement is not a solution.
        Let's rotate it to confirm that some sides have repeated colours.
        """
        self.say(voiceover)

        initial_gap: float = puzzle3d.get_cube_gap()

        # contract the puzzle
        min_gap: float = DEFAULT_BUFF
        contract_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(puzzle3d, min_gap)
        morph_and_checkpoint(self, contract_animorph)

        # rotate the puzzle
        rotation: Vector3D = cast(Vector3D, RIGHT * PI / 2.0)
        rotation_animorph: Puzzle3DCubeRotationAnimorph = Puzzle3DCubeRotationAnimorph(puzzle3d, rotation)
        for _ in range(4):
            morph_and_checkpoint(self, rotation_animorph)

        # expand the puzzle
        expand_animorph: Puzzle3DSetCubeGapAnimorph = Puzzle3DSetCubeGapAnimorph(puzzle3d, initial_gap)
        morph_and_checkpoint(self, expand_animorph)

        voiceover = """
        The starting position for each cube has 
        the face labelled x on the front,
        y on the right, and z on the top.
        """
        self.say(voiceover)

        voiceover = """
        We need to rotate each cube to match the subgraphs.
        We'll match the front-back subgraph first and 
        then match the top-bottom subgraph.
        For each subgraph, we'll match one cube at a time.
        """

        voiceover = """
        Let's start with cube 1 in the front-back subgraph. 
        Look for the edge labelled 1x which connects green to white.
        The starting position for each cube has its face labelled x
        facing front. Therefore, the starting position of cube 1
        already matches the front-back subgraph. No further rotation is needed.
        """
        self.say(voiceover)

        voiceover = """
        Next consider cube 2. It's front-back edge is labelled 2x which
        also matches its starting position. Therefore, no further rotation is needed.
        """
        self.say(voiceover)

        voiceover = """
        Now look at cube 3. It's front-back edge is labelled 3y so we
        need to rotate the right face into the front position.
        """
        self.say(voiceover)

        # rotate cube 3 90 degrees about the DOWN axis.

        voiceover = """
        Wrapping up the front-back subgraph, we see that the cube 4 edge
        is labelled 4x, which is its starting position. No rotation is needed.
        """
        self.say(voiceover)

        voiceover = """
        At this point we have half of a solution since no colour is repeated
        on the front and back sides.
        """

        # TO DO: rotate the puzzle twice be 180 degrees, pausing.

        voiceover = """
        Now let's work on the top-bottom subgraph. 
        The edge for cube 1 is labelled 1y.
        Rotate the right face to the top.
        """
        self.say(voiceover)

        # TO DO: rotate cube 1 by 90 degrees about OUT

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene5()
        scene.render()
