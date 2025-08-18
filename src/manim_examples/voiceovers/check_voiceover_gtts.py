from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from manim import Text, WHITE, tempconfig

from instant_insanity.core.config import LINEN_CONFIG

class Demo(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="en"), create_subcaption=False)
        with self.voiceover(text="Hello from Manim Voiceover without Whisper.") as tracker:
            self.play(Text("Hello", color=WHITE).animate.scale(1.2))
            self.wait(tracker.get_remaining_duration())
        self.wait(4)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = Demo()
        scene.render()
    print("OK")
