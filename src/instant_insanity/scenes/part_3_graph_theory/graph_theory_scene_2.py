from manim import Mobject, FadeIn, FadeOut, tempconfig, BLACK, Tex
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.mobjects.image import ImagesPath
from instant_insanity.scenes.coordinate_grid import GridMixin

INTRODUCTION: str = "introduction"
GRAPH_THEORY: str = "graph_theory"
GRAPH_THEORY_LATEX: str = GRAPH_THEORY + ".latex"

class GraphTheoryScene2(GridMixin, VoiceoverScene):
    images_path: ImagesPath = ImagesPath()

    @staticmethod
    def mk_topic(topic: str) -> Mobject:
        mobject: Mobject = Tex(topic, font_size=48, color=BLACK)

        return mobject

    def get_image(self, subpackages: str, filename: str, height: float = 6.0) -> Mobject:
        image: Mobject = self.images_path.get_image(subpackages, filename)
        image.height = height

        return image

    def say(self, text: str) -> None:
        """
        Says text in the scene.
        Args:
            text: The text to say.
        """
        with self.voiceover(text=text) as tracker:
            voiceover_wait(self, tracker)

    def discuss_mobject(self, mobject: Mobject, discussion: str) -> None:
        self.play(FadeIn(mobject))
        self.say(discussion)
        self.play(FadeOut(mobject))

    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        topic: Mobject
        image: Mobject
        discussion: str

        # show the US Patent
        image = self.get_image(GRAPH_THEORY, "us-patent.png")
        discussion = """
        Although released in 1967 by Parker Brothers, Instant Insanity
        had much earlier origins.
        The puzzle was patented in the United States by Frederick Schossow in 1900. 
        Instead of face colours, his puzzle used the playing
        card suit symbols clubs, diamonds, hearts, and spades.
        The puzzle might have originated even earlier in some other country.
        """
        self.discuss_mobject(image, discussion)

        # cite Eureka and show its cover
        image = self.get_image(GRAPH_THEORY, "eureka-cover.png")
        discussion = """
        The ingenious use of graph theory to solve Instant Insanity
        was published in the 1947 issue of Eureka, the Archimedeans' Journal.
        The Archimedeans is the Cambridge University Mathematical Society.
        
        The article was The Coloured Cubes Problem by F. de Carteblanche.
        """
        self.discuss_mobject(image, discussion)

        image = self.get_image(GRAPH_THEORY, "trinity-four-med.jpg")
        discussion = """
        Carteblanche was a pseudonym for a group of Cambridge undergraduates
        known as the Trinity Four who published recreational mathematical articles. 
        They also used the pseudonym Blanche Descartes, who was allegedly married to Carteblanche.
        The group members were Leonard Brooks, Arthur Stone, Cedric Smith, and Bill Tutt.
        Tutt went on to become a legendary codebreaker at Bletchley Park during World War 2 
        and later a highly influential graph theorist.
        """
        self.discuss_mobject(image, discussion)

        image = self.get_image(GRAPH_THEORY, "eureka-page-9.png")
        discussion = """
        Let's look at the article.
        The puzzle was called the Tantalizer at that time and it used the colour orange instead of blue.
        Aside from those minor differences, it was the same as Instant Insanity.
        
        Carteblanche introduced a naming scheme for the cube faces for easy reference.
        These names are given in the table at the bottom of the page.
        We'll use this naming scheme too.

        On closer inspection it turns out that the face colours given in the table are most certainly not those
        actually used in the Tantalizer since they in fact yield two distinct solutions!
        Carteblanche probably just dreamed them up as an example for the article.
        After viewing this video you'll know how to find both solutions.
        """
        self.discuss_mobject(image, discussion)

        # show the table for Instant Insanity
        image = self.get_image(GRAPH_THEORY_LATEX, "instant-insanity-table.png")
        discussion = """
        Here is the face colour table for Instant Insanity.
        In the Carteblanche naming scheme, x labels the front face, x prime labels the back face,
        y labels the right face, y prime labels the left face, z labels the top face, and z prime labels the bottom face.
        Here front, back, right, left, top, and bottom refer to the positions of the faces in some arbitrary
        starting orientation. When you rotate a cube the positions of its faces change but the labels get carried along.
        Similarly, the cube numbers 1, 2, 3, and 4 refer to the positions of the cubes in some arbitrary
        starting order. This order never changes.
        """
        self.discuss_mobject(image, discussion)

        image = self.get_image(GRAPH_THEORY, "eureka-page-10.png")
        discussion = """
        The second page of the article explains the opposite-face graph
        and illustrates it in figure 1. The nodes represent
        the face colours. The edges represent pairs of opposite faces
        and are labelled by the number of the cube they belong to.
        Note that the horizontal edge from W to O should have the label 3.
        Later, we'll explain how to use this graph for solving the puzzle.
        """
        self.discuss_mobject(image, discussion)

        image = self.get_image(GRAPH_THEORY, "eureka-page-11.png")
        discussion = """
        The final page of the article reiterates the claim that the
        solution is effectively unique and states that the chance of
        finding the solution by a random arrangement is one in forty-one thousand four hundred and seventy-two.
        """
        self.discuss_mobject(image, discussion)

        image = self.get_image(INTRODUCTION, "instant-insanity-box-front.png")
        discussion = """
        The Carteblanche claim of forty-one thousand four hundred and seventy-two combinations
        is inconsistent with the claim on the Instant Insanity box
        which states there are eighty-two thousand nine hundred and forty-four combinations.
        The Instant Insanity claim is exactly twice the Carteblanche claim.
        Which number do you think is correct?
        We'll settle this question later.
        """
        self.discuss_mobject(image, discussion)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GraphTheoryScene2()
        scene.render()
