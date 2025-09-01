from manim import Text, Write, UP, MathTex, tempconfig
from manim_voiceover import VoiceoverScene
from instant_insanity.core.google_cloud_tts_service import GCPTextToSpeechService
from instant_insanity.core.config import PREVIEW_CONFIG

class GCPTTSVoiceoverDemo(VoiceoverScene):
    def construct(self):
        # Initialize the GCP TTS service
        self.set_speech_service(GCPTextToSpeechService())

        # Create some text
        title = Text("Hello from Manim!", font_size=48)

        # Add voiceover
        with self.voiceover(text="Welcome to this mathematics explanation video!"):
            self.play(Write(title))
            self.wait(1)

        with self.voiceover(text="Let's explore some interesting mathematical concepts together."):
            self.play(title.animate.shift(UP * 2))

            # Add some mathematical content
            formula = MathTex(r"e^{i\pi} + 1 = 0")
            self.play(Write(formula))
            self.wait(1)


# Example usage:
if __name__ == "__main__":
    with tempconfig(PREVIEW_CONFIG):
        scene = GCPTTSVoiceoverDemo()
        scene.render()
