import importlib
import manim_voiceover
print("manim-voiceover:", manim_voiceover.__version__)
for mod in ("openai_whisper", "whisper"):
    spec = importlib.util.find_spec(mod)
    print(f"{mod} present? ", bool(spec))
