import numpy as np
from manim import Scene, VGroup, Dot, Line, Text, tempconfig, BLACK
from manim.typing import Vector3D, Point3D

from instant_insanity.core.config import LINEN_CONFIG
from manim_examples.geometry_diagrams.render_png import render_png


class GeoDiagram(Scene):
    def construct(self) -> None:
        """Draw a simple geometric diagram: three points and connecting lines."""
        # Points (in Manim coords; origin at center, +x right, +y up)
        A_point: Point3D = np.array([-3, -1, 0], dtype=np.float64)
        B_point: Point3D = np.array([2, 0.5, 0], dtype=np.float64)
        C_point: Point3D = np.array([0, 2, 0], dtype=np.float64)

        A = Dot(A_point, color=BLACK)
        B = Dot(B_point, color=BLACK)
        C = Dot(C_point, color=BLACK)

        A_direction: Vector3D = np.array([0.6, -0.6, 0], dtype=np.float64)
        B_direction: Vector3D = np.array([0.6, 0.6, 0], dtype=np.float64)
        C_direction: Vector3D = np.array([-0.6, 0.6, 0], dtype=np.float64)

        # Labels
        label_A = Text('A', font_size=28, color=BLACK).next_to(A, direction=A_direction)
        label_B = Text('B', font_size=28, color=BLACK).next_to(B, direction=B_direction)
        label_C = Text('C', font_size=28, color=BLACK).next_to(C, direction=C_direction)

        # Finite segments
        ab = Line(A.get_center(), B.get_center(), color=BLACK)
        ac = Line(A.get_center(), C.get_center(), color=BLACK)
        bc = Line(B.get_center(), C.get_center(), color=BLACK)

        # Group and add
        self.add(VGroup(ab, ac, bc, A, B, C, label_A, label_B, label_C))


if __name__ == "__main__":
    with tempconfig(LINEN_CONFIG):
        scene = GeoDiagram()
        scene.render()
    render_png(GeoDiagram, out_name='geo_diagram')
