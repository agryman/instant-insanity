from manim import *
import numpy as np

from instant_insanity.core.config import PREVIEW_CONFIG, LINEN_CONFIG


class BeziersWithMidpointArrows(Scene):
    """Display several CubicBezier curves with an arrow at each curve's midpoint.

    Each arrow uses a different arrow-tip style (including StealthTip), and the
    style name is shown near the arrow tip. Curves are laid out in a vertical column.
    """

    def construct(self) -> None:
        # Pick a few tip styles (several = 3 here; you can add more)
        tip_styles: list[tuple[str, type]] = [
            ("StealthTip", StealthTip),
            ("ArrowTriangleFilledTip", ArrowTriangleFilledTip),
            ("ArrowTriangleTip", ArrowTriangleTip),
        ]

        # Build some distinct cubic Beziers stacked vertically
        curves: list[VMobject] = []
        y_levels = [2.5, 0.5, -1.5]  # vertical column
        shapes = [
            # (p0, p1, p2, p3) before vertical shift
            (LEFT * 4, LEFT * 1 + UP * 2, RIGHT * 1 + DOWN * 1, RIGHT * 4),
            (LEFT * 4, LEFT * 2 + DOWN * 2, RIGHT * 2 + UP * 3, RIGHT * 4),
            (LEFT * 4, LEFT * 2 + UP * 1, RIGHT * 3 + UP * 1, RIGHT * 4),
        ]

        for (p0, p1, p2, p3), y in zip(shapes, y_levels):
            dy = y * UP
            curve = CubicBezier(p0 + dy, p1 + dy, p2 + dy, p3 + dy,
                                color=BLACK, stroke_width=2)
            curves.append(curve)

        # Helper: build a tiny tangent-aligned arrow at the midpoint (u=0.5)
        def arrow_at_midpoint(curve: VMobject, tip_shape: type, name: str) -> VGroup:
            """Create a short arrow centered at the curve midpoint with a label.

            Args:
                curve: The curve to sample (CubicBezier or any TipableVMobject).
                tip_shape: Arrow tip class (e.g., StealthTip).
                name: Label text to display near the tip.

            Returns:
                A VGroup containing the arrow (Line with tip) and the label.
            """
            u = 0.5
            p = curve.point_from_proportion(u)
            # Small forward step to estimate tangent direction
            du = 1e-3
            q = curve.point_from_proportion(min(1.0, u + du))
            v = q - p
            L = np.linalg.norm(v)
            if L < 1e-9:
                v = RIGHT  # fallback
                L = 1.0
            t_hat = v / L

            # Make a short line centered at p, oriented along t_hat
            half = 0.35  # half-length of the arrow shaft
            a = p - half * t_hat
            b = p + half * t_hat

            arrow = Line(a, b, color=BLACK, stroke_width=2)
            arrow.add_tip(tip_shape=tip_shape, tip_length=0.25)

            # Place the label just off the arrow tip, slightly above
            label = Text(name, font_size=24, color=BLACK)
            # Nudge label near the arrow's end point
            label.move_to(b + 0.25 * UP + 0.15 * t_hat)

            return VGroup(arrow, label)

        # Build arrows/labels for each curve
        arrow_groups: list[VGroup] = []
        for curve, (name, cls) in zip(curves, tip_styles):
            arrow_groups.append(arrow_at_midpoint(curve, cls, name))

        # Painter's algorithm for Cairo: add curves first, then arrows/labels on top
        self.add(*curves, *arrow_groups)
        self.wait(1)

if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = BeziersWithMidpointArrows()
        scene.render()
