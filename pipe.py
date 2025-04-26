"""
pipe.py: defines the Pipe obstacle for Flappy Bird.
Each Pipe consists of a top and bottom rectangle, moving left across the screen.
"""
import pygame
import random
import settings


class Pipe:
    """A pair of pipes with a gap, moving left at constant speed."""
    def __init__(self, x, speed=None, gap=None):
        # Horizontal position and movement
        self.x = x
        # speed can vary over time
        self.speed = speed if speed is not None else settings.PIPE_SPEED
        self.width = settings.PIPE_WIDTH
        # Gap settings (allow per-pipe randomness)
        self.gap = gap if gap is not None else settings.PIPE_GAP
        # Determine random top-pipe height based on this gap
        max_top = settings.HEIGHT - settings.PIPE_MIN_HEIGHT - self.gap
        self.top_height = random.randint(settings.PIPE_MIN_HEIGHT, max_top)
        # Create rects for top and bottom segments
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom_y = self.top_height + self.gap
        bottom_height = settings.HEIGHT - bottom_y
        self.bottom_rect = pygame.Rect(self.x, bottom_y, self.width, bottom_height)
        # decide if this pipe supports bounce on its bottom segment
        # roughly 1 in 5 pipes have bounce zones
        self.bounce_zone = (random.random() < 0.2)
        # flags for bounce and passing scoring
        self.bounced = False
        self.passed = False
        # flags for bounce scoring and passing scoring
        self.bounced = False
        self.passed = False

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
        # debug bounce-zone indicator: thin yellow stripe at top of bottom pipe
        if self.bounce_zone:
            stripe_rect = pygame.Rect(
                self.bottom_rect.x,
                self.bottom_rect.y,
                self.width,
                5
            )
            pygame.draw.rect(surface, (255, 255, 0), stripe_rect)

    def off_screen(self):
        """Return True if pipe has moved entirely off the left edge."""
        return self.x + self.width < 0