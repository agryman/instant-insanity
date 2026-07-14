from manim import tempconfig, RIGHT, DOWN, ORIGIN, FadeIn, FadeOut
from manim_voiceover import VoiceoverScene, VoiceoverTracker

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.puzzle import WINNING_MOVES_PUZZLE
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.mobjects.opposite_face_graph import OppositeFaceGraph, EdgeToSubgraphMapping
from instant_insanity.scenes.coordinate_grid import GridMixin


class OppositeFaceGraphDemo(GridMixin, VoiceoverScene):

    def construct(self):
        # Set up the Google TTS service
        self.set_speech_service(GCPTextToSpeechService())

        # enable the grid to determine positioning coordinates
        self.add_grid(False)

        # create the full Winning Moves opposite-face graph
        full_subgraph: EdgeToSubgraphMapping = OppositeFaceGraph.mk_subgraph_for_flag(True)
        wm_graph: OppositeFaceGraph = OppositeFaceGraph(WINNING_MOVES_PUZZLE, ORIGIN)
        wm_graph.set_subgraph(full_subgraph)

        self.play(FadeIn(wm_graph))
        tracker: VoiceoverTracker
        with self.voiceover(text="""
        Here's the opposite-face graph for the Winning Moves version of Instant Insanity.
        """) as tracker:
            # keep the image on screen for at least MIN_VOICEOVER_DURATION seconds
            # elapsed: float = tracker.duration - tracker.get_remaining_duration()
            # self.safe_wait(MIN_VOICEOVER_DURATION - elapsed)
            voiceover_wait(self, tracker)

        self.wait(3.0)
        self.play(FadeOut(wm_graph))

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = OppositeFaceGraphDemo()
        scene.render()
