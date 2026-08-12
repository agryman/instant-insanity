"""
This module defines the DiscussionMixin class which is intended for use
with VoiceoverScene.
"""
from manim import Mobject, Tex, BLACK, FadeIn, FadeOut, Scene, ManimColor, ImageMobject, Rectangle, VMobject, config, \
    Difference, RED, Group, DOWN, LEFT, Text
from manim_voiceover import VoiceoverScene, VoiceoverTracker

import numpy as np

from instant_insanity.core.image_region import Region, find_red_rectangle
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.mobjects.image import ImagesPath

# the path to the images resource directory in the package
IMAGES_PATH: ImagesPath = ImagesPath()

# Default image height
IMAGE_HEIGHT: float = 6.0

# the image height in scene units when the whole page is shown
PAGE_HEIGHT: float = 7.0

# the fraction of the frame that the zoomed region is allowed to occupy
ZOOM_FILL: float = 0.85

# how much larger than the frame the mask is, so that it still covers the frame
# after it has been scaled and shifted
MASK_SCALE: float = 8.0


class DiscussionMixin:
    """
    Inherit this mixin class with VoiceoverScene to create topics and images
    and then discuss them.
    """
    @staticmethod
    def mk_attribution(source: str, start_opacity: float= 1.0) -> Text:
        attribution: Text = Text(source, font_size=10, font="Monospace", color=BLACK)
        attribution.to_corner(DOWN + LEFT, buff=0.25)
        attribution.set_opacity(start_opacity)

        return attribution

    @staticmethod
    def get_image(filename: str, subpackages: str = "", height: float = IMAGE_HEIGHT) -> Mobject:
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

    def discuss_mobject(self, mobject: Mobject, discussion: str, source: str = "") -> None:
        """
        This method fades in a mobject, discusses it, and then fades it out.
        """
        attribution: Text = self.mk_attribution(source)

        assert isinstance(self, Scene)
        self.add(attribution)
        self.play(FadeIn(mobject))

        assert isinstance(self, DiscussionMixin)
        self.say(discussion)

        assert isinstance(self, Scene)
        self.play(FadeOut(mobject))
        self.remove(attribution)

    @staticmethod
    def mk_region_rect(image: ImageMobject, region: Region, **kwargs) -> Rectangle:
        """
        Makes a rectangle that bounds a region of an image.

        The region is given in image coordinates, namely fractions of the image
        width and height, with the origin in the top-left corner of the image.
        This lets the region be read off an annotated copy of the image without
        knowing where the image sits in the scene or how big it is.

        Args:
            image: the image.
            region: the region of interest.
            kwargs: passed to Rectangle, e.g. stroke_color.

        Returns:
            The bounding rectangle of the region, in scene coordinates.
        """
        u0, v0, u1, v1 = region

        width: float = image.width
        height: float = image.height
        left: float = image.get_left()[0]
        top: float = image.get_top()[1]

        x0: float = left + u0 * width
        x1: float = left + u1 * width

        # image coordinates increase downwards, but scene coordinates increase upwards
        y0: float = top - v0 * height
        y1: float = top - v1 * height

        rect: Rectangle = Rectangle(width=x1 - x0, height=y0 - y1, **kwargs)
        rect.move_to(np.array([(x0 + x1) / 2.0, (y0 + y1) / 2.0, 0.0]))

        return rect

    @staticmethod
    def mk_spotlight_mask(rect: Rectangle,
                          color: ManimColor | None = None,
                          opacity: float = 1.0) -> VMobject:
        """
        Makes a mask that covers the whole frame except for a rectangular region.

        The mask is a large rectangle with the region punched out of it. Add it on
        top of an image and fade it in to conceal everything outside the region.

        Args:
            rect: the region to leave uncovered.
            color: the mask colour, which defaults to the background colour.
            opacity: the mask opacity. Use 1.0 to conceal the rest of the image
                completely, or something like 0.9 to leave a ghost of it.

        Returns:
            The mask.
        """
        if color is None:
            color = ManimColor(config.background_color)

        outer: Rectangle = Rectangle(width=MASK_SCALE * config.frame_width,
                                     height=MASK_SCALE * config.frame_height)

        mask: VMobject = Difference(outer, rect,
                                    fill_color=color,
                                    fill_opacity=opacity,
                                    stroke_width=0.0)

        return mask

    @staticmethod
    def mk_zoom_scale(rect: Rectangle, fill: float = ZOOM_FILL) -> float:
        """
        Computes the scale factor that makes a region as large as it can be while
        still fitting inside the frame.

        Args:
            rect: the region.
            fill: the fraction of the frame that the region may occupy.

        Returns:
            The scale factor.
        """
        return min(fill * config.frame_width / rect.width,
                   fill * config.frame_height / rect.height)


    def discuss_and_zoom_image(
            self,
            subpackages: str,
            image_filename: tuple[str, str],
            image_height: float,
            image_voiceover: str,
            annotated_filenames: list[str],
            annotated_voiceovers: list[str]
    ) -> None:
        assert isinstance(self, VoiceoverScene)
        filename: str
        source: str
        filename, source = image_filename
        image: Mobject = self.get_image(filename, subpackages, height=image_height)
        assert isinstance(image, ImageMobject)

        attribution: Tex = self.mk_attribution(source)
        self.add(attribution)
        self.play(FadeIn(image, run_time=0.5))
        self.say(image_voiceover)

        annotated_filename: str
        annotated_voiceover: str
        for annotated_filename, annotated_voiceover in zip(annotated_filenames, annotated_voiceovers):
            # read the region of interest off the annotated copy of the page
            region: Region = find_red_rectangle(
                IMAGES_PATH.open_image(subpackages, annotated_filename))

            # frame the region of interest
            rect: Rectangle = self.mk_region_rect(image, region,
                                             stroke_color=RED,
                                             stroke_width=2.0)
            self.play(FadeIn(rect, run_time=0.5))

            # conceal everything outside the region
            mask: VMobject = self.mk_spotlight_mask(rect)
            self.add(mask)
            self.play(FadeIn(mask, run_time=0.5))

            # scale the image, the mask, and the frame together so that the hole in
            # the mask stays over the same part of the image
            group: Group = Group(image, mask, rect)
            center: np.ndarray = rect.get_center()
            scale: float = self.mk_zoom_scale(rect)
            self.play(group.animate.scale(scale, about_point=center).shift(-center))

            self.say(annotated_voiceover)

            # reverse the zoom and reveal the whole page again
            self.play(group.animate.shift(center).scale(1.0 / scale, about_point=center))
            self.play(FadeOut(mask), FadeOut(rect))

        # conceal the main image
        self.play(FadeOut(image, run_time=0.5))
        self.remove(attribution)
