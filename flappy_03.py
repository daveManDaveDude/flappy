"""
Flappy Bird–style prototype using pygame.
Press SPACE to flap, Q to quit.
"""
import pygame
import sys

# Screen settings
WIDTH = 400
HEIGHT = 600
FPS = 60

# Physics constants in per-second units
GRAVITY = 200.0  # downward acceleration (px/sec^2)
JUMP_VELOCITY = -105.0  # flap impulse velocity (px/sec)
# Bouncing behavior: restitution coefficient (1.0 = perfect bounce, <1 for damping)
RESTITUTION = 0.8


class Bird(pygame.sprite.Sprite):
    """A simple bird that can flap and is affected by gravity."""
    RADIUS = 20

    def __init__(self, x, y):
        super().__init__()
        # position and physics
        self.pos = pygame.math.Vector2(x, y)
        self.velocity = 0
        # load sprite frames for wing animation and scale images down by factor of 4
        level_img = pygame.image.load('wings_level.png').convert_alpha()
        down_img  = pygame.image.load('wings_down.png').convert_alpha()
        up_img    = pygame.image.load('wings_up.png').convert_alpha()
        scale_factor = 8
        # scale each image to a quarter of its original dimensions
        lw, lh = level_img.get_size()
        level_img = pygame.transform.scale(level_img, (lw // scale_factor, lh // scale_factor))
        dw, dh = down_img.get_size()
        down_img  = pygame.transform.scale(down_img,  (dw // scale_factor, dh // scale_factor))
        uw, uh = up_img.get_size()
        up_img    = pygame.transform.scale(up_img,    (uw // scale_factor, uh // scale_factor))
        # animation frames: level, down, level, up, level
        self.frames = [level_img, down_img, level_img, up_img, level_img]
        # animation state
        self.anim_index     = 0
        self.anim_timer     = 0
        self.frame_duration = 80   # ms per frame
        self.animating      = False
        # set initial image and rect
        self.image = self.frames[self.anim_index]
        self.rect  = self.image.get_rect(center=(x, y))

    def update(self, dt):
        """Update the bird's velocity and position using elapsed time in ms."""
        dt_sec = dt / 1000.0
        self.velocity += GRAVITY * dt_sec
        self.pos.y += self.velocity * dt_sec
        # floor/ceiling collision
        if self.pos.y > HEIGHT - self.RADIUS:
            # bounce off the floor: invert velocity with damping
            self.pos.y = HEIGHT - self.RADIUS
            self.velocity = -self.velocity * RESTITUTION
        elif self.pos.y < self.RADIUS:
            self.pos.y = self.RADIUS
            self.velocity = 0
        # handle wing animation
        if self.animating:
            self.anim_timer += dt
            if self.anim_timer >= self.frame_duration:
                self.anim_timer -= self.frame_duration
                self.anim_index += 1
                if self.anim_index >= len(self.frames):
                    self.animating = False
                    self.anim_index = 0
        # update image and rect for blitting
        self.image = self.frames[self.anim_index]
        self.rect  = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

    def flap(self):
        """Apply an impulse to make the bird jump and start wing-flap animation."""
        # vertical impulse
        self.velocity = JUMP_VELOCITY
        # initiate wing-flap animation if not already animating
        if not self.animating:
            self.animating  = True
            self.anim_index = 0
            self.anim_timer = 0



def main():
    """Entry point for the game."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Prototype")

    font = pygame.font.SysFont(None, 24)

    bird = Bird(100, HEIGHT // 2)
    # group for sprites: simplifies update and draw
    all_sprites = pygame.sprite.Group(bird)
    running = True

    while running:
        dt = clock.tick(FPS)  # milliseconds since last frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_SPACE:
                    bird.flap()

        all_sprites.update(dt)

        screen.fill((135, 206, 235))  # sky blue background
        all_sprites.draw(screen)

        text = font.render("Press SPACE to flap, Q to quit", True, (0, 0, 0))
        screen.blit(text, (10, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
    sys.exit()
