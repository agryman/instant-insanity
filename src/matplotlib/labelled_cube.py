import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_aspect('equal')

# Define cube vertices
r = [0, 1]
verts = [
    [[r[0], r[0], r[0]], [r[1], r[0], r[0]], [r[1], r[1], r[0]], [r[0], r[1], r[0]]],  # bottom
    [[r[0], r[0], r[1]], [r[1], r[0], r[1]], [r[1], r[1], r[1]], [r[0], r[1], r[1]]],  # top
    [[r[0], r[0], r[0]], [r[0], r[0], r[1]], [r[0], r[1], r[1]], [r[0], r[1], r[0]]],  # left
    [[r[1], r[0], r[0]], [r[1], r[0], r[1]], [r[1], r[1], r[1]], [r[1], r[1], r[0]]],  # right
    [[r[0], r[0], r[0]], [r[1], r[0], r[0]], [r[1], r[0], r[1]], [r[0], r[0], r[1]]],  # front
    [[r[0], r[1], r[0]], [r[1], r[1], r[0]], [r[1], r[1], r[1]], [r[0], r[1], r[1]]]   # back
]
ax.add_collection3d(Poly3DCollection(verts, facecolors='skyblue', linewidths=1, edgecolors='k', alpha=0.3))

# Add labels at the center of each face
face_labels = [
    ((0.5, 0.0, 0.5), "Front"),
    ((0.5, 1.0, 0.5), "Back"),
    ((0.0, 0.5, 0.5), "Left"),
    ((1.0, 0.5, 0.5), "Right"),
    ((0.5, 0.5, 0.0), "Bottom"),
    ((0.5, 0.5, 1.0), "Top"),
]

for (x, y, z), text in face_labels:
    ax.text(x, y, z, text, color='black', ha='center', va='center', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

# Set limits and view
ax.set_xlim([0, 1])
ax.set_ylim([0, 1])
ax.set_zlim([0, 1])
ax.view_init(elev=20, azim=30)  # Adjust for better visibility

plt.show()