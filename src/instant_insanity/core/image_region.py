"""
This module finds the region of interest of an image.

A Manim scene may zoom in on part of an image, for example a single line of the
table of contents of a journal. Rather than measuring that region by hand, keep
two copies of the image. Annotate the second copy in Preview by drawing a red
rectangle around the region with the Rectangle markup tool. The scene then
displays the original and reads the region off the annotated copy.

Preview writes markup into whichever file it has open, so always annotate a copy
and leave the original closed.
"""

import numpy as np
from PIL import Image

type Region = tuple[float, float, float, float]
"""
A rectangular region of interest of an image, namely u0, v0, u1, v1, given as
fractions of the image width and height with the origin at the top left corner
of the image.
"""

# a markup pixel is a strong red, which distinguishes it from the browns and
# oranges of the foxing spots on an old scanned page
MIN_RED: int = 150
MAX_OTHER: int = 110
MIN_EXCESS: int = 80


def find_red_mask(image: Image.Image) -> np.ndarray:
    """
    Finds the pixels of an image that were drawn with red markup.

    Args:
        image: the annotated image.

    Returns:
        A boolean array, True where the pixel is markup red.
    """
    pixels: np.ndarray = np.asarray(image.convert('RGB'))
    red: np.ndarray = pixels[..., 0].astype(np.int16)
    green: np.ndarray = pixels[..., 1].astype(np.int16)
    blue: np.ndarray = pixels[..., 2].astype(np.int16)

    return ((red >= MIN_RED) &
            (green <= MAX_OTHER) &
            (blue <= MAX_OTHER) &
            (red - np.maximum(green, blue) >= MIN_EXCESS))


def find_red_rectangle(image: Image.Image) -> Region:
    """
    Finds the region enclosed by the red rectangle drawn on an image.

    The rectangle is drawn with a stroke of some thickness, so its red pixels
    form a ring. The region returned follows the centre line of that ring,
    which is the rectangle as drawn.

    Args:
        image: the annotated image.

    Returns:
        The region, namely u0, v0, u1, v1 as fractions of the image width and
        height, with the origin at the top left corner of the image.

    Raises:
        ValueError: if the image has no red markup on it.
    """
    mask: np.ndarray = find_red_mask(image)
    height, width = mask.shape

    rows: np.ndarray = np.nonzero(mask.any(axis=1))[0]
    columns: np.ndarray = np.nonzero(mask.any(axis=0))[0]

    if len(rows) == 0:
        raise ValueError("the image has no red rectangle drawn on it")

    x0, x1 = int(columns[0]), int(columns[-1])
    y0, y1 = int(rows[0]), int(rows[-1])

    # the bounding box follows the outer edge of the stroke, so move in by half
    # its thickness, which is the area of the ring divided by its perimeter
    perimeter: int = 2 * ((x1 - x0 + 1) + (y1 - y0 + 1))
    inset: float = float(mask.sum()) / perimeter / 2.0

    return (float((x0 + inset) / width),
            float((y0 + inset) / height),
            float((x1 - inset) / width),
            float((y1 - inset) / height))
