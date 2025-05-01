from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.artist import Artist
from matplotlib.lines import Line2D
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
    msec_per_frame: float

    def __init__(self, width: int = WIDTH, height: int = HEIGHT, dpi: int = DPI, fps: int = FPS):
        """Create the video specification."""

        # width and height in pixels
        self.width = width
        self.height = height

        # dots (pixels) per inch
        self.dpi = dpi

        # width and height in inches
        self.width_in: float = width / dpi
        self.height_in: float = height / dpi

        # frames per second
        self.fps = fps

        # milliseconds per frame
        self.msec_per_frame = 1000 / fps


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


class SineAnimator:
    video_spec: VideoSpec
    mpeg_spec: MpegSpec
    fig: Figure
    ax: Axes
    artists: list[Artist]
    animation: FuncAnimation
    ln: Line2D
    xdata: list[float]
    ydata: list[float]
    frames: list[float]

    def __init__(self, video_spec: VideoSpec = VideoSpec(), mpeg_spec: MpegSpec = MpegSpec()):
        """Create the animation figure, axes, data, and artists."""

        self.video_spec = video_spec
        self.mpeg_spec = mpeg_spec

        figure, axes = plt.subplots(figsize=(video_spec.width_in, video_spec.height_in), dpi=video_spec.dpi)
        self.fig = figure

        self.ax = axes
        self.ax.set_xlim(0, 2*np.pi)
        self.ax.set_ylim(-1, 1)

        self.xdata = []
        self.ydata = []
        self.artists = self.ax.plot(self.xdata, self.ydata, 'ro')
        self.ln = self.artists[0]

        self.frames = list(np.linspace(0, 2*np.pi, 4 * video_spec.fps))

    def update(self, frame: float) -> list[Artist]:
        """Update the animation frame"""

        self.xdata.append(frame)
        self.ydata.append(np.sin(frame))
        self.ln.set_data(self.xdata, self.ydata)

        return self.artists

    @staticmethod
    def update_func(frame: float, animator: 'SineAnimator') -> list[Artist]:
        """Compute another frame of the animation."""

        return animator.update(frame)

    def animate(self) -> None:
        """Create the animation."""

        self.animation = FuncAnimation(self.fig, self.update_func, frames=self.frames, fargs=(self,),
                                       blit=True, interval=self.video_spec.msec_per_frame)

    def show_animation(self) -> None:
        """Show the animation"""
        self.animate()
        plt.show()

    def write_animation(self, filename: str) -> None:
        """Write the animation to a file."""
        self.animate()

        fps: int = self.video_spec.fps
        dpi: int = self.video_spec.dpi

        author: str = self.mpeg_spec.author
        bitrate: int = self.mpeg_spec.bitrate

        writer: FFMpegWriter = FFMpegWriter(fps=fps, metadata=dict(artist=author), bitrate=bitrate)

        self.animation.save(filename=filename, writer=writer, dpi=dpi)


def main():

    # show the animation
    animator = SineAnimator()
    animator.show_animation()

    # Get current time and generate a filename
    timestamp: str = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename: str = f"/tmp/sine_plot-{timestamp}.mp4"

    #write the animation
    animator = SineAnimator()
    animator.write_animation(filename)

if __name__ == "__main__":
    main()
