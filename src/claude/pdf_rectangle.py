"""
Reads the region of interest of an image out of an annotated PDF file.

The workflow is to copy an image, export the copy as a PDF, open the PDF in
Preview, draw a rectangle around the region of interest with the Rectangle
markup tool, and save it. Preview stores the rectangle as a Square annotation,
which keeps its coordinates as vector data. This module reads them back out and
converts them to fractions of the image, which is what a Manim scene needs in
order to zoom in on the region.

Only the standard library is used, so this understands the small subset of PDF
that Preview and Quartz produce.
"""

import re
import zlib
from pathlib import Path

type Region = tuple[float, float, float, float]

# the /Rect of the first Square annotation, namely x0 y0 x1 y1 in points
RECT_PATTERN: bytes = (rb'/Rect\s*\[\s*([-\d.]+)\s+([-\d.]+)\s+'
                       rb'([-\d.]+)\s+([-\d.]+)\s*\]')

# the placement of an image, namely w 0 0 h x y cm followed by a Do that paints
# it, which gives the rectangle of the page that the image covers
IMAGE_PATTERN: bytes = (rb'([-\d.]+)\s+0\s+0\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)'
                        rb'\s+cm\s*/\w+\s+Do')


def find_streams(data: bytes) -> list[bytes]:
    """
    Finds the streams of a PDF file, decompressing those that are deflated.

    Args:
        data: the contents of the PDF file.

    Returns:
        The decoded streams.
    """
    streams: list[bytes] = []

    for match in re.finditer(rb'stream\r?\n(.*?)endstream', data, re.S):
        raw: bytes = match.group(1)
        try:
            raw = zlib.decompress(raw)
        except zlib.error:
            # the stream is not deflated, for example a JPEG image
            pass

        streams.append(raw)

    return streams


def find_rect(data: bytes) -> tuple[float, float, float, float]:
    """
    Finds the rectangle of the first Square annotation.

    Args:
        data: the contents of the PDF file.

    Returns:
        The rectangle, in points, with the origin at the bottom left corner of
        the page.

    Raises:
        ValueError: if the file holds no Square annotation.
    """
    # scan whole indirect objects, since an annotation nests dictionaries
    # inside itself and so cannot be split on << and >>
    for obj in re.finditer(rb'\d+\s+\d+\s+obj\b(.*?)endobj', data, re.S):
        body: bytes = obj.group(1)
        if b'/Square' not in body:
            continue

        match = re.search(RECT_PATTERN, body)
        if match is not None:
            x0, y0, x1, y1 = (float(value) for value in match.groups())

            return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)

    raise ValueError("no Square annotation, so nothing was marked up")


def find_image_box(data: bytes) -> tuple[float, float, float, float]:
    """
    Finds the rectangle of the page that the first image covers.

    The image need not fill the page. Exporting a portrait image to US Letter
    paper, for example, leaves a margin at each side.

    Args:
        data: the contents of the PDF file.

    Returns:
        The rectangle, in points, as x, y, width, height.

    Raises:
        ValueError: if the file holds no image.
    """
    for stream in find_streams(data):
        match = re.search(IMAGE_PATTERN, stream)
        if match is not None:
            width, height, x, y = (float(value) for value in match.groups())

            return x, y, width, height

    raise ValueError("no image was found")


def find_first_rectangle(pdf_path: Path | str) -> Region:
    """
    Finds the region of interest marked up on the image in a PDF file.

    Args:
        pdf_path: the path to the PDF file.

    Returns:
        The region, namely u0, v0, u1, v1 as fractions of the image width and
        height, with the origin at the top left corner of the image.

    Raises:
        ValueError: if the file holds no annotation or no image.
    """
    data: bytes = Path(pdf_path).read_bytes()

    x0, y0, x1, y1 = find_rect(data)
    image_x, image_y, image_width, image_height = find_image_box(data)

    # PDF measures y upwards from the bottom of the page, but a region measures
    # it downwards from the top of the image, so the y coordinates swap over
    return ((x0 - image_x) / image_width,
            (image_y + image_height - y1) / image_height,
            (x1 - image_x) / image_width,
            (image_y + image_height - y0) / image_height)
