from importlib.resources import files, as_file
from importlib.resources.abc import Traversable
from pathlib import Path
from manim import Mobject, SVGMobject, ImageMobject

IMAGES_BASE_PATH: str = "instant_insanity.resources.images"

class ImagesPath:
    """
    This class represents a directory of image files stored within the package.
    """
    images_path: str

    def __init__(self, images_path: str = IMAGES_BASE_PATH) -> None:
        self.images_path = images_path

    def get_image(self, subpackage: str, filename: str) -> Mobject:
        package: str = self.images_path
        if len(subpackage) > 0:
            package = package + "." + subpackage
        resource: Traversable = files(package) / filename
        image_full_path: Path
        image: Mobject
        with as_file(resource) as image_full_path:
            if filename.endswith('.svg'):
                image = SVGMobject(image_full_path)
            else:
                image = ImageMobject(image_full_path)

        return image
