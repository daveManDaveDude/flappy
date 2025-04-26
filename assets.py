import pygame
import os

__all__ = ["load_image"]

# Cache for loaded images
_images = {}

def load_image(filename):
    """
    Load an image with alpha channel and cache it.
    Raises a pygame error if the file is not found.
    """
    if filename not in _images:
        # images now reside in the sprites/ directory
        path = os.path.join(os.path.dirname(__file__), 'sprites', filename)
        image = pygame.image.load(path).convert_alpha()
        _images[filename] = image
    return _images[filename]