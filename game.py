import pygame
import sys

import settings
# Import Bird from the root-level bird.py first; fallback to sprites/bird.py
try:
    from bird import Bird
except ImportError:
    from sprites.bird import Bird


class Game:
    """
    Main game class: handles initialization, the game loop, events, updates, and rendering.
    """
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

        # Sprite setup
        self.bird = Bird(100, settings.HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group(self.bird)

        self.running = True

    def run(self):
        """
        Main loop: process input, update state, draw, repeat until exit.
        """
        while self.running:
            dt = self.clock.tick(settings.FPS)
            self.handle_events()
            self.all_sprites.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self):
        """
        Handle all pending pygame events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.bird.flap()

    def draw(self):
        """
        Draw background, sprites, and UI.
        """
        self.screen.fill((135, 206, 235))  # sky blue
        self.all_sprites.draw(self.screen)
        text = self.font.render("Press SPACE to flap, Q to quit", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))
        pygame.display.flip()