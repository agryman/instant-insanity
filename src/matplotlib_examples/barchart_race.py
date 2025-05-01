"""https://matplotlib.org/stable/users/explain/animations/animations.html"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()
rng = np.random.default_rng(19680801)

# Tableau Colors from 'T10' categorical palette.
colors = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
    'tab:purple',
    'tab:brown',
    'tab:pink',
    'tab:gray',
    'tab:olive',
    'tab:cyan',
]
n = len(colors)
data = np.array([20] * n)
x = np.array(range(1, n + 1))

artists = []
for i in range(20):
    data += rng.integers(low=0, high=10, size=data.shape)
    container = ax.barh(x, data, color=colors)
    artists.append(container)


ani = animation.ArtistAnimation(fig=fig, artists=artists, interval=400)
ani.save(filename="/tmp/barchart_race.mp4", writer="ffmpeg")
plt.show()
