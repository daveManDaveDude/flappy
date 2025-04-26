import pygame
import sys

import settings
## Import Bird from root-level bird.py first; fallback to sprites/bird.py
try:
    from bird import Bird
except ImportError:
    from sprites.bird import Bird
## Import Pipe from root-level pipe.py; fallback to sprites/pipe.py
try:
    from pipe import Pipe
except ImportError:
    from sprites.pipe import Pipe


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
        # initialize or reset game data
        self.running = True
        self.start_new_game()

    def start_new_game(self):
        """
        Initialize or reset game state: bird, pipes, score, timers.
        """
        # Bird and sprites
        self.bird = Bird(100, settings.HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group(self.bird)
        # Pipes
        self.pipes = []
        self.pipe_timer = 0
        # Score
        self.score = 0
        self.score_timer = 0
        # Game over flag
        self.game_over = False
        # Spawn initial pipe
        self._spawn_pipe()

    def run(self):
        """
        Main loop: process input, update state, draw, repeat until exit.
        """
        while self.running:
            dt = self.clock.tick(settings.FPS)
            self.handle_events()
            # update game only if not game over
            if not self.game_over:
                self.all_sprites.update(dt)
                self._update_pipes(dt)
                self._update_score(dt)
                self._check_collisions()
            # always draw frame
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
                # restart game after game over
                if self.game_over and event.key == pygame.K_r:
                    self.start_new_game()
                # normal flap input only when playing
                if not self.game_over and event.key == pygame.K_SPACE:
                    self.bird.flap()
    
    def _spawn_pipe(self):
        """
        Create a new Pipe at the right edge and add it to the list.
        """
        pipe = Pipe(settings.WIDTH)
        self.pipes.append(pipe)

    def _update_pipes(self, dt):
        """
        Update existing pipes, spawn new ones, and remove off-screen pipes.
        """
        # spawn timer
        self.pipe_timer += dt
        if self.pipe_timer >= settings.PIPE_SPAWN_INTERVAL:
            self.pipe_timer -= settings.PIPE_SPAWN_INTERVAL
            self._spawn_pipe()
        # update and cull
        for pipe in list(self.pipes):
            pipe.update(dt)
            if pipe.off_screen():
                self.pipes.remove(pipe)
    
    def _update_score(self, dt):
        """
        Increment score by 1 per 0.1 second survived.
        """
        self.score_timer += dt
        # award a point for each 100 ms
        while self.score_timer >= 100:
            self.score += 1
            self.score_timer -= 100

    def _check_collisions(self):
        """
        Check for collisions between the bird and any pipe; mark game over.
        """
        for pipe in self.pipes:
            if self.bird.rect.colliderect(pipe.top_rect) or self.bird.rect.colliderect(pipe.bottom_rect):
                self.game_over = True
                break

    def draw(self):
        """
        Draw background, sprites, and UI.
        """
        self.screen.fill((135, 206, 235))  # sky blue
        # draw pipes behind the bird
        for pipe in self.pipes:
            pipe.draw(self.screen)
        # draw bird and other sprites
        self.all_sprites.draw(self.screen)
        # draw instructions
        instr = self.font.render("Press SPACE to flap, Q to quit", True, (0, 0, 0))
        self.screen.blit(instr, (10, 10))
        # draw score
        score_surf = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_surf, (10, 30))
        # draw game over overlay
        if self.game_over:
            over_surf = self.font.render("Game Over! Press R to restart", True, (255, 0, 0))
            # center the text
            ox = settings.WIDTH // 2 - over_surf.get_width() // 2
            oy = settings.HEIGHT // 2 - over_surf.get_height() // 2
            self.screen.blit(over_surf, (ox, oy))
        pygame.display.flip()