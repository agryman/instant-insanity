import matplotlib.pyplot as plt
import numpy as np
from instant_insanity.cube import TOP, BOTTOM, RIGHT, LEFT, FRONT, BACK

from mpl_toolkits.mplot3d.art3d import Poly3DCollection

verts = np.array([FRONT, BACK, RIGHT, LEFT, TOP, BOTTOM])

ax = plt.figure().add_subplot(projection='3d')

poly = Poly3DCollection(verts, alpha=0.9)
poly.set_facecolors(['red', 'green', 'blue', 'white', 'green', 'red'])
poly.set_edgecolor('black')

ax.add_collection3d(poly)
ax.set_aspect('equal')

# for desired orientation
ax.view_init(elev=30, azim=30)

ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)

plt.show()