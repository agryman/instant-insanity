from typing import Type
import numpy as np
from manim import *

from instant_insanity.core.config import LINEN_CONFIG


class BeziersWithEndpointArrows(Scene):
    """Display several CubicBezier curves with dots at ends and arrow tips pointing into the end."""

    def construct(self) -> None:
        """Build the scene.

        Notes:
            - Uses BLACK for strokes/text on a linen background (via LINEN_CONFIG in the preview snippet).
            - Arrow tips are placed so that their points touch the first-contact point on the end dot's perimeter.
            - Tangent direction is computed from the curve near u = 1.0 to determine inward direction.
        """
        DOT_RADIUS: float = 0.08

        tip_styles: list[tuple[str, Type[ArrowTip]]] = [
            ('StealthTip', StealthTip),
            ('ArrowTriangleFilledTip', ArrowTriangleFilledTip),
            ('ArrowTriangleTip', ArrowTriangleTip),
        ]

        y_levels: list[float] = [2.5, 0.5, -1.5]

        shapes: list[tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]] = [
            (LEFT * 4, LEFT * 1 + UP * 2, RIGHT * 1 + DOWN * 1, RIGHT * 4),
            (LEFT * 4, LEFT * 2 + DOWN * 2, RIGHT * 2 + UP * 3, RIGHT * 4),
            (LEFT * 4, LEFT * 2 + UP * 1, RIGHT * 3 + UP * 1, RIGHT * 4),
        ]

        curves: list[VMobject] = []
        for (p0, p1, p2, p3), y in zip(shapes, y_levels):
            dy: np.ndarray = y * UP
            curve: VMobject = CubicBezier(
                p0 + dy, p1 + dy, p2 + dy, p3 + dy,
                color=BLACK,
                stroke_width=2,
            )
            curves.append(curve)

        def arrow_at_end(curve: VMobject, tip_shape: Type[ArrowTip], name: str) -> VGroup:
            """Create an inward-pointing arrow tip at the curve's end and a nearby label.

            Args:
                curve: The curve to annotate.
                tip_shape: The Manim arrow tip style class to use.
                name: The label text to display near the tip.

            Returns:
                A VGroup containing the (shaftless) arrow and its label.
            """
            u_end: float = 1.0
            end_point: np.ndarray = curve.point_from_proportion(u_end)

            u_before: float = 1.0 - 1e-3
            before_point: np.ndarray = curve.point_from_proportion(u_before)

            tangent: np.ndarray = before_point - end_point
            L: float = float(np.linalg.norm(tangent))
            if L < 1e-9:
                tangent = LEFT
                L = 1.0

            t_hat: np.ndarray = tangent / L

            # Tip point b lands on the dot perimeter where the curve first meets the dot.
            b: np.ndarray = end_point + DOT_RADIUS * t_hat

            # Create a hidden short shaft so only the tip renders.
            arrow_length: float = 0.5
            a: np.ndarray = b + arrow_length * t_hat
            arrow: Line = Line(a, b, color=BLACK, stroke_width=0)
            arrow.set_stroke(opacity=0)
            arrow.add_tip(tip_shape=tip_shape, tip_length=0.3)

            # Label placed slightly offset using a left-normal relative to t_hat.
            n_hat: np.ndarray = np.array([-t_hat[1], t_hat[0], 0.0])
            label: Text = Text(name, font_size=24, color=BLACK)
            label.move_to(b + 0.22 * n_hat - 0.05 * t_hat)

            return VGroup(arrow, label)

        arrow_groups: list[VGroup] = []
        dots: list[Dot] = []
        for curve, (name, cls) in zip(curves, tip_styles):
            arrow_groups.append(arrow_at_end(curve, cls, name))
            p0: np.ndarray = curve.point_from_proportion(0.0)
            p3: np.ndarray = curve.point_from_proportion(1.0)
            dots.extend([
                Dot(p0, radius=DOT_RADIUS, color=BLACK),
                Dot(p3, radius=DOT_RADIUS, color=BLACK),
            ])

        # Cairo uses painter's algorithm; order matters: curves, then dots, then arrows/labels.
        self.add(*curves, *dots, *arrow_groups)
        self.wait(1)


if __name__ == '__main__':
    with tempconfig(LINEN_CONFIG):
        scene = BeziersWithEndpointArrows()
        scene.render()