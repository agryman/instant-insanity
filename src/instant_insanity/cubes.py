"""This module contains code for drawing cubes."""

from dataclasses import dataclass
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
from IPython.display import HTML
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class FaceNumber(Enum):
    """Numbers that appear on the faces of a die."""
    FRONT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4
    LEFT = 5
    BACK = 6

class FaceColour(Enum):
    """Colours that appear on a puzzle block face."""
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    WHITE = 'white'

# use black as the edge colour
BLACK: str = 'black'

@dataclass
class Face:
    """A face of a block"""
    face_number: FaceNumber
    face_colour: FaceColour

    def draw_face(self) -> None:
        """Draw a face."""
        pass


class Block:
    """ An Instant Insanity puzzle block. """
    pass

class Puzzle:
    """ An Instant Insanity puzzle. """
    pass


fig: Figure
ax: Axes
collection: Poly3DCollection

fig, ax = plt.subplots()

def setup() -> None:
    """Set up the animation axes and data."""
    global fig, ax, ln, xdata, ydata

    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = ax.plot([], [], 'ro')

def init() -> tuple[Line2D]:
    """Initialize the axes for the animation."""
    global ax, ln

    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)

    return ln,

def update(frame) -> tuple[Line2D]:
    """Compute another frame of the animation."""
    global xdata, ydata, ln

    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)

    return ln,

def animate() -> FuncAnimation:
    global fig
    frames = np.linspace(0, 2*np.pi, 128)

    return FuncAnimation(fig, func=update, frames=frames,
                         init_func=init, blit=True, interval=50)

def main():
    setup()
    animate()
    plt.show()

if __name__ == "__main__":
    main()

