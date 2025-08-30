"""
Demo scene showing how to create undirected graphs with CubicBezier edges and Dot nodes,
then add directional arrows that touch the node perimeters.
"""

import numpy as np
from manim import (
    Scene, CubicBezier, Dot, StealthTip, VGroup, FadeIn, Write, Wait,
    UP, DOWN, LEFT, RIGHT, OUT, BLUE, RED, GREEN, YELLOW, BLACK, WHITE
)
from manim.typing import Point3D


class DirectedGraphArrowDemo(Scene):
    def construct(self):
        # Set white background
        self.camera.background_color = WHITE
        # Create nodes at various positions
        node_positions = {
            'A': 2 * UP + 2 * LEFT,
            'B': 2 * UP + 2 * RIGHT, 
            'C': 2 * DOWN + 2 * RIGHT,
            'D': 2 * DOWN + 2 * LEFT
        }
        
        # Create dots for nodes
        nodes = {}
        node_radius = 0.2
        for label, pos in node_positions.items():
            nodes[label] = Dot(
                point=pos,
                radius=node_radius,
                color=BLUE,
                fill_opacity=1.0,
                stroke_color=BLACK,
                stroke_width=2
            )
        
        # Define edges as tuples (start_node, end_node)
        edge_definitions = [
            ('A', 'B'),
            ('B', 'C'), 
            ('C', 'D'),
            ('D', 'A')
        ]
        
        # Create undirected edges using CubicBezier
        edges = {}
        for start_label, end_label in edge_definitions:
            start_pos = node_positions[start_label]
            end_pos = node_positions[end_label]
            
            # Calculate control points for smooth curves
            direction = end_pos - start_pos
            distance = np.linalg.norm(direction)
            
            # Create slight curve by offsetting control points perpendicular to edge
            perpendicular = np.cross(direction, OUT)
            perpendicular = perpendicular / np.linalg.norm(perpendicular) if np.linalg.norm(perpendicular) > 0 else np.array([0, 0, 0])
            
            curve_offset = 0.3 * distance * perpendicular
            
            start_handle = start_pos + 0.3 * direction + curve_offset
            end_handle = end_pos - 0.3 * direction + curve_offset
            
            edge = CubicBezier(
                start_pos,
                start_handle, 
                end_handle,
                end_pos,
                color=BLACK,
                stroke_width=4
            )
            
            edges[(start_label, end_label)] = edge
        
        # Add all nodes and edges to scene
        self.add(*nodes.values())
        self.add(*edges.values())
        
        # Wait to show undirected graph
        self.wait(1)
        
        # Now add directional arrows
        # Define directions for each edge (start -> end)
        edge_directions = [
            ('A', 'B'),  # A -> B
            ('B', 'C'),  # B -> C
            ('C', 'D'),  # C -> D  
            ('D', 'A')   # D -> A
        ]
        
        arrows = []
        
        for start_label, end_label in edge_directions:
            # Get the corresponding edge
            if (start_label, end_label) in edges:
                edge = edges[(start_label, end_label)]
                reverse = False
            elif (end_label, start_label) in edges:
                edge = edges[(end_label, start_label)]
                reverse = True
            else:
                continue
                
            # Calculate arrow position and direction
            
            # Get point at 80% along the curve
            proportion = 0.8 if not reverse else 0.2
            arrow_pos = edge.point_from_proportion(proportion)
            
            # Calculate tangent at that point by using nearby points
            delta = 0.01
            if not reverse:
                # For forward direction, look slightly ahead
                next_proportion = min(1.0, proportion + delta)
                next_point = edge.point_from_proportion(next_proportion)
                tangent_vector = next_point - arrow_pos
            else:
                # For reverse direction, look slightly behind
                prev_proportion = max(0.0, proportion - delta)
                prev_point = edge.point_from_proportion(prev_proportion)
                tangent_vector = arrow_pos - prev_point
            
            # Normalize tangent vector and calculate angle
            if np.linalg.norm(tangent_vector) > 0:
                tangent_unit = tangent_vector / np.linalg.norm(tangent_vector)
                angle = np.arctan2(tangent_unit[1], tangent_unit[0])
                
                # Create arrow tip
                arrow = StealthTip(
                    color=RED,
                    length=0.25,
                    fill_opacity=1.0,
                    stroke_color=BLACK,
                    stroke_width=1
                )
                arrow.rotate(angle)
                
                # Position the arrow tip so its tip point is exactly at arrow_pos
                # For StealthTip, we need to adjust based on its length and rotation
                # The tip extends forward from the center by half its length
                tip_offset = (arrow.length / 2) * tangent_unit
                arrow.move_to(arrow_pos - tip_offset)
                
                arrows.append(arrow)
        
        # Animate arrows fading in
        self.play(FadeIn(*arrows), run_time=2)
        self.wait(2)


if __name__ == "__main__":
    scene = DirectedGraphArrowDemo()
    scene.render()