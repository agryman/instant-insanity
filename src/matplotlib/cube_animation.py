from typing import cast
import numpy as np
from scipy.spatial.transform import Rotation as R
import matplotlib.animation as animation
from matplotlib.artist import Artist
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from instant_insanity.animator import Animator, VideoSpec, MpegSpec
from datetime import datetime

DEFAULT_CUBE_LENGTH: float = 1.0
DEFAULT_CUBE_COLOURS: list[str] = ['dodgerblue', 'red', 'forestgreen', 'white', 'yellow', 'purple']

DEFAULT_AZIMUTH: float = -15.0
DEFAULT_ELEVATION: float = 20.0

def remove_axis(ax: Axes3D) -> None:
    # Remove axis labels, grid, and ticks
    ax.set_axis_off()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

def label_axis(ax: Axes3D) -> None:
    # set axes labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')


class Cube:
    """A coloured 3D cube centered at the origin with a given edge length."""
    
    length: float
    colours: list[str]
    vertices: np.ndarray
    faces: list[list[int]]

    def __init__(self, length: float = None, colours: list[str] = None):

        if length is None:
            length = DEFAULT_CUBE_LENGTH

        if colours is None:
            colours = DEFAULT_CUBE_COLOURS

        self.length = length
        self.colours = colours
        self.vertices = np.array([
            [-1, -1, -1],
            [1, -1, -1],
            [1, 1, -1],
            [-1, 1, -1],  # Bottom face
            [-1, -1, 1],
            [1, -1, 1],
            [1, 1, 1],
            [-1, 1, 1]  # Top face
        ]) * (length / 2)
        
        self.faces = [
            [0, 1, 5, 4],  # Left face
            [2, 3, 7, 6],  # Right face
            [1, 2, 6, 5],  # Front face
            [4, 7, 3, 0],  # Back face
            [4, 5, 6, 7],  # Top face
            [0, 1, 2, 3],  # Bottom face
        ]

    def mk_poly_verts(self, rotation: R = None, translation: np.ndarray = None) -> list[np.ndarray]:
        """
        Make a list of the cube's polygons from the rotated and translated vertices.

        Args:
            rotation: A 3x3 SciPy rotation matrix.
            translation: A translation 3-vector.

        Returns:
            the transformed vertices.
        """

        if rotation is None:
            rotation = R.from_euler('z', 0, degrees=True)

        if translation is None:
            translation = np.array([0, 0, 0])

        vertices: np.ndarray = rotation.apply(self.vertices) + translation
        poly_verts: list[np.ndarray] = list(vertices[self.faces])

        return poly_verts

    def mk_poly_collection(self, rotation: R = None, translation: np.ndarray = None) -> Poly3DCollection:
        """Make a Poly3DCollection of the cube's rotated and translated faces.
        Args:
            rotation: A 3x3 SciPy rotation matrix.
            translation: A translation 3-vector.

        Returns:
            the Poly3DCollection of the cube's faces.
        """

        poly_verts: list[np.ndarray] = self.mk_poly_verts(rotation, translation)

        return Poly3DCollection(poly_verts, facecolors=self.colours, edgecolor='black')


class CubeAnimator(Animator):
    """Animate the motion of a coloured cube."""

    cube: Cube                  # the cube to animate
    cube_poly: Poly3DCollection # the artist that draws the cube
    duration: int               # the duration of the animation in seconds

    def __init__(self, video_spec: VideoSpec = None, mpeg_spec: MpegSpec = None,
                 length: float = None, colours: list[str] = None):

        super().__init__(video_spec=video_spec, mpeg_spec=mpeg_spec)

        self.cube = Cube(length=length, colours=colours)

    def draw_next_frame(self, frame: float) -> list[Artist]:
        """
        Draw the next animation frame.

        Args:
            frame: The time in seconds of the frame.

        Returns:
            a list of artists to be drawn in the frame.
        """

        """Rotate the cube about its z-axis uniformly from 0 to 360 degrees."""
        angle: float = 360 * frame / self.duration
        rotation: R = R.from_euler('z', angle, degrees=True)
        translation: np.ndarray = np.array([0, 0, 0])
        poly_verts: list[np.ndarray] = self.cube.mk_poly_verts(rotation, translation)
        self.cube_poly.set_verts(poly_verts)

        return self.artists

    def animate(self) -> None:
        """Create the animation figure, axes, data, and artists."""

        # Create a figure and 3D axis
        self.fig = self.video_spec.mk_figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        ax: Axes3D = cast(Axes3D, self.ax)
        ax.set_proj_type('ortho')

        # set viewpoint to orient x (back to front) and y (left to right)
        ax.view_init(elev=DEFAULT_ELEVATION, azim=DEFAULT_AZIMUTH)

        # set axes limits
        lim: float = self.cube.length
        ax.set_xlim(xmin=-lim, xmax=lim)
        ax.set_ylim(ymin=-lim, ymax=lim)
        ax.set_zlim(zmin=-lim, zmax=lim)

        remove_axis(ax)

        # initialize the polygons in the starting position
        self.cube_poly = self.cube.mk_poly_collection()
        ax.add_collection3d(self.cube_poly)
        self.artists = [self.cube_poly]

        # compute the list of times
        self.duration = 4
        num_frames: int = self.duration * self.video_spec.fps
        times: np.ndarray = np.linspace(0, self.duration, num_frames, endpoint=False)
        self.frames = list(times)

        self.animation = animation.FuncAnimation(self.fig, self.update_func, frames=self.frames, fargs=(self,),
                                                 blit=False, interval=self.video_spec.msec_per_frame)


def main():

    # show the animation
    animator: CubeAnimator = CubeAnimator()
    animator.show_animation()

    # Get current time and generate a filename
    timestamp: str = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename: str = f"/tmp/cube_animator-{timestamp}.mp4"

    # write the animation
    animator = CubeAnimator()
    animator.write_animation(filename)


if __name__ == "__main__":
    main()
