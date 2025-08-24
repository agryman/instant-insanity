# Animators Class Diagram
*Arthur Ryman, last updated 2025-08-23*


```mermaid
classDiagram
    Animation <|-- AnimorphAnimation
    Animorph *-- Mobject  : mobject
    Animorph <|-- MoveToAnimorph
    Animorph <|-- PolygonToDotAnimorph
    Animorph <|-- CubeAnimorph
    ThreeDPuzzleCube --* CubeAnimorph : mobject
    CubeAnimorph <|-- CubeRigidMotionAnimorph
    CubeAnimorph <|-- CubeExplosionAnimorph
    Animorph --* AnimorphAnimation : animorph
    Mobject <|-- VMobject
    VMobject <|-- Polygon
    VMobject <|-- Dot
    Polygon --* PolygonToDotAnimorph : mobject
    Dot --* PolygonToDotAnimorph : dot
    VMobject <|-- VGroup
    VGroup <|-- Polygons3D
    Polygons3D <|-- PuzzleCube3D
    Polygons3D <|-- Puzzle3D
    PuzzleCube3D --* Puzzle3D
    
    <<manin>> Mobject
    <<manim>> VMobject
    <<manim>> VGroup
    <<manim>> Dot
    <<manin>> Polygon
    
    class Polygons3D {
        projection: Projection
        depth_sorter: DepthSort
        id_to_model_path_0: dict
        id_to_model_path: dict
        id_to_scene_path: OrderedDict
        id_to_scene_polygon: OrderedDict
        update_polygons(id_to_model_path, **polygon_settings)
        conceal_polygons()
        remove_polygons()
    }
    
    class PuzzleCube3D {
        cube_spec: PuzzleCubeSpec
        puzzle_cube: PuzzleCube
        name_to_id(face_name)$
        id_to_name(polygon_id)$
        mk_id_to_model_path_0()$
        get_colour_name(face_name)
        get_manim_colour(face_name)
        update_polygons(id_to_model_path, **polygon_settings)
        
    }
    
    class Puzzle3D {
        puzzle_spec: PuzzleSpec
        cubes: dict[CubeNumber, PuzzleCube3D]
    }
    
    class Animorph {
        alpha: float
        mobject: Mobject
        morph_to()*
        play()
    }
    <<abstract>> Animorph
    
    class MoveToAnimorph {
        start_point
        end_point
    }
    
    class PolygonToDotAnimorph {
        polygon_centre
        w0_radius
        w0_theta
        dot
        doc_centre
        dot_radius
    }
 
    class AnimorphAnimation {
        animorph: Animorph
        interpolate_mobject()
    }
```