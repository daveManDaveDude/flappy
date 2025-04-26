"""
pipe.py: defines the Pipe obstacle for Flappy Bird.
Each Pipe consists of a top and bottom rectangle, moving left across the screen.
"""
import pygame
import random
import settings


class Pipe:
    """A pair of pipes with a gap, moving left at constant speed."""
    def __init__(self, x):
        # Horizontal position and movement
        self.x = x
        self.speed = settings.PIPE_SPEED
        self.width = settings.PIPE_WIDTH
        # Gap settings
        self.gap = settings.PIPE_GAP
        # Determine random top-pipe height
        max_top = settings.HEIGHT - settings.PIPE_MIN_HEIGHT - self.gap
        self.top_height = random.randint(settings.PIPE_MIN_HEIGHT, max_top)
        # Create rects for top and bottom segments
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_y = self.top_height + self.gap
        bottom_height = settings.HEIGHT - bottom_y
        self.bottom_rect = pygame.Rect(self.x, bottom_y, self.width, bottom_height)

    def update(self, dt):
        """Move the pipe left by speed * dt."""
        dx = self.speed * (dt / 1000.0)
        self.x -= dx
        # Update rect positions
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def draw(self, surface):
        """Draw black rectangles for pipe segments."""
        pygame.draw.rect(surface, (0, 0, 0), self.top_rect)
        pygame.draw.rect(surface, (0, 0, 0), self.bottom_rect)

    def off_screen(self):
        """Return True if pipe has moved entirely off the left edge."""
        return self.x + self.width < 0