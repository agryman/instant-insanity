from manim import *
from instant_insanity.core.config import PREVIEW_CONFIG

class TransformVsReplacement(Scene):
    """Demonstrate the difference between Transform and ReplacementTransform.

    Left:  Transform(poly1, dot1)
        - poly1 keeps its identity (class and id) and remains in the scene.
        - dot1 is not added to the scene (used only as target geometry/style).

    Right: ReplacementTransform(poly2, dot2)
        - poly2 is removed from the scene at the end.
        - dot2 is added to the scene and remains (its identity is preserved).
    """

    def construct(self):
        # Left pair (Transform)
        poly1 = Polygon([-2, -1, 0], [0, 1.5, 0], [2, -1, 0],
                        color=BLUE, fill_opacity=0.4).shift(LEFT * 3.5)
        dot1 = Dot(point=poly1.get_center(), radius=0.2, color=BLUE)

        # Right pair (ReplacementTransform)
        poly2 = Polygon([-2, -1, 0], [0, 1.5, 0], [2, -1, 0],
                        color=GREEN, fill_opacity=0.4).shift(RIGHT * 3.5)
        dot2 = Dot(point=poly2.get_center(), radius=0.2, color=GREEN)

        # Labels
        label_left = MathTex(r"\text{Transform}").next_to(poly1, UP, buff=0.5)
        label_right = MathTex(r"\text{ReplacementTransform}").next_to(poly2, UP, buff=0.5)

        self.add(poly1, poly2, label_left, label_right)

        # Print BEFORE state
        print("\n--- BEFORE ---")
        print(f"poly1: id={id(poly1)}, type={type(poly1).__name__}, in scene? {poly1 in self.mobjects}")
        print(f"dot1 : id={id(dot1)},  type={type(dot1).__name__},  in scene? {dot1 in self.mobjects}")
        print(f"poly2: id={id(poly2)}, type={type(poly2).__name__}, in scene? {poly2 in self.mobjects}")
        print(f"dot2 : id={id(dot2)},  type={type(dot2).__name__},  in scene? {dot2 in self.mobjects}")

        self.wait(0.5)

        # Run both animations in parallel
        self.play(
            Transform(poly1, dot1),                 # morph poly1, keep identity
            ReplacementTransform(poly2, dot2),      # replace poly2 with dot2
            run_time=2
        )

        self.wait(0.3)

        # Print AFTER state
        print("\n--- AFTER ---")
        print(f"poly1: id={id(poly1)}, type={type(poly1).__name__}, in scene? {poly1 in self.mobjects}")
        print(f"dot1 : id={id(dot1)},  type={type(dot1).__name__},  in scene? {dot1 in self.mobjects}")
        print(f"poly2: id={id(poly2)}, type={type(poly2).__name__}, in scene? {poly2 in self.mobjects}")
        print(f"dot2 : id={id(dot2)},  type={type(dot2).__name__},  in scene? {dot2 in self.mobjects}")

        # Visual pause
        self.wait(0.7)

if __name__ == "__main__":
    with tempconfig(PREVIEW_CONFIG):
        scene = TransformVsReplacement()
        scene.render()
