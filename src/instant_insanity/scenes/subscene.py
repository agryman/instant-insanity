"""
This module defines the SubsceneMixin class which is intended for use
with Scene and its subclasses.
"""
from typing import Callable, Sequence

type Subscene = Callable[[], None]


class SubsceneMixin:
    """
    Inherit this mixin class to selectively execute the subscenes of a scene.

    A scene is divided into subscenes, each implemented as a method that takes
    no arguments and returns nothing. Rendering a full scene is slow, so during
    development it is useful to render only some of its subscenes.

    Each subscene method guards itself by returning immediately when the
    playlist omits it::

        def subscene_1_introduce_the_graph(self) -> None:
            if self.skip(self.subscene_1_introduce_the_graph):
                return
            ...

    Override get_playlist to render only some subscenes. The default empty
    playlist renders all of them, which is the normal state of a finished scene.
    """

    def get_playlist(self) -> Sequence[Subscene]:
        """
        Override this method to render only some of the subscenes of a scene.

        The returned sequence is recomputed on every call to skip, so it MUST be
        cheap to compute. Return a list of bound subscene methods, for example::

            def get_playlist(self) -> Sequence[Subscene]:
                return [
                    self.subscene_2_discuss_subgraphs,
                    self.subscene_4_discuss_node_degrees,
                ]

        Returns:
            The subscenes to render, or an empty sequence to render all of them.
        """
        return ()

    def skip(self, subscene: Subscene) -> bool:
        """
        Call this method at the start of each subscene method to decide if it
        should return immediately.

        Args:
            subscene: the bound subscene method being guarded.

        Returns:
            True if the playlist is non-empty and omits the subscene.
        """
        playlist: Sequence[Subscene] = self.get_playlist()

        # bound methods compare equal when they have the same instance and function,
        # so the freshly bound subscene argument matches its entry in the playlist
        return len(playlist) > 0 and subscene not in playlist