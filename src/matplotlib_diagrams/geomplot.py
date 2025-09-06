# geomplot.py
from collections.abc import Iterable
from pathlib import Path
import io

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes

type Point = tuple[float, float]
type Segment = tuple[Point, Point]

__all__ = [
    'Point',
    'Segment',
    'start_figure',
    'setup_axes',
    'plot_points',
    'plot_segments',
    'plot_infinite_lines',
    'plot_hline',
    'save_svg',
    'svg_xml',
    'display_svg',
]

# ---------------- Figure/Axes creation ----------------

def start_figure(*, size: tuple[float, float] = (5.0, 5.0), dpi: int = 120) -> tuple[Figure, Axes]:
    """Create a new Matplotlib figure and axes.

    Args:
        size: Figure size in inches as (width, height).
        dpi: Resolution in dots per inch.

    Returns:
        A pair (fig, ax).
    """
    fig, ax = plt.subplots(figsize=size, dpi=dpi)
    return fig, ax

# ---------------- Axes utilities ----------------

def setup_axes(
        ax: Axes,
        points: list[Point],
        *,
        padding: float = 0.1,
        y_down: bool = False
) -> None:
    """Configure axes so that points *and their labels* fit inside the viewport.

    This computes the tight bbox of all labels (as annotations with an offset)
    and expands x/y limits so labels are fully visible, plus a data-space padding.

    Args:
        ax: Axes to configure.
        points: Mapping label -> (x, y) coordinate.
        padding: Extra margin (in data units) added around the tight bbox.
        y_down: If True, invert the y-axis so it increases downward.
    """
    if not points:
        ax.set_aspect('equal', adjustable='box')
        if y_down:
            ax.invert_yaxis()
        return

    # Base limits from raw point coordinates
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    # Apply data-space padding and finalize axes
    xmin -= padding
    xmax += padding
    ymin -= padding
    ymax += padding

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, linewidth=0.5, alpha=0.4)
    ax.set_xlabel('x')
    ax.set_ylabel('y', rotation=0, ha='right', va='center')

    if y_down:
        ax.invert_yaxis()

# ---------------- Drawing primitives ----------------

def plot_points(ax: Axes, points: dict[str, Point], *, s: float = 40, **kwargs) -> None:
    """Plot labeled points.

    Args:
        ax: Axes to draw on.
        points: Mapping from label to (x, y).
        s: Marker size passed to scatter().
    """
    xs = [p[0] for p in points.values()]
    ys = [p[1] for p in points.values()]
    ax.scatter(xs, ys, s=s, zorder=3, **kwargs)
    for label, (x, y) in points.items():
        ax.annotate(label, (x, y), xytext=(5, 5), textcoords='offset points')

def plot_segments(ax: Axes, segments: Iterable[Segment], *, linewidth: float = 1.5) -> None:
    """Plot finite line segments.

    Args:
        ax: Axes to draw on.
        segments: Iterable of ((x1, y1), (x2, y2)) pairs.
        linewidth: Line width for segments.
    """
    for (x1, y1), (x2, y2) in segments:
        ax.plot([x1, x2], [y1, y2], linewidth=linewidth, zorder=2)

from matplotlib.axes import Axes
from collections.abc import Iterable

type Point = tuple[float, float]
type Segment = tuple[Point, Point]

def plot_infinite_lines(
    ax: Axes,
    lines: Iterable[Segment],
    *,
    linewidth: float = 1.0,
    **line_kws,
) -> None:
    """Draw lines (through two points) extended to the current Axes limits.

    This uses the rectangle defined by the current x/y limits as the viewport.
    Each input line is intersected with that rectangle and drawn between the
    two intersection points (if they exist).

    Args:
        ax: Axes to draw on.
        lines: Iterable of ((x1, y1), (x2, y2)) point pairs defining each line.
        linewidth: Line width for the lines.
        **line_kws: Extra Matplotlib line style kwargs (e.g., color='k').
    """
    # Use sorted limits so this works even if the axes are inverted.
    xlo, xhi = sorted(ax.get_xlim())
    ylo, yhi = sorted(ax.get_ylim())
    tol = 1e-9  # numeric tolerance for boundary checks / dedup

    def _inside_y(y: float) -> bool:
        return (ylo - tol) <= y <= (yhi + tol)

    def _inside_x(x: float) -> bool:
        return (xlo - tol) <= x <= (xhi + tol)

    for (x1, y1), (x2, y2) in lines:
        dx, dy = x2 - x1, y2 - y1
        if dx == 0.0 and dy == 0.0:
            continue  # degenerate

        candidates: list[tuple[float, Point]] = []

        # Intersections with vertical sides x = xlo, xhi
        if dx != 0.0:
            t = (xlo - x1) / dx
            y = y1 + t * dy
            if _inside_y(y):
                candidates.append((t, (xlo, y)))

            t = (xhi - x1) / dx
            y = y1 + t * dy
            if _inside_y(y):
                candidates.append((t, (xhi, y)))

        # Intersections with horizontal sides y = ylo, yhi
        if dy != 0.0:
            t = (ylo - y1) / dy
            x = x1 + t * dx
            if _inside_x(x):
                candidates.append((t, (x, ylo)))

            t = (yhi - y1) / dy
            x = x1 + t * dx
            if _inside_x(x):
                candidates.append((t, (x, yhi)))

        if not candidates:
            continue  # line misses the viewport entirely

        # Deduplicate near-identical intersection points (corner touches).
        uniq: list[tuple[float, Point]] = []
        for t, (x, y) in sorted(candidates, key=lambda z: z[0]):
            if not uniq:
                uniq.append((t, (x, y)))
            else:
                _, (ux, uy) = uniq[-1]
                if abs(x - ux) > tol or abs(y - uy) > tol:
                    uniq.append((t, (x, y)))

        if len(uniq) >= 2:
            # Use the two extreme intersections along the line parameter.
            (_, p0), (_, p1) = uniq[0], uniq[-1]
            (xA, yA), (xB, yB) = p0, p1
            ax.plot([xA, xB], [yA, yB], linewidth=linewidth, **line_kws)
        # If there's only one unique intersection (tangent/corner touch), skip.

def plot_hline(ax: Axes, y: float, *, label: str | None = None, x_pad: float = 0.02, **line_kws) -> None:
    """Draw a horizontal line at y and optionally place a label just outside the right edge.

    Args:
        ax: Axes to draw on.
        y: Y coordinate of the horizontal line.
        label: Optional text label to place near the right end.
        x_pad: Fractional padding beyond the right x-limit for the label anchor.
        **line_kws: Extra kwargs forwarded to ``ax.axhline`` (e.g., color, linewidth).
    """
    ax.axhline(y=y, **line_kws)
    if label is not None:
        xmin, xmax = ax.get_xlim()
        x = xmax + (xmax - xmin) * x_pad
        ax.text(x, y, label, va='center', ha='left')

# ---------------- SVG export & display ----------------

def save_svg(
    figure: Figure,
    path: str | Path,
    *,
    dpi: int = 144,
    transparent: bool = True,
    metadata: dict[str, str] | None = None,
    pad_inches: float = 0.01,
) -> Path:
    """Save a figure to SVG.

    Args:
        figure: Figure to save.
        path: Output path ('.svg' will be ensured).
        dpi: Resolution used for any rasterized artists.
        transparent: Transparent background for the SVG.
        metadata: Optional metadata (e.g., {'Title': 'My Diagram'}).
        pad_inches: Padding around the tight bounding box, in inches.

    Returns:
        The resolved output path.
    """
    out_path = Path(path).with_suffix('.svg')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(
        out_path,
        format='svg',
        bbox_inches='tight',
        pad_inches=pad_inches,
        dpi=dpi,
        transparent=transparent,
        metadata=metadata or {},
    )
    return out_path

def svg_xml(
    figure: Figure,
    *,
    dpi: int = 144,
    transparent: bool = True,
    metadata: dict[str, str] | None = None,
    pad_inches: float = 0.01,
) -> str:
    """Render a figure to an SVG XML string.

    Args:
        figure: Figure to render.
        dpi: Resolution used for any rasterized artists.
        transparent: Transparent background for the SVG.
        metadata: Optional metadata (e.g., {'Title': 'My Diagram'}).
        pad_inches: Padding around the tight bounding box, in inches.

    Returns:
        The SVG document as a UTF-8 string.
    """
    buf = io.StringIO()
    figure.savefig(
        buf,
        format='svg',
        bbox_inches='tight',
        pad_inches=pad_inches,
        dpi=dpi,
        transparent=transparent,
        metadata=metadata or {},
    )
    return buf.getvalue()

def display_svg(
    figure: Figure,
    *,
    dpi: int = 144,
    transparent: bool = True,
    metadata: dict[str, str] | None = None,
    pad_inches: float = 0.01,
):
    """Display a figure inline in a Jupyter notebook as SVG.

    Args:
        figure: Figure to display.
        dpi: Resolution used for any rasterized artists.
        transparent: Transparent background for the SVG.
        metadata: Optional metadata (e.g., {'Title': 'My Diagram'}).
        pad_inches: Padding around the tight bounding box, in inches.
    """
    from IPython.display import display, SVG  # local import to avoid hard dependency
    display(SVG(svg_xml(figure, dpi=dpi, transparent=transparent, metadata=metadata, pad_inches=pad_inches)))
