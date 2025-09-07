import matplotlib_diagrams.geomplot as gp

def abc_example():
    A: gp.Point = (0.0, 0.0)
    B: gp.Point = (4.0, 1.0)
    C: gp.Point = (2.0, 3.0)

    points: dict[str, gp.Point] = {'A': A, 'B': B, 'C': C}
    segments: list[gp.Segment] = [(A, B), (A, C), (B, C)]
    lines: list[gp.Segment] = [(A, B), (A, C)]

    fig, ax = gp.start_figure(size=(5, 5), dpi=120)
    gp.setup_axes(ax, list(points.values()), padding=1.0, y_down=False)
    gp.plot_infinite_lines(ax, lines)
    gp.plot_segments(ax, segments)
    gp.plot_points(ax, points)
    gp.plot_hline(ax, y=1.5, label='C', color='black', linewidth=1.2)

    ax.set_title('Geometric diagram (OO Matplotlib)')
    gp.display_svg(fig)  # or: gp.save_svg(fig, 'fig/diagram')
