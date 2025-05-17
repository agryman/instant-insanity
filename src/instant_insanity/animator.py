from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.artist import Artist
from matplotlib.animation import FuncAnimation, FFMpegWriter

# use 720p as defaults for video specification
WIDTH: int = 1280
HEIGHT: int = 720
DPI: int = 100
FPS: int = 30

# defaults for mpeg specification
AUTHOR: str = 'kwargs.xyz'
BITRATE: int = 1800

class VideoSpec:
    """Video specification"""
    dpi: int
    width: int
    height: int
    fps: int
    width_in: float
    height_in: float
    fig_size: tuple[float, float]
    msec_per_frame: float

    def __init__(self, width: int = WIDTH, height: int = HEIGHT, dpi: int = DPI, fps: int = FPS):
        """Create the video specification."""

        # width and height in pixels
        self.width = width
        self.height = height

        # dots (pixels) per inch
        self.dpi = dpi

        # width and height in inches
        self.width_in = width / dpi
        self.height_in = height / dpi
        self.fig_size = (self.width_in, self.height_in)

        # frames per second
        self.fps = fps

        # milliseconds per frame
        self.msec_per_frame = 1000 / fps

    def mk_figure(self) -> Figure:
        """
        Create a figure with the video specification.

        Returns:
            the figure.
        """

        return  plt.figure(figsize=self.fig_size, dpi=self.dpi)


class MpegSpec:
    """MPEG file specification"""
    author: str
    bitrate: int

    def __init__(self, author: str = AUTHOR, bitrate: int = BITRATE):
        """Create the MPEG specification."""

        # author
        self.author = author

        # bit rate
        self.bitrate = bitrate


class Animator(ABC):
    """Abstract base class for animator classes"""

    video_spec: VideoSpec
    mpeg_spec: MpegSpec
    fig: Figure
    ax: Axes
    artists: list[Artist]
    frames: list[float]
    animation: FuncAnimation

    def __init__(self, video_spec: VideoSpec = None, mpeg_spec: MpegSpec = None):

        if video_spec is None:
            video_spec = VideoSpec()

        if mpeg_spec is None:
            mpeg_spec = MpegSpec()

        self.video_spec = video_spec
        self.mpeg_spec = mpeg_spec

    @abstractmethod
    def animate(self) -> None:
        """Create the animation."""
        pass

    @abstractmethod
    def draw_next_frame(self, frame: float) -> list[Artist]:
        """Draw the next animation frame."""
        pass

    @staticmethod
    def update_func(frame: float, animator: 'Animator') -> list[Artist]:
        """Draw the next animation frame."""

        return animator.draw_next_frame(frame)

    def show_animation(self) -> None:
        """Show the animation."""

        self.animate()
        plt.show()

    def write_animation(self, filename: str) -> None:
        """Write the animation to a file."""

        self.animate()

        fps: int = self.video_spec.fps
        author: str = self.mpeg_spec.author
        bitrate: int = self.mpeg_spec.bitrate
        writer: FFMpegWriter = FFMpegWriter(fps=fps, metadata=dict(artist=author), bitrate=bitrate)

        dpi: int = self.video_spec.dpi
        self.animation.save(filename=filename, writer=writer, dpi=dpi)
