# Animators Class Diagram
*Arthur Ryman, last updated 2025-08-19*


```mermaid
classDiagram
    Animation <|-- AnimorphAnimation
    Mobject <|-- ValueTracker
    Animorph *-- Mobject  : mobject
    Animorph <|-- PolygonToDotAnimorph
    ValueTracker --* Animorph : alpha_tracker
    Animorph --* AnimorphAnimation : animorph
    Mobject <|-- VMobject
    VMobject <|-- VGroup
    VGroup <|-- TrackedVGroup
    ValueTracker --* TrackedVGroup : tracker
    TrackedVGroup <|-- TrackedPolygon
    TrackedVGroup <|-- ThreeDPolygons
    ThreeDPolygons <|-- ThreeDPuzzleCube
    TrackedVGroup --* TrackedVGroupAnimator : tracked_vgroup
    TrackedVGroupAnimator <|-- CubeAnimator
    ThreeDPuzzleCube --* CubeAnimator : tracked_vgroup
    CubeAnimator <|-- CubeRigidMotionAnimator
    CubeAnimator <|-- CubeExplosionAnimator
    TrackedVGroupAnimator <|-- ThreeDPolygonsAnimator
    TrackedVGroupAnimator <|-- PolygonToDotAnimator
    TrackedVGroupAnimator <|-- AnimorphAnimator
    
    class Animorph {
        mobject: Mobject
        alpha_tracker: ValueTracker
        morph_to()*
    }
    <<abstract>> Animorph

    class TrackedVGroup {
        tracker: ValueTracker
    }
    
    class AnimorphAnimation {
        animorph: Animorph
        interpolate_mobject()
    }
    class TrackedVGroupAnimator {
        tracked_vgroup: TrackedVGroup
        mk_updater(self) Updater 
        play()
        interpolate()*
    }
    <<abstract>> TrackedVGroupAnimator
    <<abstract>> CubeAnimator
```