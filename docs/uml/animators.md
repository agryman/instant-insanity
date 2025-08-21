# Animators Class Diagram
*Arthur Ryman, last updated 2025-08-19*


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
    VGroup <|-- ThreeDPolygons
    ThreeDPolygons <|-- ThreeDPuzzleCube
    
    <<manin>> Mobject
    <<manim>> VMobject
    <<manim>> VGroup
    <<manim>> Dot
    <<manin>> Polygon
    
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