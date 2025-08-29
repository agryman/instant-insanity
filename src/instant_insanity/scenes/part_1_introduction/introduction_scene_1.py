from dataclasses import dataclass
from pathlib import Path

from manim import ValueTracker, always_redraw, Tex, BLACK, UP, DOWN, LEFT, Mobject, SVGMobject, ImageMobject, tempconfig
from manim_voiceover import VoiceoverScene

from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.config import LINEN_CONFIG

IMAGE_PATH = "~/Documents/repositories/GitHub/agryman/instant-insanity/notebooks/images/scenes/part_1_introduction/"

@dataclass
class PuzzleInfo:
    """Information about a puzzle."""
    name: str
    voiceover: str
    year: int
    image_filename: str
    image_attribution: str
    image_height: float


class IntroductionScene1(VoiceoverScene):
    def construct(self):
        # Set up the Google TTS service
        self.set_speech_service(GCPTextToSpeechService())

        # Define the path to images
        image_path = Path(IMAGE_PATH).expanduser()

        wordle_info: PuzzleInfo = PuzzleInfo(
            name='Wordle',
            voiceover='Before Wordle...',
            year=2021,
            image_filename='wordle-cropped.png',
            image_attribution='© 2025 The New York Times Company',
            image_height=4.0,
        )

        sudoku_info: PuzzleInfo = PuzzleInfo(
            name='Sudoku',
            voiceover='...before Sudoku...',
            year=1986,
            image_filename='sudoku-cropped.png',
            image_attribution='© 2025 The New York Times Company',
            image_height=4.0,
        )

        rubiks_cube_info: PuzzleInfo = PuzzleInfo(
            name="Rubik's Cube",
            voiceover="...before Rubik's Cube...",
            year=1974,
            image_filename="Rubik's_cube.svg",
            image_attribution='image by Booyabazooka, CC BY-SA 3.0',
            image_height=4.0,
        )

        instant_insanity_info: PuzzleInfo = PuzzleInfo(
            name="Instant Insanity",
            voiceover="""
            ...there was Instant Insanity.
            ...
            Released in 1967 by Parker Brothers, Instant Insanity became a craze.
            Millions of copies were sold, including one to a certain high school student named Arthur.
            """,
            year=1967,
            image_filename='winning-moves-instant-insanity-cubes_linen.png',
            image_attribution='winning-moves.com',
            image_height=2.0,
        )

        info_list: list[PuzzleInfo] = [
            wordle_info,
            sudoku_info,
            rubiks_cube_info,
            instant_insanity_info,
        ]

        # Create a ValueTracker for the year, starting at 2025
        year_tracker = ValueTracker(2025)

        # Create the year text that updates based on the tracker (BLACK text for LINEN background)
        year_text = always_redraw(
            lambda: Tex(str(int(year_tracker.get_value())),
                        font_size=72,
                        color=BLACK)
            .to_edge(UP, buff=1.0)
        )

        # Display the initial year
        self.add(year_text)
        self.wait(1.0)

        info: PuzzleInfo
        for info in info_list:
            filename: str = info.image_filename
            full_path: Path = image_path / filename
            image: Mobject
            if filename.endswith('.svg'):
                image = SVGMobject(full_path)
            else:
                image = ImageMobject(full_path)
            image.height = info.image_height

            name: Tex = Tex(info.name,
                              font_size=48,
                              color=BLACK)

            attribution: Tex = Tex(info.image_attribution,
                                     font_size=14,
                                     color=BLACK)

            # leave the image centered in the frame and position the name and attribution
            name.to_edge(DOWN, buff=1.0)
            attribution.to_corner(DOWN + LEFT, buff=0.25)

            with self.voiceover(text=info.voiceover) as tracker:

                self.add(name)
                self.add(image)
                self.add(attribution)

                name.set_opacity(0)
                image.set_opacity(0)
                attribution.set_opacity(0)

                self.play(year_tracker.animate.set_value(info.year),
                          name.animate.set_opacity(1),
                          image.animate.set_opacity(1),
                          attribution.animate.set_opacity(1),
                          run_time=1.0)

                # self.wait(1)

                # leave the last item on screen, else fade out
                if info == info_list[-1]:
                    self.wait(2.0)
                else:
                    self.play(name.animate.set_opacity(0),
                              attribution.animate.set_opacity(0),
                              image.animate.set_opacity(0),
                              run_time=1.0)

                    self.remove(name)
                    self.remove(image)
                    self.remove(attribution)


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = IntroductionScene1()
        scene.render()