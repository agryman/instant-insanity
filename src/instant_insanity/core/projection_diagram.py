import numpy as np
import sympy as sp

import matplotlib.pyplot as plt
from manim.typing import Point3D, Vector3D
from manim import (Scene, tempconfig, Dot, RIGHT, UP, BLACK, DEFAULT_SMALL_DOT_RADIUS, MathTex, UR, UL, Line,
                   DOWN, PURE_BLUE, PURE_RED, Arrow, StealthTip, LEFT)

import matplotlib_diagrams.geomplot as gp
from instant_insanity.core.config import LINEN_CONFIG
from instant_insanity.scenes.coordinate_grid import GridMixin


class ProjectionDiagram:
    """
    This class draws a perspective projection diagram.

    The diagram consists of the following geometric objects:
    * the viewpoint v - 2 free parameters that define the point (v_1, v_2)
    * the horizonal lines C, D, and E - 3 free parameters that define the y-intercepts: c, d, e
    * the points p, p', and p'' on C - 3 free parameters that define the x-components: p_1, p'_1, p''_1
    * the light rays L, L', and L'' from v through p, p', and p''
    * the points m, m', and m'' on D where the light rays cross it
    * the points n, n', and n'' on E where the light rays cross it
    * the unit vectors u, u', and u'' pointing from p, p', and p'' towards v

    The diagram contains 10 labelled points.
    The labels are v, p, p', p'', m, m', m'', n, n', and n''.
    The primed labels are formed by concatenating the point's base name and a decorator.

    Compute the points as follows:
    p = (p_1, c), p' = (p'_1, c), p'' = (p''_1, c)

    m_1 = v_1 + (d - v_2) * (p_1 - v_1) / (p_2 - v_2)
    m'_1 = v_1 + (d - v_2) * (p'_1 - v_1) / (p'_2 - v_2)
    m''_1 = v_1 + (d - v_2) * (p''_1 - v_1) / (p''_2 - v_2)

    m = (m_1, d), m' = (m'_1, d), m'' = (m''_1, d)

    n_1 = v_1 + (e - v_2) * (p_1 - v_1) / (p_2 - v_2)
    n'_1 = v_1 + (e - v_2) * (p'_1 - v_1) / (p'_2 - v_2)
    n''_1 = v_1 + (e - v_2) * (p''_1 - v_1) / (p''_2 - v_2)

    n = (n_1, e), n' = (n'_1, e), n'' = (n''_1, e)

    The diagram contains 3 horizontal lines that represent planes.
    The planes are labelled C, D, and E, respectively.

    Draw C from p to p'.
    Draw D from m to m'.
    Draw E from n to n'.

    The diagram contains 3 light rays that pass through v and the points p, p', and p'' respectively.

    The diagram contains 3 unit vectors that point from the p's to v.

    The base of the unit vectors u, u', and u'' are at p, p', and p''.

    u = (v - p) / norm(v - p),
    u' = (v - p') / norm(v - p'),
    u'' = (v - p'') / norm(v - p'')

    The tips of the unit vectors are tip, tip', and tip''.
    tip = p + u,
    tip' = p' + u',
    tip'' = p'' + u''


    Attributes:
        viewpoint: the viewpoint v
        plane_labels: the letters C, D, and E
        plane_zs: the y-intercepts of the planes
        point_names: the base names of the points p, m, and z
        decorators: the decorators are strings consisting of 0, 1, or 2 primes
        points: a dict whose keys are point labels and whose values are the point coordinates
        u: a list of the unit vectors u, u', u''
    """
    viewpoint: sp.Point2D

    plane_labels: str
    point_names: str
    plane_zs: list[float]

    decorators: list[str]
    p_xs: list[float]

    h_lines: list[sp.Line2D]
    light_rays: list[sp.Line2D]
    points: dict[str, sp.Point2D]
    u: list[sp.Segment2D]

    def __init__(self):

        # the viewpoint
        self.viewpoint = sp.Point2D(-1.0, 2.5)

        # planes, drawn as horizontal lines, going down the diagram
        self.point_names = 'pmn'
        self.plane_labels = 'CDE'
        self.plane_zs = [0.00, -1.25, -2.50]

        # points and light rays going across the diagram
        self.p_xs = [-3.0, 0.0, 2.0]
        self.decorators = ["'" * n for n in range(len(self.p_xs))]

        # p, p', p''
        c: float = self.plane_zs[0]
        p_x: float
        ps: list[sp.Point2D] = [sp.Point2D(p_x, c) for p_x in self.p_xs]

        # create the light rays L, L', L'' from the ps to v
        p: sp.Point2D
        self.light_rays = [sp.Line2D(p, self.viewpoint) for p in ps]

        # define the horizontal lines C, D, E
        plane_z: float
        self.h_lines = [sp.Line2D(
            sp.Point2D(0, plane_z),
            sp.Point2D(1, plane_z)
        )
            for plane_z in self.plane_zs]

        # define the horizontal line V
        viewpoint_y: float = self.viewpoint[1]
        self.viewpoint_h_line = sp.Line2D(
            sp.Point2D(0, viewpoint_y),
            sp.Point2D(1, viewpoint_y)
        )

        # initialize the points dict with the viewpoint v
        self.points = {'v': self.viewpoint}

        # add the nine points where the three horizontal lines C, D, E intersect the three light rays L, L', L''
        h_line: sp.Line2D
        point_name: str
        light_ray: sp.Line2D
        decorator: str
        for h_line, point_name in zip(self.h_lines, self.point_names):
            for light_ray, decorator in zip(self.light_rays, self.decorators):
                point_label: str = point_name + decorator
                intersection_point: sp.Point2D = light_ray.intersection(h_line)[0]
                assert isinstance(intersection_point, sp.Point2D)
                self.points[point_label] = intersection_point

        # create the three unit vectors that point from plane C (base point p) to the viewpoint v
        self.u = []
        for p in ps:
            x: float = float(self.viewpoint[0] - p[0])
            y: float  = float(self.viewpoint[1] - p[1])
            theta: float = np.arctan2(y, x)
            tip_x = p[0] + np.cos(theta)
            tip_y = p[1] + np.sin(theta)
            tip: sp.Point2D = sp.Point2D(tip_x, tip_y)
            self.u.append(sp.Segment2D(p, tip))

def sp_point2d_to_gp_point(point: sp.Point2D) -> gp.Point:
    return float(point.x), float(point.y)

def sp_line2d_to_gp_segment(line: sp.Line2D) -> gp.Segment:
    p1: sp.Point2D = line.p1
    p2: sp.Point2D = line.p2
    return sp_point2d_to_gp_point(p1), sp_point2d_to_gp_point(p2)

def show_projection_diagram():
    """Show the projection diagram using matplotlib."""
    diagram: ProjectionDiagram = ProjectionDiagram()
    fig, ax = gp.start_figure(size=(5, 5), dpi=120)

    points: dict[str, gp.Point] = {key: sp_point2d_to_gp_point(point)
                                   for key, point in diagram.points.items()}
    gp.setup_axes(ax, list(points.values()), padding=2.0, y_down=False)

    # h_lines: list[gp.Segment] = [sp_line2d_to_gp_segment(line) for line in diagram.h_lines]
    # gp.plot_infinite_lines(ax, h_lines, color='blue')

    light_rays: list[gp.Segment] = [sp_line2d_to_gp_segment(light_ray)
                                    for light_ray in diagram.light_rays]
    gp.plot_infinite_lines(ax, light_rays, color='red')

    gp.plot_points(ax, points, color='black')

    # draw unit vectors pointing towards v with bases at p, p', p''
    for point_decorator, u in zip(diagram.decorators, diagram.u):
        p: gp.Point = sp_point2d_to_gp_point(u.p1)
        tip: gp.Point = sp_point2d_to_gp_point(u.p2)
        tip_x, tip_y = tip

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
    for plane_label, plane_z in zip(diagram.plane_labels, diagram.plane_zs):
        gp.plot_hline(ax, y=plane_z, label=plane_label, color='blue', linewidth=1.2)

    gp.plot_hline(ax, y=diagram.viewpoint[1], label='V', color='blue', linewidth=1.2)

    ax.set_ylabel('z', rotation=0, labelpad=5, ha='right', va='center')

    ax.axis('off')
    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title('Perspective Projection')
    plt.show()


class ProjectionDiagramScene(GridMixin, Scene):

    @staticmethod
    def x_at_y(line: sp.Line2D, y_value: float) -> float:
        # Get two points on the line
        p1, p2 = line.points
        # Calculate slope
        slope = (p2.y - p1.y) / (p2.x - p1.x)
        # Use point-slope form: y - y1 = m(x - x1)
        # Solve for x: x = (y - y1)/m + x1
        return float((y_value - p1.y) / slope + p1.x)

    @staticmethod
    def sp_to_np(p: sp.Point2D) -> Point3D:
        """Converts a SymPy 2D Point to a NumPy 3D Point."""
        return float(p.x) * RIGHT + float(p.y) * UP

    @staticmethod
    def infinite_line(sp_line: sp.Line2D) -> Line:
        p1: Point3D = ProjectionDiagramScene.sp_to_np(sp_line.p1)
        p2: Point3D = ProjectionDiagramScene.sp_to_np(sp_line.p2)
        direction: Vector3D = p2 - p1
        q1: Point3D = p1 - 10 * direction
        q2: Point3D = p1 + 10 * direction
        line: Line = Line(q1, q2)
        return line

    def construct(self):
        self.add_grid(False)

        diagram: ProjectionDiagram = ProjectionDiagram()

        # draw and label the horizontal lines that represent the planes
        math_tex: MathTex
        line: Line

        plane_labels: str = diagram.plane_labels + 'V'
        h_lines: list[sp.Line2D] = diagram.h_lines + [diagram.viewpoint_h_line]
        plane_zs: list[float] = diagram.plane_zs + [float(diagram.viewpoint[1])]
        plane_label: str
        h_line: sp.Line2D
        y_intercept: float
        for plane_label, h_line, y_intercept in zip(plane_labels, h_lines, plane_zs):
            line = self.infinite_line(h_line)
            line.set_color(PURE_BLUE)
            line.set_stroke(width=2)
            self.add(line)
            label_point: Point3D = y_intercept * UP + 6.5 * RIGHT
            math_tex = MathTex(plane_label, font_size=24, color=BLACK)
            math_tex.next_to(label_point, DOWN, buff=0.1)
            self.add(math_tex)

        # draw the three light rays through the viewpoint and label them L, L', L''
        light_ray: sp.Line2D
        decorator: str
        direction: Vector3D
        for light_ray, decorator in zip(diagram.light_rays, diagram.decorators):
            line = self.infinite_line(light_ray)
            line.set_color(PURE_RED)
            line.set_stroke(width=2)
            self.add(line)
            ray_label: str = 'L' + decorator
            y: float = -3.25
            x: float = ProjectionDiagramScene.x_at_y(light_ray, y)
            ray_point: Point3D = x * RIGHT + y * UP
            direction = RIGHT if len(decorator) == 0 else LEFT
            math_tex = MathTex(ray_label, font_size=24, color=BLACK)
            math_tex.next_to(ray_point, direction=direction, buff=0.2)
            self.add(math_tex)

        # draw and label the nine points
        point_label: str
        point_xy: sp.Point2D
        for point_label, point_xy in diagram.points.items():
            point: Point3D = ProjectionDiagramScene.sp_to_np(point_xy)
            dot: Dot = Dot(point, radius=DEFAULT_SMALL_DOT_RADIUS, color=BLACK)
            self.add(dot)
            direction = UL if len(point_label) == 1 else UR
            math_tex = MathTex(point_label, color=BLACK, font_size=24)
            math_tex.next_to(dot, direction=direction, buff=0.1)
            self.add(math_tex)

        # draw the three unit vectors and their labels
        u: sp.Segment2D
        for u, decorator in zip(diagram.u, diagram.decorators):
            start: Point3D = ProjectionDiagramScene.sp_to_np(u.p1)
            end: Point3D = ProjectionDiagramScene.sp_to_np(u.p2)
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
            u_label: str = 'u' + decorator
            math_tex = MathTex(u_label, color=BLACK, font_size=24)
            direction = UL if len(u_label) == 1 else UR
            math_tex.next_to(end, direction=direction, buff=0.1)
            self.add(math_tex)

render_manim: bool = True

if __name__ == '__main__':
    if render_manim:
        with tempconfig(LINEN_CONFIG):
            scene = ProjectionDiagramScene()
            scene.render()
    else:
        show_projection_diagram()
