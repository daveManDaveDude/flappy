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
        # Load bird wing frames and burnt sprite
        base_img = assets.load_image("wings_level.png")
        down_img = assets.load_image("wings_down.png")
        up_img   = assets.load_image("wings_up.png")
        # sprite to show after explosion
        burnt_img = assets.load_image("bird_burnt.png")

        # Smooth scale each image down by SCALE_FACTOR
        def scale(img):
            w, h = img.get_size()
            return pygame.transform.smoothscale(img, (w // settings.SCALE_FACTOR, h // settings.SCALE_FACTOR))

        # Smooth scale images down by SCALE_FACTOR
        self.base_image = scale(base_img)
        self.anim_frames = [scale(down_img), self.base_image, scale(up_img)]
        # Pre-scale burnt image for post-explosion display (scaled down by an extra factor)
        burnt_scaled = scale(burnt_img)
        # further reduce size by factor 2.2 for a slightly smaller sprite
        factor = 2.2
        new_w = max(1, int(burnt_scaled.get_width() / factor))
        new_h = max(1, int(burnt_scaled.get_height() / factor))
        self.burnt_image = pygame.transform.smoothscale(
            burnt_scaled,
            (new_w, new_h)
        )

        # Animation state
        self.anim_index = 0
        self.anim_timer = 0
        self.frame_duration = settings.FRAME_DURATION
        self.animating = False

        # Sprite initial image and rect
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(x, y))
        # freeze flag: skip updates when True (e.g., after explosion)
        self.frozen = False

    def update(self, dt):
        """
        Update bird physics, animation, constraints, and sprite rect.
        dt: elapsed milliseconds since last frame.
        """
        if self.frozen:
            return
        self._update_physics(dt)
        self._update_animation(dt)
        self._apply_constraints()
        self._update_rect()

    def _update_physics(self, dt):
        """Apply gravity to velocity and update vertical position."""
        dt_sec = dt / 1000.0
        self.velocity += settings.GRAVITY * dt_sec
        self.pos.y += self.velocity * dt_sec

    def _update_animation(self, dt):
        """Advance wing-flap animation frames."""
        if self.animating:
            self.anim_timer += dt
            if self.anim_timer >= self.frame_duration:
                self.anim_timer -= self.frame_duration
                self.anim_index += 1
                if self.anim_index >= len(self.anim_frames):
                    self.animating = False
        self.image = self.anim_frames[self.anim_index] if self.animating else self.base_image

    def _apply_constraints(self):
        """Prevent bird from moving above the top of the screen."""
        half_h = self.image.get_height() / 2
        if self.pos.y < half_h:
            self.pos.y = half_h
            self.velocity = 0

    def _update_rect(self):
        """Update the sprite rect based on current image and position."""
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