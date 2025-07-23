from manim import *

class CubeNet(Scene):
    def construct(self):
        square_size = 1

        # Create six squares
        faces = [Square(side_length=square_size) for _ in range(6)]

        # Arrange in T-shape net for a cube
        positions = [
            UP,             # Top face
            ORIGIN,         # Center face
            LEFT,           # Left face
            RIGHT,          # Right face
            DOWN,           # Bottom face
            DOWN * 2        # Very bottom face
        ]

        for face, pos in zip(faces, positions):
            face.move_to(pos)

        net = VGroup(*faces)
        self.play(Create(net))
        self.wait()

if __name__ == "__main__":
    scene = CubeNet()
    scene.render(preview=True)
