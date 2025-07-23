"""
https://claude.ai/chat/201b45e1-48ba-4ab4-9712-ae58b7fd48d1
https://claude.ai/public/artifacts/72037ea3-b5c8-4ad1-b3e6-9f80c2784acd

This code animates two cube faces moving apart in 3D space, with a connecting line that updates its position accordingly.
"""

import numpy as np

from manim import (    ThreeDScene, Rotate, config,
    UP, LEFT, RIGHT, PI, DEGREES,
    WHITE, Square, Line3D, UpdateFromFunc, BLACK, BLUE, RED, YELLOW,
    PURE_BLUE, PURE_RED, PURE_GREEN
)
from manim.typing import Point3D

config.background_color = WHITE  # must be set before scene instantiation


# Version with more explicit z-order control
class CubeFacesAnimationWithZOrder(ThreeDScene):
 
    def update_mobjects_z_index(self):
        """Update z_index for all objects based on distance from camera"""

        # Get the camera position in 3D space
        phi: float = self.camera.get_phi()
        theta: float = self.camera.get_theta()
        focal_distance: float = self.camera.get_focal_distance()

        x: float = focal_distance * np.sin(phi) * np.cos(theta)
        y: float = focal_distance * np.sin(phi) * np.sin(theta)
        z: float = focal_distance * np.cos(phi)
        camera_pos: Point3D = np.array([x, y, z])
        
        for obj in self.mobjects:
            obj_pos = obj.get_center()
            distance = np.linalg.norm(obj_pos - camera_pos)
            obj.z_index = -distance  # Negative so farther objects have lower z_index
    
    def sort_mobjects_by_z_index(self):
        """Sort the scene's mobjects by their z_index in-place"""
        self.mobjects.sort(key=lambda obj: obj.z_index)

    def update_mobjects_z_order(self):
        self.update_mobjects_z_index()
        self.sort_mobjects_by_z_index()

    def construct(self):
        # Set up 3D camera
        # self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.set_camera_orientation(phi=-30 * DEGREES, theta=-90 * DEGREES)

        radius: float = 2.5
        radius_vector: Point3D = np.array([radius, 0, 0])
        
        # Create the right face (at x = radius)
        right_face = Square(side_length=1, fill_opacity=1.0, fill_color=YELLOW, stroke_color=BLACK, stroke_width=2)
        right_face.rotate(PI/2, axis=UP)
        right_face.move_to(radius_vector)
        
        # Create the left face (at x = -radius)
        left_face = Square(side_length=1, fill_opacity=1.0, fill_color=RED, stroke_color=BLACK, stroke_width=2)
        left_face.rotate(PI/2, axis=UP)
        left_face.rotate(PI, axis=RIGHT)
        left_face.move_to(-1.0*radius_vector)

        # self.scene_objects = [left_face, right_face]

        # self.add(*self.scene_objects)
        # self.update_mobjects_z_order()

        # self.wait(2)
        
        def make_line():
            left_centre = left_face.get_center()
            right_centre = right_face.get_center()
            return Line3D(
                start=left_centre,
                end=right_centre,
                color=BLACK,
                stroke_width=1
            )

        connecting_line: Line3D = make_line()
        # self.scene_objects.append(connecting_line)
        # self.add(connecting_line)
        # self.update_mobjects_z_order()

        self.add(left_face, right_face, connecting_line)
        
        # self.wait(2)

        # During animation, we need to move the line and manage z-order
        def update_line_and_z_order(line):
            # Update line position using the working method
            new_line = make_line()
            line.become(new_line)
            
            # Update z-order based on camera position
            self.update_mobjects_z_order()
        
        # Add the updater to the line
        # connecting_line.add_updater(update_line_and_z_order)
        
        # Animate the faces moving outward
        # self.play(
        #     left_face.animate.move_to(-2.0*radius_vector),
        #     right_face.animate.move_to(2.0*radius_vector),
        #     run_time=3
        # )
        
        # Remove the updater
        # connecting_line.remove_updater(update_line_and_z_order)

        # self.wait(2)
        
        # # Show different camera angles
        # self.move_camera(phi=45 * DEGREES, theta=45 * DEGREES, run_time=2)
        # self.wait(1)
        
        # self.move_camera(phi=90 * DEGREES, theta=0 * DEGREES, run_time=2)
        # self.wait(1)


# Usage example:
# To render the animation, save this file and run:
# manim -pql filename.py CubeFacesAnimation
# or
# manim -pql filename.py CubeFacesAnimationWithZOrder

# For running the scene directly
if __name__ == "__main__":
    scene = CubeFacesAnimationWithZOrder()
    scene.render(preview=True)
