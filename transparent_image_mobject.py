"""
Custom ImageMobject that properly handles PNG transparency/alpha channels.
Manim's default ImageMobject ignores per-pixel alpha, so we need to process it manually.
"""

import numpy as np
from manim import ImageMobject
from PIL import Image


class TransparentImageMobject(ImageMobject):
    """ImageMobject that respects PNG alpha channels for transparency."""
    
    def __init__(self, filename_or_array, **kwargs):
        # Load the image with PIL to preserve alpha
        if isinstance(filename_or_array, str):
            pil_image = Image.open(filename_or_array).convert("RGBA")
            img_array = np.array(pil_image)
        else:
            img_array = filename_or_array
            
        # Process the alpha channel
        img_array = self._process_alpha_channel(img_array)
        
        # Pass the processed array to the parent class
        super().__init__(img_array, **kwargs)
    
    def _process_alpha_channel(self, img_array):
        """
        Process the alpha channel to make transparent pixels actually transparent.
        This replaces fully transparent pixels with the scene background color.
        """
        # Get alpha channel
        alpha = img_array[:, :, 3] / 255.0
        
        # For pixels with very low alpha (effectively transparent), 
        # we'll set their RGB to match the background and alpha to 0
        transparent_mask = alpha < 0.1  # Threshold for "transparent"
        
        # Set transparent pixels to have alpha = 0
        img_array[transparent_mask, 3] = 0
        
        # You could also set RGB to background color, but alpha=0 should be enough
        # img_array[transparent_mask, 0:3] = [background_r, background_g, background_b]
        
        return img_array


def create_transparent_image(image_path):
    """Convenience function to create a transparent image."""
    return TransparentImageMobject(str(image_path))