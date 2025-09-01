import numpy as np

from manim import (ThreeDScene, BLACK, WHITE, DEGREES, VGroup, Square, Text, OUT, UP, RIGHT, DOWN, LEFT, IN,
                   RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE, PI, Rotate, normalize, rotation_matrix, angle_between_vectors)


class LabelledCube(ThreeDScene):
    def construct(self):
        self.renderer.background_color = WHITE
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)

        face_size = 2
        face_opacity = 0.9

        # Helper function to create a face with attached label
        def make_face(color, label_text, normal, up_direction):
            face = Square(side_length=face_size, fill_color=color, fill_opacity=face_opacity)
            face.set_stroke(BLACK, width=2)

            # Orient the face
            face_rotation_matrix = self.rotation_matrix_from_vectors(OUT, normal, up_direction)
            face.apply_matrix(face_rotation_matrix)
            face.shift(normal * face_size / 2)

            # Create and orient label in the same local frame
            label = Text(label_text, color=BLACK).scale(0.5)
            label.apply_matrix(face_rotation_matrix)
            label.move_to(normal * (face_size / 2 - 0.01))  # embed just in front of the face

            # Attach label to face
            face.add(label)
            return face

        # Define all 6 faces with label, normal, and "up" direction
        front = make_face(RED, "x", OUT, UP)
        back = make_face(GREEN, "x'", IN, UP)
        right = make_face(BLUE, "y", RIGHT, UP)
        left = make_face(ORANGE, "y'", LEFT, UP)
        top = make_face(YELLOW, "z", UP, IN)
        bottom = make_face(PURPLE, "z'", DOWN, OUT)
        cube = VGroup(front, back, right, left, top, bottom)
        self.add(cube)

        self.play(Rotate(cube, angle=PI / 2, axis=UP), run_time=2)
        self.wait()

    # Utility: construct a rotation matrix from source to target vector
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
    scene = LabelledCube()
    scene.render(preview=True)
