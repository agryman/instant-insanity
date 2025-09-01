#!/usr/bin/env python3
"""
Create a Manim-compatible image by converting transparency to a specific color
that can then be made transparent in Manim using color-based transparency.
"""

from PIL import Image
import sys
from pathlib import Path


def create_manim_compatible_transparent_image(input_path, output_path, bg_color=(0, 255, 0)):
    """
    Convert PNG with alpha channel to PNG with colored background for Manim.
    
    Args:
        input_path: Input PNG with alpha channel
        output_path: Output PNG with colored background instead of transparency
        bg_color: RGB color to use for transparent areas (default: bright green for chroma key)
    """
    try:
        # Open the image
        img = Image.open(input_path).convert("RGBA")
        width, height = img.size
        pixels = img.load()
        
        # Create a new RGB image with the background color
        new_img = Image.new("RGB", (width, height), bg_color)
        new_pixels = new_img.load()
        
        # Process each pixel
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                
                if a > 128:  # Non-transparent pixel
                    # Use the original RGB values
                    new_pixels[x, y] = (r, g, b)
                else:  # Transparent pixel
                    # Use background color (will be made transparent in Manim)
                    new_pixels[x, y] = bg_color
        
        # Save the result
        new_img.save(output_path, "PNG")
        print(f"Created Manim-compatible image: {output_path}")
        print(f"Transparent areas are now {bg_color} (use this for chroma key in Manim)")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python create_manim_compatible_image.py <input_png> [output_png]")
        return
    
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path.parent / f"{input_path.stem}_manim.png"
    
    success = create_manim_compatible_transparent_image(input_path, output_path)
    if success:
        print("\n✓ Now use this in your Manim scene with:")
        print(f'image = ImageMobject("{output_path}")')
        print("# TODO: Add chroma key removal code to make green transparent")


if __name__ == "__main__":
    main()