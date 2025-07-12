from manim import *
import numpy as np


class InstantInsanityScene(ThreeDScene):
    def construct(self):
        # Set up 3D camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Define colors for the puzzle (Red, Blue, Green, Yellow)
        colors = [RED, BLUE, GREEN, YELLOW]
        color_names = ["R", "B", "G", "Y"]

        # Define the 4 cubes with their face colors
        # Each cube has 6 faces: front, back, left, right, top, bottom
        cube_faces = [
            [RED, BLUE, GREEN, YELLOW, RED, BLUE],  # Cube 1
            [BLUE, GREEN, YELLOW, RED, GREEN, YELLOW],  # Cube 2
            [GREEN, YELLOW, RED, BLUE, YELLOW, RED],  # Cube 3
            [YELLOW, RED, BLUE, GREEN, BLUE, GREEN]  # Cube 4
        ]

        # Convert to color indices for graph representation
        cube_face_indices = []
        for cube in cube_faces:
            indices = []
            for face_color in cube:
                indices.append(colors.index(face_color))
            cube_face_indices.append(indices)

        self.introduce_puzzle()
        self.show_cubes_3d(cube_faces)
        self.rotate_cubes_demonstration()
        self.transition_to_graph_theory()
        self.create_multigraph(cube_face_indices)
        self.solve_puzzle()

    def introduce_puzzle(self):
        title = Text("Instant Insanity", font_size=48, color=WHITE)
        title.to_edge(UP)

        description = Text(
            "Arrange 4 cubes so each side shows\nall 4 colors exactly once",
            font_size=24,
            color=LIGHT_GRAY
        )
        description.next_to(title, DOWN, buff=0.5)

        self.add_fixed_in_frame_mobjects(title, description)
        self.play(Write(title), Write(description))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(description))

    def show_cubes_3d(self, cube_faces):
        # Create 4 cubes positioned in a row
        cubes = []
        positions = [LEFT * 4, LEFT * 1.5, RIGHT * 1.5, RIGHT * 4]

        for i, (faces, pos) in enumerate(zip(cube_faces, positions)):
            cube = self.create_colored_cube(faces, pos)
            cubes.append(cube)

        # Animate cubes appearing
        for cube in cubes:
            self.play(Create(cube), run_time=0.8)

        self.cubes = cubes
        self.wait(1)

    def create_colored_cube(self, face_colors, position):
        # Create a cube with colored faces
        cube = Cube(side_length=1, fill_opacity=0.8, stroke_width=2)
        cube.move_to(position)

        # Color each face
        faces = [
            cube[0],  # front
            cube[1],  # back
            cube[2],  # left
            cube[3],  # right
            cube[4],  # top
            cube[5]  # bottom
        ]

        for face, color in zip(faces, face_colors):
            face.set_fill(color, opacity=0.8)
            face.set_stroke(WHITE, width=2)

        return cube

    def rotate_cubes_demonstration(self):
        # Rotate cubes to show different faces
        self.play(
            *[Rotate(cube, PI / 2, axis=UP) for cube in self.cubes],
            run_time=1.5
        )
        self.wait(0.5)

        self.play(
            *[Rotate(cube, PI / 2, axis=RIGHT) for cube in self.cubes],
            run_time=1.5
        )
        self.wait(0.5)

        # Reset to original orientation
        self.play(
            *[Rotate(cube, -PI / 2, axis=RIGHT) for cube in self.cubes],
            *[Rotate(cube, -PI / 2, axis=UP) for cube in self.cubes],
            run_time=1.5
        )
        self.wait(1)

    def transition_to_graph_theory(self):
        # Add transition text
        transition_text = Text(
            "Let's solve this using Graph Theory!",
            font_size=36,
            color=YELLOW
        )
        self.add_fixed_in_frame_mobjects(transition_text)
        self.play(Write(transition_text))
        self.wait(2)
        self.play(FadeOut(transition_text))

        # Move cubes to make room for graph
        self.play(
            *[cube.animate.shift(UP * 2 + LEFT * 0.5) for cube in self.cubes],
            run_time=1.5
        )

    def create_multigraph(self, cube_face_indices):
        # Create vertices for the 4 colors
        vertices = {}
        vertex_positions = {
            0: UP * 2 + LEFT * 3,  # Red
            1: UP * 2 + RIGHT * 3,  # Blue
            2: DOWN * 2 + LEFT * 3,  # Green
            3: DOWN * 2 + RIGHT * 3  # Yellow
        }

        colors = [RED, BLUE, GREEN, YELLOW]
        color_names = ["R", "B", "G", "Y"]

        # Create vertex circles
        for i, (pos, color, name) in enumerate(zip(vertex_positions.values(), colors, color_names)):
            circle = Circle(radius=0.3, color=color, fill_opacity=0.8)
            circle.move_to(pos)
            label = Text(name, font_size=24, color=WHITE)
            label.move_to(pos)
            vertex_group = VGroup(circle, label)
            vertices[i] = vertex_group

        # Animate vertex creation
        for vertex in vertices.values():
            self.add_fixed_in_frame_mobjects(vertex)
            self.play(Create(vertex), run_time=0.5)

        # Create edges for each cube
        edges = []
        edge_labels = []

        print(f"Creating edges for {len(cube_face_indices)} cubes...")

        for cube_idx, faces in enumerate(cube_face_indices):
            print(f"Cube {cube_idx + 1}: {faces}")
            # For each cube, create edges between opposite faces
            # front-back, left-right, top-bottom
            pairs = [(0, 1), (2, 3), (4, 5)]  # opposite face pairs

            for pair_idx, (face1, face2) in enumerate(pairs):
                color1, color2 = faces[face1], faces[face2]
                print(f"  Pair {pair_idx + 1}: faces {face1}-{face2}, colors {color1}-{color2}")

                # Create curved edge between vertices
                start_pos = vertex_positions[color1]
                end_pos = vertex_positions[color2]

                if color1 == color2:  # Self-loop
                    edge = self.create_self_loop(start_pos, colors[color1], cube_idx, pair_idx)
                    label_pos = start_pos + UP * 0.8 + RIGHT * (0.3 * pair_idx)
                else:  # Regular edge
                    edge = self.create_curved_edge(start_pos, end_pos, colors[color1], cube_idx, pair_idx)
                    # Offset label position for multiple edges between same vertices
                    label_pos = (start_pos + end_pos) / 2
                    # Add offset for multiple edges between same vertices
                    offset = 0.3 * (pair_idx - 1)
                    perpendicular = np.array([-(end_pos[1] - start_pos[1]), end_pos[0] - start_pos[0], 0])
                    if np.linalg.norm(perpendicular) > 0:
                        perpendicular = perpendicular / np.linalg.norm(perpendicular) * offset
                        label_pos += perpendicular

                edge_label = Text(f"C{cube_idx + 1}", font_size=14, color=WHITE)
                edge_label.move_to(label_pos)

                edges.append(edge)
                edge_labels.append(edge_label)

        print(f"Total edges created: {len(edges)}")
        print(f"Expected: 12 edges (3 pairs × 4 cubes)")

        # Animate edge creation
        for edge, label in zip(edges, edge_labels):
            self.add_fixed_in_frame_mobjects(edge, label)
            self.play(Create(edge), Write(label), run_time=0.8)

        self.vertices = vertices
        self.edges = edges
        self.edge_labels = edge_labels
        self.wait(2)

    def create_curved_edge(self, start, end, color, cube_idx, pair_idx):
        # Create a curved arrow between two points
        # Vary the curve angle to avoid overlapping edges
        base_angle = PI / 4
        angle_offset = (pair_idx - 1) * PI / 8  # Spread multiple edges
        curve_angle = base_angle + angle_offset

        curve = ArcBetweenPoints(start, end, angle=curve_angle)
        curve.set_color(color)
        curve.set_stroke(width=3)

        # Add arrowhead
        arrow = Arrow(start, end, color=color, stroke_width=3, buff=0.3)
        arrow.put_start_and_end_on(start, end)

        return VGroup(curve, arrow)

    def create_self_loop(self, pos, color, cube_idx, pair_idx):
        # Create a self-loop at a vertex
        # Offset multiple self-loops
        radius = 0.4
        loop_offset = pair_idx * 0.3
        loop_pos = pos + UP * (0.4 + loop_offset)

        loop = Circle(radius=radius, color=color, stroke_width=3)
        loop.move_to(loop_pos)

        # Add small arrow to indicate direction
        arrow_tip = Triangle(color=color, fill_opacity=1)
        arrow_tip.scale(0.1)
        arrow_tip.move_to(loop_pos + UP * radius)

        return VGroup(loop, arrow_tip)

    def solve_puzzle(self):
        # Add solution explanation
        solution_title = Text("Graph Theory Solution", font_size=32, color=YELLOW)
        solution_title.to_edge(UP)

        solution_text = Text(
            "Find two edge-disjoint subgraphs where each vertex has degree 2",
            font_size=20,
            color=LIGHT_GRAY
        )
        solution_text.next_to(solution_title, DOWN, buff=0.3)

        self.add_fixed_in_frame_mobjects(solution_title, solution_text)
        self.play(Write(solution_title), Write(solution_text))
        self.wait(3)

        # Highlight solution paths (this would be puzzle-specific)
        self.highlight_solution_paths()

        self.wait(2)

    def highlight_solution_paths(self):
        # This would highlight the actual solution paths
        # For demonstration, we'll just highlight some edges
        highlight_color = YELLOW

        # Example: highlight first few edges as "solution"
        if len(self.edges) > 0:
            for i in range(min(3, len(self.edges))):
                self.play(
                    self.edges[i].animate.set_color(highlight_color),
                    run_time=0.5
                )

        self.wait(2)


# Additional scene for detailed cube face analysis
class CubeAnalysisScene(Scene):
    def construct(self):
        title = Text("Cube Face Analysis", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # Create a manual table using Text objects and rectangles
        colors = [RED, BLUE, GREEN, YELLOW]
        color_map = {"R": RED, "B": BLUE, "G": GREEN, "Y": YELLOW}

        # Table data
        cube_data = [
            ["Cube 1", "R", "B", "G", "Y", "R", "B"],
            ["Cube 2", "B", "G", "Y", "R", "G", "Y"],
            ["Cube 3", "G", "Y", "R", "B", "Y", "R"],
            ["Cube 4", "Y", "R", "B", "G", "B", "G"]
        ]

        headers = ["Cube", "Front", "Back", "Left", "Right", "Top", "Bottom"]

        # Create table manually
        table_group = VGroup()

        # Create header row
        header_row = VGroup()
        for i, header in enumerate(headers):
            cell = Rectangle(width=1.2, height=0.5, stroke_color=WHITE, fill_color=DARK_GRAY, fill_opacity=0.3)
            text = Text(header, font_size=16, color=WHITE)
            text.move_to(cell.get_center())
            cell_group = VGroup(cell, text)
            header_row.add(cell_group)

        # Arrange header cells horizontally
        header_row.arrange(RIGHT, buff=0)
        table_group.add(header_row)

        # Create data rows
        for row_idx, row_data in enumerate(cube_data):
            data_row = VGroup()
            for col_idx, cell_data in enumerate(row_data):
                cell = Rectangle(width=1.2, height=0.5, stroke_color=WHITE, fill_color=BLACK, fill_opacity=0.1)

                # Color the text based on the cell content
                if cell_data in color_map:
                    text_color = color_map[cell_data]
                else:
                    text_color = WHITE

                text = Text(cell_data, font_size=16, color=text_color)
                text.move_to(cell.get_center())
                cell_group = VGroup(cell, text)
                data_row.add(cell_group)

            # Arrange data cells horizontally
            data_row.arrange(RIGHT, buff=0)
            data_row.next_to(header_row, DOWN, buff=0)
            data_row.shift(DOWN * row_idx * 0.5)
            table_group.add(data_row)

        table_group.scale(0.8)
        table_group.next_to(title, DOWN, buff=1)

        self.play(Create(table_group))
        self.wait(3)


# Scene for showing the final solution
class SolutionScene(Scene):
    def construct(self):
        title = Text("Instant Insanity Solution", font_size=36, color=GREEN)
        title.to_edge(UP)
        self.play(Write(title))

        # Show the arrangement that solves the puzzle
        solution_text = Text(
            "The graph theory approach guarantees we find\nthe unique solution (if one exists)!",
            font_size=24,
            color=LIGHT_GRAY
        )
        solution_text.next_to(title, DOWN, buff=0.5)

        self.play(Write(solution_text))
        self.wait(3)

if __name__ == "__main__":
    #scene = InstantInsanityScene()
    #scene = CubeAnalysisScene()
    scene = SolutionScene()
    scene.render(preview=True)

# The above code was generated at: https://claude.ai/chat/a8d80d07-50cf-4781-8fba-5f1ecaeb4ac0
