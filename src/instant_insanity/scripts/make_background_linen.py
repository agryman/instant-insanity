#!/usr/bin/env python3
"""
Script to convert white background to transparent using flood fill from borders.
This preserves white pixels within the image content (like on cubes) while removing
only the background white pixels connected to the image borders.
"""

from PIL import Image
import sys
from pathlib import Path


def is_white_ish(pixel, tolerance=10):
    """Check if a pixel is white-ish within tolerance."""
    if len(pixel) == 3:  # RGB
        r, g, b = pixel
        return all(abs(255 - c) <= tolerance for c in [r, g, b])
    elif len(pixel) == 4:  # RGBA
        r, g, b, a = pixel
        return all(abs(255 - c) <= tolerance for c in [r, g, b]) and a > 200
    return False


def flood_fill_background(img, tolerance=10):
    """Flood fill from border pixels to identify background areas."""
    width, height = img.size
    pixels = img.load()
    
    # Track which pixels are background
    background_mask = [[False for _ in range(width)] for _ in range(height)]
    visited = [[False for _ in range(width)] for _ in range(height)]
    
    def flood_fill_iterative(start_x, start_y):
        """Iterative flood fill to avoid recursion depth issues."""
        stack = [(start_x, start_y)]
        
        while stack:
            x, y = stack.pop()
            
            # Check bounds and if already visited
            if (x < 0 or x >= width or y < 0 or y >= height or 
                visited[y][x] or not is_white_ish(pixels[x, y], tolerance)):
                continue
            
            # Mark as visited and background
            visited[y][x] = True
            background_mask[y][x] = True
            
            # Add neighbors to stack
            stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    
    # Start flood fill from all border pixels that are white-ish
    border_pixels = []
    
    # Top and bottom edges
    for x in range(width):
        border_pixels.extend([(x, 0), (x, height - 1)])
    
    # Left and right edges (excluding corners to avoid duplicates)
    for y in range(1, height - 1):
        border_pixels.extend([(0, y), (width - 1, y)])
    
    # Perform flood fill from each border pixel
    for x, y in border_pixels:
        if is_white_ish(pixels[x, y], tolerance) and not visited[y][x]:
            flood_fill_iterative(x, y)
    
    return background_mask


def make_background_transparent(input_path, output_path, tolerance=10, fill_color=(236, 230, 226)):
    """
    Convert white background to specific fill color using flood fill from borders.
    
    Args:
        input_path: Path to input PNG file
        output_path: Path for output PNG file with filled background
        tolerance: Color tolerance for matching white pixels (0-255)
        fill_color: RGB tuple for background fill color (default: LINEN #ece6e2)
    """
    try:
        # Open and convert to RGBA
        img = Image.open(input_path).convert("RGBA")
        width, height = img.size
        pixels = img.load()
        assert isinstance(pixels, Image.core.PixelAccess)
        
        print(f"Processing image: {width}x{height} pixels")
        print(f"Tolerance: {tolerance}")
        
        # Get background mask using flood fill
        print("Performing flood fill from borders...")
        background_mask = flood_fill_background(img, tolerance)
        
        # Count background pixels
        background_count = sum(sum(row) for row in background_mask)
        print(f"Found {background_count} background pixels to fill with color {fill_color}")
        
        # Apply fill color to background pixels
        filled_count = 0
        for y in range(height):
            for x in range(width):
                if background_mask[y][x]:
                    # Set to fill color with full opacity
                    pixels[x, y] = (fill_color[0], fill_color[1], fill_color[2], 255)
                    filled_count += 1
        
        # Save result
        img.save(output_path, "PNG")
        print(f"Saved image with filled background to: {output_path}")
        print(f"Filled {filled_count} pixels with color {fill_color}")
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return False
    
    return True


def main():
    """Main function to handle command line usage."""
    if len(sys.argv) < 2:
        print("Usage: python make_background_transparent.py <input_file> [output_file] [tolerance] [fill_color]")
        print("  input_file: PNG file to process")
        print("  output_file: Output file (optional, defaults to input_linen.png)")
        print("  tolerance: Color matching tolerance 0-255 (optional, default 10)")
        print("  fill_color: 'linen' or 'R,G,B' format (optional, default linen)")
        return
    
    input_path = Path(sys.argv[1])
    
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' does not exist")
        return
    
    # Determine output path
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        output_path = input_path.parent / f"{input_path.stem}_linen.png"
    
    # Get tolerance
    tolerance = 10
    if len(sys.argv) >= 4:
        try:
            tolerance = int(sys.argv[3])
            if not 0 <= tolerance <= 255:
                print("Tolerance must be between 0 and 255")
                return
        except ValueError:
            print("Tolerance must be an integer")
            return
    
    # Get fill color
    fill_color = (236, 230, 226)  # Default LINEN #ece6e2
    if len(sys.argv) >= 5:
        color_arg = sys.argv[4].lower()
        if color_arg == 'linen':
            fill_color = (236, 230, 226)
        else:
            try:
                # Parse R,G,B format
                rgb_parts = color_arg.split(',')
                if len(rgb_parts) == 3:
                    rgb: list[int] = [int(c.strip()) for c in rgb_parts]
                    fill_color = (rgb[0], rgb[1], rgb[2])
                    # Validate RGB values
                    if not all(0 <= c <= 255 for c in fill_color):
                        print("RGB values must be between 0 and 255")
                        return
                else:
                    print("Color format must be 'linen' or 'R,G,B' (e.g., '250,240,230')")
                    return
            except ValueError:
                print("Invalid color format. Use 'linen' or 'R,G,B' (e.g., '250,240,230')")
                return
    
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Fill color: {fill_color}")
    
    success = make_background_transparent(str(input_path), str(output_path), tolerance, fill_color)
    
    if success:
        print("✓ Conversion completed successfully!")
    else:
        print("✗ Conversion failed")


if __name__ == "__main__":
    main()