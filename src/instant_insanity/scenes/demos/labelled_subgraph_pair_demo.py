from manim import tempconfig
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.puzzle import WINNING_MOVES_PUZZLE, Puzzle
from instant_insanity.mobjects.labelled_subgraph import LabelledSubgraphPair
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.subscene import SubsceneMixin


class LabelledSubgraphPairDemo(GridMixin, SubsceneMixin, DiscussionMixin, VoiceoverScene):

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        puzzle: Puzzle = WINNING_MOVES_PUZZLE
        labelled_subgraph_pair = LabelledSubgraphPair(puzzle)
        labelled_subgraph_pair.add_solution_edges()

        labelled_subgraph_pair.add_to_scene(self)
        labelled_subgraph_pair.add_edge_directions(self)

        self.wait(3.0)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = LabelledSubgraphPairDemo()
        scene.render()
