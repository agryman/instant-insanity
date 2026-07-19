from manim import Mobject, FadeIn, FadeOut, tempconfig, BLACK, Tex
from manim_voiceover import VoiceoverScene

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
# from instant_insanity.core.voiceover import voiceover_wait
# from instant_insanity.mobjects.image import ImagesPath
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin

# image subpackages
INTRODUCTION: str = "introduction"
GRAPH_THEORY: str = "graph_theory"
GRAPH_THEORY_LATEX: str = GRAPH_THEORY + ".latex"

class GraphTheoryScene2(GridMixin, DiscussionMixin, VoiceoverScene):
    def construct(self):
        self.set_speech_service(GCPTextToSpeechService())
        self.add_grid(False)

        topic: Mobject
        image: Mobject
        discussion: str

        # show the US Patent
        image = self.get_image("us-patent.png", GRAPH_THEORY)
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
        image = self.get_image("eureka-cover.png", GRAPH_THEORY)
        discussion = """
        The ingenious use of graph theory to solve Instant Insanity
        was published in the 1947 issue of Eureka, the Archimedeans' Journal.
        The Archimedeans is the Cambridge University Mathematical Society.
        
        The article was The Coloured Cubes Problem by F. de Carteblanche.
        """
        self.discuss_mobject(image, discussion)

        image = self.get_image("trinity-four-med.jpg", GRAPH_THEORY)
        discussion = """
        Carteblanche was a pseudonym for a group of Cambridge undergraduates
        known as the Trinity Four who published recreational mathematical articles. 
        They also used the pseudonym Blanche Descartes, who was allegedly married to Carteblanche.
        The group members were Leonard Brooks, Arthur Stone, Cedric Smith, and Bill Tutt.
        Tutt went on to become a legendary codebreaker at Bletchley Park during World War 2.
        He later became a highly influential graph theorist.
        """
        self.discuss_mobject(image, discussion)

        image = self.get_image("eureka-page-9.png", GRAPH_THEORY)
        discussion = """
        Let's look at the article.
        The puzzle was called the Tantalizer at that time and it used the colour orange instead of blue.
        Aside from those minor differences, it was the same as Instant Insanity.
        
        Carteblanche introduced a naming scheme for the cube faces for easy reference.
        These names are given in the table at the bottom of the page.
        We'll use this naming scheme too.
        
        Carteblache says he is not sure that his table matches the commercial version.
        His uncertainty is well founded since his table has two distinct solutions!
        Carteblanche probably just dreamed up the table as an example for the article.
        After viewing this video you'll know how to easily find both solutions.
        """
        self.discuss_mobject(image, discussion)

        # show the table for Instant Insanity
        image = self.get_image("instant-insanity-table.png", GRAPH_THEORY_LATEX)
        discussion = """
        Here is the face colour table for Instant Insanity.
        Carteblache's face-naming scheme is based on imposing x y z axes on each cube
        The x axis points from back to front,
        the y axis points from left to right,
        and the z axis points from bottom to top.
        Each face is perpendicular to the axis given by the face name.
        Primes are added to the back, left, and bottom faces.
        Here front, back, right, left, top, and bottom refer to the positions of the faces in some arbitrary
        starting orientation. 
        When you rotate a cube the positions of its faces change but the labels go along for the ride.
        Similarly, the cube numbers 1, 2, 3, and 4 refer to the positions of the cubes in some arbitrary
        starting order and this order never changes.
        """
        self.discuss_mobject(image, discussion)

        image = self.get_image("eureka-page-10-fig-1.png", GRAPH_THEORY)
        discussion = """
        The second page of the article explains the opposite-face graph
        and illustrates it in figure 1. The nodes represent
        the face colours. The edges represent pairs of opposite faces
        and are labelled by the number of the cube they belong to.
        Note that the horizontal edge from W to O should have the label 3.
        Later, we'll explain how to use this graph for solving the puzzle.
        """
        self.discuss_mobject(image, discussion)

        image = self.get_image("eureka-page-11.png", GRAPH_THEORY)
        discussion = """
        The final page of the article reiterates the claim that the
        solution is effectively unique and states that the chance of
        finding the solution by a random arrangement is one in forty-one thousand four hundred and seventy-two.
        This is another way of saying that there are forty-one thousand four hundred and seventy-two combinations.
        """
        self.discuss_mobject(image, discussion)

        image = self.get_image("instant-insanity-box-front.png", INTRODUCTION)
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
