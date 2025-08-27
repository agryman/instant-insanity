from instant_insanity.animator import Animator, VideoSpec, MpegSpec
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
from datetime import datetime

class SineAnimator(Animator):
    xdata: list[float]
    ydata: list[float]
    ln: Line2D

    def __init__(self, video_spec: VideoSpec = VideoSpec(), mpeg_spec: MpegSpec = MpegSpec()):

        super().__init__(video_spec=video_spec, mpeg_spec=mpeg_spec)

    def draw_next_frame(self, frame: float) -> list[Artist]:
        """Draw the next animation frame"""

        self.xdata.append(frame)
        self.ydata.append(np.sin(frame))
        self.ln.set_data(self.xdata, self.ydata)

        return [self.ln]  # Return list[Line2D] as list[Artist] - Line2D inherits from Artist

    def animate(self) -> None:
        """Create the animation figure, axes, data, and artists."""

        figure, axes = plt.subplots(figsize=self.video_spec.fig_size, dpi=self.video_spec.dpi)
        self.fig = figure
        self.ax = axes
        self.ax.set_xlim(0, 2*np.pi)
        self.ax.set_ylim(-1, 1)
        self.frames = list(np.linspace(0, 2 * np.pi, 4 * self.video_spec.fps))

        self.xdata = []
        self.ydata = []
        self.artists = list(self.ax.plot(self.xdata, self.ydata, 'ro'))
        self.ln = self.artists[0]
        self.animation = FuncAnimation(self.fig, self.update_func, frames=self.frames, fargs=(self,),
                                       blit=True, interval=self.video_spec.msec_per_frame)


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
