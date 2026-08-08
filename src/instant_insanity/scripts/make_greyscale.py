#!/usr/bin/env python3
"""
Script to make the greyscale copy of an image that gets annotated.

A scene reads the region of interest of an image off an annotated copy of it,
on which a red rectangle has been drawn around the region. Any red already in
the image would be mistaken for that rectangle, so the copy is converted to
greyscale first. A grey pixel has equal red, green, and blue components, so it
can never be taken for markup.

The copy keeps three colour channels rather than becoming a single channel
greyscale image, since Preview needs a colour capable image to draw red on.

Usage:
    make-greyscale input.png [--force]

The output is always a new file, named after the input with -greyscale added,
so eureka-page-11.png gives eureka-page-11-greyscale.png. Copy that file, with
-greyscale changed to -annotated, and draw the red rectangle on the copy. Open
only the copy in Preview, since Preview writes markup into whichever file it
has open, which would spoil the original or the greyscale version.
"""

import argparse
from pathlib import Path

from PIL import Image, ImageOps

GREYSCALE_SUFFIX: str = "-greyscale"

# the annotated copy takes the same name with the suffix swapped, which is the
# name that scenes read the region of interest from
ANNOTATED_SUFFIX: str = "-annotated"


def get_output_path(input_path: Path) -> Path:
    """
    Gets the output path for an input image.

    Args:
        input_path: the path to the input image.

    Returns:
        The path to the output image, named after the input with -greyscale
        added to its base name.
    """
    return input_path.with_name(input_path.stem + GREYSCALE_SUFFIX + input_path.suffix)


def make_greyscale(image: Image.Image) -> Image.Image:
    """
    Converts an image to greyscale, keeping its colour channels.

    Args:
        image: the image.

    Returns:
        The greyscale image, in RGB or RGBA according to whether the original
        had an alpha channel.
    """
    greyscale: Image.Image = ImageOps.grayscale(image.convert('RGB')).convert('RGB')

    # keep any transparency, so that the copy still looks like the original
    if image.mode in ('RGBA', 'LA') or 'transparency' in image.info:
        greyscale.putalpha(image.convert('RGBA').getchannel('A'))

    return greyscale


def main() -> None:
    """Main function to handle command line usage."""
    parser = argparse.ArgumentParser(
        description="Make the greyscale copy of an image that gets annotated.")
    parser.add_argument("input", type=Path, help="the image to copy")
    parser.add_argument("--force", action="store_true",
                        help="overwrite the output even if it already exists")
    args = parser.parse_args()

    input_path: Path = args.input
    if not input_path.is_file():
        print(f"Error: Input file '{input_path}' does not exist")
        return

    output_path: Path = get_output_path(input_path)

    # the output is where the markup lives, so overwriting it destroys the
    # rectangle that was drawn by hand
    if output_path.exists() and not args.force:
        print(f"Error: '{output_path}' already exists, so any markup on it would be lost")
        print("Use --force to overwrite it")
        return

    image: Image.Image = Image.open(input_path)
    greyscale: Image.Image = make_greyscale(image)
    greyscale.save(output_path)

    annotated_name: str = output_path.name.replace(GREYSCALE_SUFFIX, ANNOTATED_SUFFIX)

    print(f"Input:  {input_path} ({image.width}x{image.height} {image.mode})")
    print(f"Output: {output_path} ({greyscale.width}x{greyscale.height} {greyscale.mode})")
    print(f"✓ Copy the output to '{annotated_name}', then open only that copy "
          f"in Preview and draw one red rectangle on it")


if __name__ == "__main__":
    main()
