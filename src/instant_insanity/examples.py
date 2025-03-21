"""This module contains animation examples."""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.lines import Line2D
from matplotlib.animation import FuncAnimation

fig: Figure
ax: Axes
ln: Line2D
xdata: list[float]
ydata: list[float]

def setup_sine() -> None:
    """Set up the sine wave animation axes and data."""
    global fig, ax, ln, xdata, ydata

    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = ax.plot([], [], 'ro')

def init_sine() -> tuple[Line2D]:
    """Initialize the axes for sine wave animation."""
    global ax, ln

    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)

    return ln,

def update_sine(frame) -> tuple[Line2D]:
    """Compute another frame of the sine wave animation."""
    global xdata, ydata, ln

    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)

    return ln,

def animate_sine() -> FuncAnimation:
    global fig
    frames = np.linspace(0, 2*np.pi, 128)

    return FuncAnimation(fig, func=update_sine, frames=frames,
                  init_func=init_sine, blit=True, interval=50)

def main():
    setup_sine()
    animate_sine()
    plt.show()

if __name__ == "__main__":
    main()
