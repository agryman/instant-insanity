import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

# global variables used in animation
fig: Figure
ax: Axes
ln: list[Line2D]
xdata: list[float]
ydata: list[float]

def setup() -> None:
    """Set up the animation axes and data."""
    global fig, ax, ln, xdata, ydata

    fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=100)
    xdata, ydata = [], []
    ln = ax.plot([], [], 'ro')

def init() -> list[Line2D]:
    """Initialize the axes for the animation."""
    global ax, ln

    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)

    return ln

def update(frame) -> list[Line2D]:
    """Compute another frame of the animation."""
    global xdata, ydata, ln

    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln[0].set_data(xdata, ydata)

    return ln

def animate() -> FuncAnimation:
    global fig

    frames = np.linspace(0, 2*np.pi, 128)

    return FuncAnimation(fig, func=update, frames=frames,
                         init_func=init, blit=True, interval=1000/30)

def main():
    setup()
    ffmeg_writer = FFMpegWriter(fps=30, metadata=dict(artist="kwargs.xyz"), bitrate=1800)
    ani = animate()
    plt.show()
    ani.save(filename="/tmp/sine_plot.mp4", writer=ffmeg_writer, dpi=100)

if __name__ == "__main__":
    main()
