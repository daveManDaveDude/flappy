"""
pipe.py: defines the Pipe obstacle for Flappy Bird.
Each Pipe consists of a top and bottom rectangle, moving left across the screen.
"""
import pygame
import random
import settings


class Pipe(pygame.sprite.Sprite):
    """A pair of pipes as one sprite: top and bottom segments with a gap."""
    def __init__(self, x, speed=None, gap=None, top_height=None):
        super().__init__()
        # speed can vary over time
        self.speed = speed if speed is not None else settings.PIPE_SPEED
        self.width = settings.PIPE_WIDTH
        # gap size (allow per-pipe randomness)
        self.gap = gap if gap is not None else settings.PIPE_GAP
        # determine top-pipe height (optionally constrained)
        min_top = settings.PIPE_MIN_HEIGHT
        max_top = settings.HEIGHT - settings.PIPE_MIN_HEIGHT - self.gap
        if top_height is None:
            self.top_height = random.randint(min_top, max_top)
        else:
            # clamp provided top_height to allowable range
            self.top_height = max(min(top_height, max_top), min_top)
        bottom_y = self.top_height + self.gap
        bottom_height = settings.HEIGHT - bottom_y
        # collision rects
        self.top_rect = pygame.Rect(x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(x, bottom_y, self.width, bottom_height)
        # create the visual image of both segments
        image = pygame.Surface((self.width, settings.HEIGHT), pygame.SRCALPHA)
        # top pipe
        pygame.draw.rect(image, settings.PIPE_COLOR, (0, 0, self.width, self.top_height))
        # bottom pipe
        pygame.draw.rect(image, settings.PIPE_COLOR, (0, bottom_y, self.width, bottom_height))
        # bounce-zone indicator (yellow stripe)
        self.bounce_zone = (random.random() < settings.PIPE_BOUNCE_CHANCE)
        if self.bounce_zone:
            stripe_height = settings.PIPE_BOUNCE_STRIPE_HEIGHT
            pygame.draw.rect(
                image,
                settings.BOUNCE_STRIPE_COLOR,
                (0, bottom_y, self.width, stripe_height)
            )
        # assign sprite attributes and track float x-position for smooth movement
        self.image = image
        self.rect = image.get_rect(topleft=(x, 0))
        # float-based x position for sub-pixel movement
        self.pos_x = float(self.rect.x)
        # scoring flags
        self.bounced = False
        self.passed = False

    def update(self, dt):
        """Move the pipe left by speed * dt and update collision rects."""
        # compute movement in pixels (float)
        dx = self.speed * (dt / 1000.0)
        # update float position and apply to rect
        self.pos_x -= dx
        new_x = int(self.pos_x)
        self.rect.x = new_x
        # update collision rects to match
        self.top_rect.x = new_x
        self.bottom_rect.x = new_x


    def off_screen(self):
        """Return True if pipe has moved entirely off the left edge."""
        return self.rect.right < 0