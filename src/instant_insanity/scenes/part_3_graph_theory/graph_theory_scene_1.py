from manim import tempconfig
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.scenes.coordinate_grid import GridMixin


class GraphTheoryScene1(GridMixin, VoiceoverScene):
    def say(self, text: str) -> None:
        """
        Says text in the scene.
        Args:
            text: The text to say.
        """
        with self.voiceover(text=text) as tracker:
            voiceover_wait(self, tracker)

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(True)

        self.say("Let's do some graph theory!")

        self.say(
            """In high school, we learn to draw graphs of functions on the familiar x-y coordinate plane. 
            For example, here's the graph of a parabola."""
        )

        self.say("""Mathematicians also use the term graph for another kind of object.
            This second meaning of graph is simply any collection of points
            connected by lines.
            That’s the kind of graph we’ll be talking about in this video.""")


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene1()
        scene.render()
