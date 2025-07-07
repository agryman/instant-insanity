from instant_insanity.animator import Animator, VideoSpec, MpegSpec
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
from datetime import datetime

class SineTrailAnimator(Animator):
    xdata: list[float]  # the array of x-values for the sine curve
    ydata: list[float]  # the array of y-values for the sine curve
    ln: Line2D          # the artist that draws the sine curve
    N: int              # the number of points to keep in the trail of the sine curve

    def __init__(self, video_spec: VideoSpec = None, mpeg_spec: MpegSpec = None):

        super().__init__(video_spec=video_spec, mpeg_spec=mpeg_spec)

    def draw_next_frame(self, frame: float) -> list[Artist]:
        """Draw the next animation frame"""

        self.xdata.append(frame)
        self.ydata.append(np.sin(frame))
        self.ln.set_data(self.xdata[-self.N:], self.ydata[-self.N:])

        return self.artists

    def animate(self) -> None:
        """Create the animation figure, axes, data, and artists."""

        figure, axes = plt.subplots(figsize=self.video_spec.fig_size, dpi=self.video_spec.dpi)
        self.fig = figure
        self.ax = axes
        self.N = 20

        def init():
            self.ax.set_xlim(0, 2*np.pi)
            self.ax.set_ylim(-1, 1)

            self.xdata = []
            self.ydata = []
            self.artists = list(self.ax.plot(self.xdata, self.ydata, 'ro'))
            self.ln = self.artists[0]

            return self.artists

        self.frames = list(np.linspace(0, 2 * np.pi, 4 * self.video_spec.fps))

        self.animation = FuncAnimation(self.fig, self.update_func, frames=self.frames, fargs=(self,),
                                       init_func=init, blit=True, interval=self.video_spec.msec_per_frame)


def main():

    # show the animation
    animator = SineTrailAnimator()
    animator.show_animation()

    # Get current time and generate a filename
    timestamp: str = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename: str = f"/tmp/sine_trail_animator-{timestamp}.mp4"

    #write the animation
    animator = SineTrailAnimator()
    animator.write_animation(filename)

if __name__ == "__main__":
    main()
