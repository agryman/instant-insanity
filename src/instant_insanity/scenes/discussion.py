"""
This module defines the DiscussionMixin class which is intended for use
with VoiceoverScene.
"""
from manim import Mobject, Tex, BLACK, FadeIn, FadeOut, Scene, ManimColor
from manim_voiceover import VoiceoverScene, VoiceoverTracker

from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.mobjects.image import ImagesPath

IMAGES_PATH: ImagesPath = ImagesPath()


class DiscussionMixin:
    """
    Inherit this mixin class with VoiceoverScene to create topics and images
    and then discuss them.
    """
    @staticmethod
    def get_image(filename: str, subpackages: str = "", height: float = 6.0) -> Mobject:
        """

        Args:
            filename: the image filename.
            subpackages: the subpackages name.
            height: the image height.

        Returns:
            The image object.
        """
        image: Mobject = IMAGES_PATH.get_image(subpackages, filename)
        image.height = height

        return image

    @staticmethod
    def mk_topic(topic: str, font_size: float = 48, color: ManimColor = BLACK) -> Mobject:
        """

        Args:
            topic: The topic text.
            font_size: The font size.
            color: The colour.

        Returns:
            A Tex object.

        """
        mobject: Mobject = Tex(topic, font_size=font_size, color=color)

        return mobject

    def say(self, text: str) -> None:
        """
        Says text in the scene.
        Args:
            text: The text to say.
        """
        tracker: VoiceoverTracker
        assert isinstance(self, VoiceoverScene)
        with self.voiceover(text=text) as tracker:
            voiceover_wait(self, tracker)

    def discuss_mobject(self, mobject: Mobject, discussion: str) -> None:
        """
        This method fades in a mobject, discusses it, and then fades it out.
        """
        assert isinstance(self, Scene)
        self.play(FadeIn(mobject))

        assert isinstance(self, DiscussionMixin)
        self.say(discussion)

        assert isinstance(self, Scene)
        self.play(FadeOut(mobject))
