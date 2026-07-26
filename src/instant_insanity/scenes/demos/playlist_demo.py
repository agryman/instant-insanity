"""
This module explores how to selectively enable the execution of subscenes within a scene.
"""

class MyScene:
    playlist: list[object] = list()

    def skip(self, method: object) -> bool:
        return len(self.playlist) > 0 and method not in self.playlist

    def subscene_1(self) -> None:
        if self.skip(self.subscene_1):
            return
        print("This is subscene 1")

    def subscene_2(self) -> None:
        if self.skip(self.subscene_2):
            return
        print("This is subscene 2")

    def subscene_3(self) -> None:
        if self.skip(self.subscene_3):
            return
        print("This is subscene 3")

    def play(self) -> None:
        self.subscene_1()
        self.subscene_2()
        self.subscene_3()


def main() -> None:
    scene = MyScene()
    scene.playlist = [scene.subscene_1, scene.subscene_3]
    scene.play()

if __name__ == "__main__":
    main()
