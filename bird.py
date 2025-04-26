import pygame
from pygame.math import Vector2
import settings
import assets


class Bird(pygame.sprite.Sprite):
    """
    A simple bird that can flap and is affected by gravity.
    Manages its own animation and physics.
    """
    def __init__(self, x, y):
        super().__init__()
        # Position and physics
        self.pos = Vector2(x, y)
        self.velocity = 0

        # Load and scale images
        base = assets.load_image("wings_level.png")
        down = assets.load_image("wings_down.png")
        up   = assets.load_image("wings_up.png")

        # Smooth scale each image down by SCALE_FACTOR
        def scale(img):
            w, h = img.get_size()
            return pygame.transform.smoothscale(img, (w // settings.SCALE_FACTOR, h // settings.SCALE_FACTOR))

        self.base_image = scale(base)
        self.anim_frames = [scale(down), self.base_image, scale(up)]

        # Animation state
        self.anim_index = 0
        self.anim_timer = 0
        self.frame_duration = settings.FRAME_DURATION
        self.animating = False

        # Sprite initial image and rect
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        """
        Update velocity, position, handle collisions, and animate wings.
        dt: elapsed milliseconds since last frame.
        """
        dt_sec = dt / 1000.0
        self.velocity += settings.GRAVITY * dt_sec
        self.pos.y += self.velocity * dt_sec

        # (floor/ceiling collision will occur after choosing image to use its dimensions)

        # Handle animation frames
        if self.animating:
            self.anim_timer += dt
            if self.anim_timer >= self.frame_duration:
                self.anim_timer -= self.frame_duration
                self.anim_index += 1
                if self.anim_index >= len(self.anim_frames):
                    self.animating = False

        # Choose current image
        if self.animating:
            self.image = self.anim_frames[self.anim_index]
        else:
            self.image = self.base_image

        # Floor/ceiling collision based on current frame height
        half_h = self.image.get_height() / 2
        if self.pos.y > settings.HEIGHT - half_h:
            self.pos.y = settings.HEIGHT - half_h
            self.velocity = -self.velocity * settings.RESTITUTION
        elif self.pos.y < half_h:
            self.pos.y = half_h
            self.velocity = 0
        # Update rect to new position and size
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def flap(self):
        """
        Apply an upward impulse and start wing flap animation.
        """
        self.velocity = settings.JUMP_VELOCITY
        if not self.animating:
            self.animating = True
            self.anim_index = 0
            self.anim_timer = 0