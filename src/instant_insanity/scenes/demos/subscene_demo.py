"""
This module demonstrates how to selectively execute the subscenes of a scene
using SubsceneMixin.

SubsceneMixin is normally inherited together with VoiceoverScene, but it has no
Manim dependency, so this demo uses plain classes that print their subscenes
instead of rendering them. Run this module to see the effect of a playlist.
"""
from typing import Sequence

from instant_insanity.scenes.subscene import SubsceneMixin, Subscene


class DemoScene(SubsceneMixin):
    """
    A scene divided into three subscenes.

    This class does not override get_playlist, so it inherits the default empty
    playlist and therefore renders all of its subscenes. This is the normal
    state of a finished scene.
    """

    def subscene_1_introduction(self) -> None:
        if self.skip(self.subscene_1_introduction):
            return
        print("This is subscene_1_introduction.")

    def subscene_2_development(self) -> None:
        if self.skip(self.subscene_2_development):
            return
        print("This is subscene_2_development.")

    def subscene_3_conclusion(self) -> None:
        if self.skip(self.subscene_3_conclusion):
            return
        print("This is subscene_3_conclusion.")

    def get_playlist(self) -> Sequence[Subscene]:
        return [
            self.subscene_1_introduction,
            self.subscene_3_conclusion,
        ]

    def construct(self) -> None:
        """
        Renders the scene by calling each subscene in order. Each subscene
        decides for itself whether the playlist omits it.
        """
        self.subscene_1_introduction()
        self.subscene_2_development()
        self.subscene_3_conclusion()


def main() -> None:
    scene: DemoScene = DemoScene()
    print("playlist: ", scene.get_playlist())
    scene.construct()


if __name__ == "__main__":
    main()