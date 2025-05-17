import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create a figure with 1080p resolution (16:9)
fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
ax = plt.axes(xlim=(0, 2*np.pi), ylim=(-1.1, 1.1))
line, = ax.plot([], [], lw=3)

# Initialization function
def init():
    line.set_data([], [])
    return line,

# Update function
def update(frame):
    x = np.linspace(0, 2*np.pi, 1000)
    y = np.sin(x + 0.1 * frame)
    line.set_data(x, y)
    return line,

# Create animation
frames = 300  # 10 seconds at 30 fps
ani = FuncAnimation(fig, update, init_func=init, frames=frames, blit=True)

# Save to MP4 with ffmpeg at 1080p, 30 fps
ani.save("/tmp/sine_wave_1080p.mp4", fps=30, bitrate=8000,
         extra_args=['-vcodec', 'libx264'])

plt.close()