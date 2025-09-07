import numpy as np
import matplotlib.pyplot as plt
from manim.typing import Point3D, Vector3D
from manim import Scene, tempconfig, Dot, RIGHT, UP, BLACK, DEFAULT_SMALL_DOT_RADIUS, MathTex, UR, UL, Line, BLUE, DOWN, \
    PURE_BLUE, PURE_RED, Arrow, StealthTip, PURE_GREEN
from matplotlib.patches import ArrowStyle

import matplotlib_diagrams.geomplot as gp
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.scenes.coordinate_grid import GridMixin


class ProjectionDiagram:
    """
    Draw the projection diagram.
    """
    v: gp.Point
    plane_labels: str
    point_names: str
    plane_zs: list[float]
    delta_z: float
    point_decorators: list[str]
    delta_xs: list[float]
    alphas: list[float]
    points: dict[str, gp.Point]
    lines: list[gp.Segment]
    u_tips: dict[str, gp.Point]

    def __init__(self):

        # the viewpoint
        self.v = (-4.0, 12.0)

        # planes going down the diagram
        self.plane_labels = 'CDE'
        self.point_names = 'pmn'
        self.plane_zs = [2.0, -3.0, -8.0]
        self.delta_z = -5.0

        # lines going across the diagram
        self.point_decorators = ["", "'", "''"]
        self.delta_xs = [-2.0, 1.0, 3.0]
        self.alphas = [2.0, 3.0, 4.0]

        # create the nine points where the lines intersect the plane
        self.points = {"v": self.v}
        point_name: str
        alpha: float
        for point_name, alpha in zip(self.point_names, self.alphas):
            point_decorator: str
            delta_x: float
            for point_decorator, delta_x in zip(self.point_decorators, self.delta_xs):
                key: str = point_name + point_decorator
                value: gp.Point = (self.v[0] + alpha * delta_x, self.v[1] + alpha * self.delta_z)
                self.points[key] = value

        # create the three lines through the viewpoint
        self.lines = [
            (self.v, self.points['n' + point_decorator])
            for point_decorator in self.point_decorators
        ]

        # create the tips of the three unit vector that point from plane C (base point p) to the viewpoint v
        self.u_tips: dict[str, gp.Point] = {}
        for point_decorator in self.point_decorators:
            key = 'p' + point_decorator
            p = self.points[key]
            x = self.v[0] - p[0]
            y = self.v[1] - p[1]
            theta = np.arctan2(y, x)
            r = 5.0
            tip_x = p[0] + r * np.cos(theta)
            tip_y = p[1] + r * np.sin(theta)
            self.u_tips[key] = (tip_x, tip_y)

    def draw_matplotlib_axes(self):
        fig, ax = gp.start_figure(size=(5, 5), dpi=120)
        gp.setup_axes(ax, list(self.points.values()), padding=2.0, y_down=False)
        gp.plot_infinite_lines(ax, self.lines, color='blue')
        gp.plot_points(ax, self.points, color='blue')

        # draw unit vectors pointing towards v with bases at p, p', p''
        for point_decorator in self.point_decorators:
            key = 'p' + point_decorator
            p = self.points[key]
            tip_x, tip_y = self.u_tips[key]

            # draw the arrow tip
            ax.annotate(
                '',
                xy=(tip_x, tip_y),
                xytext=p,
                arrowprops=dict(
                    arrowstyle="-|>",
                    color='black',
                    lw=2.0,
                    shrinkA=0,
                    shrinkB=0
                )
            )
            # draw the arrow label
            ax.text(
                tip_x + 0.75,
                tip_y,
                'u' + point_decorator,
                fontsize=12,
                ha='left',
                va='top',
                color='black'
            )

        plane_label: str
        plane_z: float
        for plane_label, plane_z in zip(self.plane_labels, self.plane_zs):
            gp.plot_hline(ax, y=plane_z, label=plane_label, color='black', linewidth=1.2)

        ax.set_ylabel('z', rotation=0, labelpad=5, ha='right', va='center')

        ax.axis('off')
        ax.set_xticks([])
        ax.set_yticks([])

        _ = ax.set_title('Perspective Projection')

    def draw_manim_scene(self):
        pass

def show_projection_diagram():
    """Plot the projection diagram."""
    projection_diagram = ProjectionDiagram()
    projection_diagram.draw_matplotlib_axes()
    plt.show()

class ProjectionDiagramScene(GridMixin, Scene):

    @staticmethod
    def transform_xy(x: float, y: float) -> Point3D:
        return (x + 2) * 0.50 * RIGHT +  (y - 2) * 0.25 * UP

    @staticmethod
    def infinite_line(p1: Point3D, p2: Point3D) -> Line:
        direction: Vector3D = p2 - p1
        x1: Point3D = p1 - 10 * direction
        x2: Point3D = p1 + 10 * direction
        line: Line = Line(x1, x2)
        return line

    def construct(self):
        self.add_grid(False)

        diagram: ProjectionDiagram = ProjectionDiagram()

        # draw and label the lines that represent the planes
        math_tex: MathTex
        plane_label: str
        plane_z: float
        for plane_label, plane_z in zip(diagram.plane_labels, diagram.plane_zs):
            y_intercept: Point3D = self.transform_xy(0.0, plane_z)
            line: Line = self.infinite_line(y_intercept, y_intercept + RIGHT)
            line.set_color(PURE_BLUE)
            line.set_stroke(width=2)
            self.add(line)
            label_point: Point3D = y_intercept + 5.5 * RIGHT
            math_tex = MathTex(plane_label, font_size=24, color=BLACK)
            math_tex.next_to(label_point, DOWN, buff=0.1)
            self.add(math_tex)

        # draw the light rays through the viewpoint
        p0: Point3D = self.transform_xy(*diagram.v)
        point_name: str = diagram.point_names[0]
        point_label: str
        point_decorator: str
        for point_decorator in diagram.point_decorators:
            point_label = point_name + point_decorator
            p1: Point3D = self.transform_xy(*diagram.points[point_label])
            line = self.infinite_line(p0, p1)
            line.set_color(PURE_RED)
            line.set_stroke(width=2)
            self.add(line)

        # draw and label the points
        point_xy: gp.Point
        direction: Vector3D
        for point_label, point_xy in diagram.points.items():
            point: Point3D = self.transform_xy(*point_xy)
            dot: Dot = Dot(point, radius=DEFAULT_SMALL_DOT_RADIUS, color=BLACK)
            self.add(dot)
            direction = UL if len(point_label) == 1 else UR
            math_tex = MathTex(point_label, color=BLACK, font_size=24)
            math_tex.next_to(dot, direction=direction, buff=0.1)
            self.add(math_tex)

        # draw the unit vectors and their labels
        for point_decorator in diagram.point_decorators:
            label: str = 'p' + point_decorator
            start_xz: gp.Point = diagram.points[label]
            end_xz: gp.Point = diagram.u_tips[label]
            start: Point3D = self.transform_xy(*start_xz)
            end: Point3D = self.transform_xy(*end_xz)
            arrow: Arrow = Arrow(
                start=start,
                end=end,
                buff=0.0,
                max_tip_length_to_length_ratio=0.05,
                max_stroke_width_to_length_ratio=2,
                stroke_width=3,
                color=BLACK,
                tip_shape=StealthTip
            )
            self.add(arrow)
            point_label = 'u' + point_decorator
            math_tex = MathTex(point_label, color=BLACK, font_size=24)
            direction = UL if len(point_label) == 1 else UR
            math_tex.next_to(end, direction=direction, buff=0.1)
            self.add(math_tex)


if __name__ == '__main__':
    # show_projection_diagram()
    with tempconfig(LINEN_CONFIG):
        scene = ProjectionDiagramScene()
        scene.render()
