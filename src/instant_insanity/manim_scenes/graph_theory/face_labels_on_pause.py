import numpy as np

from manim import (config, WHITE, ThreeDScene, DEGREES, PI, RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE, BLACK,
                   OUT, IN, UP, DOWN, LEFT, RIGHT, Square, VGroup, Text, Rotate, FadeIn,
                   rotation_matrix, normalize, angle_between_vectors)

config.background_color = WHITE  # must be set before scene instantiation

class FaceLabelsOnPause(ThreeDScene):
    def construct(self):
        #self.renderer.background_color = WHITE
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)

        face_size = 2
        face_opacity = 1.0  # fully opaque

        # Face colors
        face_color = {
            "x": RED,
            "x'": GREEN,
            "y": BLUE,
            "y'": ORANGE,
            "z": YELLOW,
            "z'": PURPLE,
        }

        # Face definitions: label → (normal, up_hint)
        face_to_directions = {
            "x":  (OUT,    UP),
            "x'": (IN,     UP),
            "y":  (RIGHT,  UP),
            "y'": (LEFT,   UP),
            "z":  (UP,     IN),
            "z'": (DOWN,   OUT),
        }

        # Store face: (mobject, normal)
        faces = {}

        for name, (normal, up_dir) in face_to_directions.items():
            face = Square(side_length=face_size, fill_color=face_color[name], fill_opacity=face_opacity)
            face.set_stroke(BLACK, width=2)

            # Align face so its normal points in the desired direction
            rot_matrix = self.rotation_matrix_from_vectors(OUT, normal, up_dir)
            face.apply_matrix(rot_matrix)
            face.shift(normal * (face_size / 2))

            faces[name] = (face, normal)

        # the following code is wrong because VGroup draws the objects in the order that they were added
        # TODO: add a filter to the list comprehension to only add visible faces.
        # Note that the cube is animated using Rotate, which I assume means we can't filter out the faces here
        #
        cube = VGroup(*[f for f, _ in faces.values()])
        self.add(cube)

        # Spin the cube
        self.play(Rotate(cube, angle=PI / 2, axis=UP), run_time=2)
        self.wait()

        # After pause, show labels for the visible faces
        visible_labels = self.get_visible_labels(faces)
        self.play(*[FadeIn(label) for label in visible_labels])
        self.wait()

    def get_camera_forward(self):
        # Compute the camera forward direction from theta and phi
        theta, phi = self.camera.theta, self.camera.phi
        camera_forward = np.array([
            np.cos(theta) * np.sin(phi),
            np.sin(theta) * np.sin(phi),
            np.cos(phi)
        ])

        return camera_forward

    def get_visible_faces(self):
        # Get the list of visible faces
        pass

    def get_visible_labels(self, face_map):
        camera_forward = self.get_camera_forward()

        labels = []
        for name, (face, normal) in face_map.items():
            if np.dot(normal, camera_forward) < 0:  # face toward camera
                center_3d = face.get_center()
                center_2d = self.camera.project_point(center_3d)
                label = Text(name, color=BLACK).scale(0.5)
                label.move_to(center_2d)
                labels.append(label)

        return labels

    @staticmethod
    def rotation_matrix_from_vectors(from_vec, to_vec, up_hint):
        from_vec = normalize(from_vec)
        to_vec = normalize(to_vec)
        axis = np.cross(from_vec, to_vec)
        if np.linalg.norm(axis) < 1e-8:
            return np.eye(3) if np.allclose(from_vec, to_vec) else rotation_matrix(PI, up_hint)
        angle = angle_between_vectors(from_vec, to_vec)
        return rotation_matrix(angle, axis)


if __name__ == "__main__":
    scene = FaceLabelsOnPause()
    scene.render(preview=True)
