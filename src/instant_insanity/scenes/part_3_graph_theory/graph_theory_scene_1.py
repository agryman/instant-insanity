from manim import tempconfig, Mobject
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.mobjects.image import IMAGES_BASE_PATH, ImagesPath
from instant_insanity.scenes.coordinate_grid import GridMixin


class GraphTheoryScene1(GridMixin, VoiceoverScene):
    images_path: ImagesPath = ImagesPath()
    subpackages: str = "graph_theory.latex"

    def get_image(self, filename: str) -> Mobject:
        image: Mobject = self.images_path.get_image(self.subpackages, filename)

        return image

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
        self.add_grid(False)

        fade_duration: float = 1.0
        pause_duration: float = 1.0

        self.say(
            """Let's get started with some graph theory!
            We'll begin with some terminology.
            Mathematicians often give the same name to different things
            and different names to the same thing.
            This holds for the name "graph".
            It is used for two different things.
            """
        )
        self.wait(duration=pause_duration)

        image: Mobject = self.get_image("parabola-graph.png")
        image.height = 6.0
        self.add(image)
        self.say(
            """In high school we learn that a graph is an x-y plot of a function or relation.
            For example, here's the graph of the function y equals x squared which forms a parabola.
            This kind of graph is not the subject of graph theory.
            """
        )
        self.wait(duration=pause_duration)
        self.remove(image)

        image = self.get_image("example-simple-graph.png")
        self.add(image)
        self.say("""Mathematicians also give the name "graph" to any collection of points
            interconnected by lines.
            For example, here's a small graph that has five points and four lines.
            Every line must begin on some point and must end on some point.
            This is the kind of graph that is the subject of graph theory and the topic of this video.
            """)
        self.wait(duration=pause_duration)
        self.remove(image)

        image = self.get_image("example-crossover-graph.png")
        self.add(image)
        self.say("""We regard two graphs as being essentially the same if they contain the same number of points
        and those points are interconnected in the same way. 
        The positions of the points and the routes taken by the lines
        just define a particular layout of the graph. 
        The layout of a graph is not an essential property of the graph.
        We can lay out a graph in many different ways. 
        We usually use a layout that makes the structure of the graph easier to understand. 
        
        For example, here is another layout the previous graph. 
        This layout is less clear because two lines cross each other.""")

        self.wait(duration=pause_duration)
        self.remove(image)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene1()
        scene.render()
