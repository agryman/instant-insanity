import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter

# Set size to match 720p resolution
dpi = 100
width_in = 1280 / dpi
height_in = 720 / dpi
fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=dpi)

# Example plot
line, = ax.plot([], [], lw=2)

def init():
    ax.set_xlim(0, 2)
    ax.set_ylim(-1, 1)
    return line,

def update(frame):
    x = [0, frame / 100]
    y = [0, frame / 100]
    line.set_data(x, y)
    return line,

# Create animation
anim = FuncAnimation(fig, update, frames=100, init_func=init, blit=True)
plt.show()

# Save as 720p MP4 with 30 fps
writer = FFMpegWriter(fps=30, metadata=dict(artist='Arthur'), bitrate=1800)
anim.save("/tmp/line_plot_animation_720p.mp4", writer=writer)