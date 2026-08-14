from dataclasses import dataclass

from manim import ValueTracker, always_redraw, Tex, BLACK, UP, DOWN, LEFT, Mobject, tempconfig, Text
from manim_voiceover import VoiceoverScene, VoiceoverTracker
from manim_voiceover.services.recorder import RecorderService

from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.voiceover import voiceover_wait
from instant_insanity.mobjects.image import ImagesPath, WORDLE_SOURCE, SUDOKU_SOURCE, RUBIKS_CUBE_SOURCE, \
    INSTANT_INSANITY_SOURCE
from instant_insanity.scenes.coordinate_grid import GridMixin
from instant_insanity.scenes.discussion import DiscussionMixin
from instant_insanity.scenes.subscene import SubsceneMixin

# Wait time between puzzles
WAIT_BETWEEN_PUZZLES_DURATION: float = 0.5

# Fade-in and Fade-out duration
FADE_DURATION: float = 0.5

IMAGES_SUBPACKAGE = 'introduction'


@dataclass
class PuzzleInfo:
    """Information about a puzzle."""
    name: str
    voiceover: str
    year: int
    image_filename: str
    image_attribution: str
    image_height: float


class IntroductionScene1(DiscussionMixin, GridMixin, SubsceneMixin, VoiceoverScene):
    def construct(self):
        # Set up the Google TTS service
        # self.set_speech_service(GCPTextToSpeechService())
        self.set_speech_service(RecorderService(transcription_model=None))

        self.add_grid(False)

        wordle_info: PuzzleInfo = PuzzleInfo(
            name='Wordle',
            voiceover='Before Wordle,',
            year=2021,
            image_filename='wordle-cropped.png',
            image_attribution=WORDLE_SOURCE,
            image_height=4.0,
        )

        sudoku_info: PuzzleInfo = PuzzleInfo(
            name='Sudoku',
            voiceover='before Sudoku,',
            year=1986,
            image_filename='sudoku-cropped.png',
            image_attribution=SUDOKU_SOURCE,
            image_height=4.0,
        )

        rubiks_cube_info: PuzzleInfo = PuzzleInfo(
            name="Rubik's Cube",
            voiceover="before Rubik's Cube,",
            year=1974,
            image_filename="Rubik's_cube.svg",
            image_attribution=RUBIKS_CUBE_SOURCE,
            image_height=4.0,
        )

        instant_insanity_info: PuzzleInfo = PuzzleInfo(
            name="Instant Insanity",
            voiceover="""
            there was Instant Insanity!
            ...
            Released in 1967 by Parker Brothers, Instant Insanity became a craze.
            Millions of copies were sold, 
            including one to a certain Northview Heights high school student named Arthur.
            """,
            year=1967,
            image_filename='winning-moves-instant-insanity-cubes_linen.png',
            image_attribution=INSTANT_INSANITY_SOURCE,
            image_height=2.0,
        )

        info_list: list[PuzzleInfo] = [
            wordle_info,
            sudoku_info,
            rubiks_cube_info,
            instant_insanity_info,
        ]

        # Create a ValueTracker for the year, starting at the first image
        year_tracker = ValueTracker(info_list[0].year)

        # Create the year text that updates based on the tracker (BLACK text for LINEN background)
        year_text = always_redraw(
            lambda: Tex(str(int(year_tracker.get_value())),
                        font_size=72,
                        color=BLACK)
            .to_edge(UP, buff=1.0)
        )

        # Display the initial year
        self.add(year_text)

        images_path: ImagesPath = ImagesPath()
        info: PuzzleInfo
        for info in info_list:
            image: Mobject = images_path.get_image(IMAGES_SUBPACKAGE, info.image_filename)
            image.height = info.image_height

            name: Tex = Tex(info.name, font_size=48, color=BLACK)

            # leave the image centered in the frame and position the name
            name.to_edge(DOWN, buff=1.0)

            start_opacity: float = 1.0 if info == info_list[0] else 0.0

            name.set_opacity(start_opacity)
            image.set_opacity(start_opacity)
            attribution: Text = self.mk_attribution(info.image_attribution, start_opacity=start_opacity)

            self.add(name)
            self.add(image)
            self.add(attribution)

            if info == info_list[0]:
                # show the first image then wait
                self.wait(WAIT_BETWEEN_PUZZLES_DURATION)
            else:
                # fade in the puzzle and turn back the year
                self.play(year_tracker.animate.set_value(info.year),
                          name.animate.set_opacity(1),
                          image.animate.set_opacity(1),
                          attribution.animate.set_opacity(1),
                          run_time=FADE_DURATION)

            tracker: VoiceoverTracker
            with self.voiceover(text=info.voiceover) as tracker:
                # keep the image on screen for at least MIN_VOICEOVER_DURATION seconds
                # elapsed: float = tracker.duration - tracker.get_remaining_duration()
                # self.safe_wait(MIN_VOICEOVER_DURATION - elapsed)
                voiceover_wait(self, tracker)

            # leave the last item on screen, else fade out
            if info == info_list[-1]:
                self.wait(WAIT_BETWEEN_PUZZLES_DURATION)
            else:
                # fade out the puzzle
                self.play(name.animate.set_opacity(0),
                          attribution.animate.set_opacity(0),
                          image.animate.set_opacity(0),
                          run_time=FADE_DURATION)

                self.remove(name)
                self.remove(image)
                self.remove(attribution)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = IntroductionScene1()
        scene.render()