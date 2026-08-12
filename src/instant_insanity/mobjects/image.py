from importlib.resources import files, as_file
from importlib.resources.abc import Traversable
from pathlib import Path
from manim import Mobject, SVGMobject, ImageMobject
from PIL import Image

IMAGES_BASE_PATH: str = "instant_insanity.resources.images"

class ImagesPath:
    """
    This class represents a directory of image files stored within the package.
    """
    images_path: str

    def __init__(self, images_path: str = IMAGES_BASE_PATH) -> None:
        self.images_path = images_path

    def get_resource(self, subpackage: str, filename: str) -> Traversable:
        """
        Gets an image file stored within the package.

        Args:
            subpackage: the subpackage name.
            filename: the image filename.

        Returns:
            The image file.
        """
        package: str = self.images_path
        if len(subpackage) > 0:
            package = package + "." + subpackage

        return files(package) / filename

    def get_image(self, subpackage: str, filename: str) -> Mobject:
        resource: Traversable = self.get_resource(subpackage, filename)
        image_full_path: Path
        image: Mobject
        with as_file(resource) as image_full_path:
            if filename.endswith('.svg'):
                image = SVGMobject(image_full_path)
            else:
                image = ImageMobject(image_full_path)

        return image

    def open_image(self, subpackage: str, filename: str) -> Image.Image:
        """
        Opens an image with Pillow, so that its pixels can be examined.

        Args:
            subpackage: the subpackage name.
            filename: the image filename.

        Returns:
            The image.
        """
        resource: Traversable = self.get_resource(subpackage, filename)
        image_full_path: Path
        image: Image.Image
        with as_file(resource) as image_full_path:
            image = Image.open(image_full_path)

            # read the pixels before the file goes out of scope
            image.load()

        return image

IMAGE_HEIGHT: float = 6.0
INTRODUCTION = "introduction"
GRAPH_THEORY_LATEX: str = "graph_theory.latex"
GRAPH_THEORY: str = "graph_theory"

EUREKA_SOURCE: str = r"https://archim.soc.srcf.net/publications/"
RUBIKS_CUBE_SOURCE: str = r"image by Booyabazooka, CC BY-SA 3.0"
SUDOKU_SOURCE: str = r"© 2025 The New York Times Company"
TRINITY_FOUR_SOURCE: str = r"https://www.squaring.net/history_theory/brooks_smith_stone_tutte.html"
US_PATENT_SOURCE: str = r"https://patents.google.com/patent/US646463A/en"
INSTANT_INSANITY_SOURCE: str = r"https://winning-moves.com/product/InstantInsanity.asp"
WORDLE_SOURCE: str = r"© 2025 The New York Times Company"
