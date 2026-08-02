#!/usr/bin/env python3
"""
Script to print the region of interest marked up on the image in a PDF file.

Usage:
    python src/claude/print_pdf_rectangle.py [pdf_file]

The PDF file defaults to the annotated Eureka table of contents. The region is
printed as a Python constant, ready to paste into a scene.
"""

import sys
from pathlib import Path

from pdf_rectangle import Region, find_first_rectangle

DEFAULT_PDF: Path = Path("src/instant_insanity/resources/images/graph_theory/"
                         "eureka-page-1-toc.pdf-annotated.pdf")


def main() -> None:
    """Main function to handle command line usage."""
    pdf_path: Path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PDF

    if not pdf_path.is_file():
        print(f"Error: '{pdf_path}' does not exist")
        return

    try:
        region: Region = find_first_rectangle(pdf_path)
    except ValueError as error:
        print(f"Error: {error}")
        return

    name: str = pdf_path.stem.split('.')[0].replace('-', '_').upper()
    values: str = ", ".join(f"{value:.4f}" for value in region)

    print(f"# region of {pdf_path.name}")
    print(f"{name}_REGION: Region = ({values})")


if __name__ == "__main__":
    main()
