import numpy as np
import matplotlib.pyplot as plt
import matplotlib_diagrams.geomplot as gp

def create_projection_diagram():
    """Plot the projection diagram."""
    point_names: str = 'pmn'
    point_decorators: list[str] = ["", "'", "''"]

    alphas: list[float] = [2.0, 3.0, 4.0]

    delta_xs: list[float] = [-2.0, 1.0, 3.0]
    delta_y: float = -5.0

    v: gp.Point = (-4.0, 12.0)
    points: dict[str, gp.Point] = {"v": v}

    point_name: str
    alpha: float
    for point_name, alpha in zip(point_names, alphas):
        point_decorator: str
        delta_x: float
        for point_decorator, delta_x in zip(point_decorators, delta_xs):
            key: str = point_name + point_decorator
            value: gp.Point = (v[0] + alpha * delta_x, v[1] + alpha * delta_y)
            points[key] = value

    lines: list[gp.Segment] = [
        (v, points["n"]),
        (v, points["n'"]),
        (v, points["n''"])
    ]

    fig, ax = gp.start_figure(size=(5, 5), dpi=120)
    gp.setup_axes(ax, list(points.values()), padding=2.0, y_down=False)
    gp.plot_infinite_lines(ax, lines, color='blue')
    gp.plot_points(ax, points, color='blue')

    # draw unit vectors pointing towards v with bases at p, p', p''
    for decorator in point_decorators:
        key = "p" + decorator
        p = points[key]
        x = v[0] - p[0]
        y = v[1] - p[1]
        theta = np.arctan2(y, x)
        r = 5.0
        tip_x = p[0] + r * np.cos(theta)
        tip_y = p[1] + r * np.sin(theta)

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
            "u" + decorator,
            fontsize=12,
            ha='left',
            va='top',
            color='black'
        )

    plane_labels: str = 'CDE'
    plane_zs: list[float] = [2.0, -3.0, -8.0]
    plane_label: str
    plane_z: float
    for plane_label, plane_z in zip(plane_labels, plane_zs):
        gp.plot_hline(ax, y=plane_z, label=plane_label, color='black', linewidth=1.2)

    ax.set_ylabel('z', rotation=0, labelpad=5, ha='right', va='center')

    ax.axis('off')
    ax.set_xticks([])
    ax.set_yticks([])

    _ = ax.set_title('Perspective Projection')

if __name__ == '__main__':
    create_projection_diagram()
    plt.show()