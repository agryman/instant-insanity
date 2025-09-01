# Manim Mobjects Class Diagram
*Arthur Ryman, last updated 2025-08-19*

```mermaid
classDiagram
    Mobject <|-- VMobject
    VMobject <|-- VGroup
    class Mobject {
        color
        name
        dim
        target
        z_index
        point_hash
        submobjects
        updaters
        updating_suspended
        points
        reset_points()
        generate_points()
        init_colors()
    }
```

