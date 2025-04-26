import sys
import random

import pygame

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
        self.debug = False          # debug mode: draw collider
        self.start_new_game()

    def start_new_game(self):
        """
        Initialize or reset game state: bird, pipes, score, timers.
        """
        # Bird and sprites
        self.bird = Bird(100, settings.HEIGHT // 2)
        self.all_sprites = pygame.sprite.Group(self.bird)
        # Pipes
        self.pipes = pygame.sprite.Group()
        self.pipe_timer = 0
        # dynamic pipe speed and spawn interval (horizontal gap fixed)
        self.pipe_speed = settings.PIPE_SPEED
        # initial time interval so pipes start at consistent horizontal spacing
        self.pipe_interval = settings.PIPE_SPAWN_INTERVAL * (settings.PIPE_SPEED / self.pipe_speed)
        # Score
        self.score = 0
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
                elif event.key == pygame.K_d:
                    # toggle debug collider display
                    self.debug = not self.debug
                elif self.game_over and event.key == pygame.K_r:
                    # restart after game over
                    self.start_new_game()
                elif not self.game_over and event.key == pygame.K_SPACE:
                    # flap when playing
                    self.bird.flap()
    
    def _spawn_pipe(self):
        """
        Create a new Pipe at the right edge and add it to the list.
        """
        # randomize vertical gap by ± variance
        gap = int(
            settings.PIPE_GAP *
            (1.0 + random.uniform(-settings.PIPE_VARIANCE, settings.PIPE_VARIANCE))
        )
        pipe = Pipe(settings.WIDTH, speed=self.pipe_speed, gap=gap)
        self.pipes.add(pipe)

    def _update_pipes(self, dt):
        """
        Update existing pipes, spawn new ones, and remove off-screen pipes.
        """
        # handle pipe spawning, movement, scoring, and culling
        self._spawn_timer_tick(dt)
        self._move_and_score_pipes(dt)
    
    
    def _spawn_timer_tick(self, dt):
        """Advance the pipe spawn timer and spawn pipes at variable intervals."""
        self.pipe_timer += dt
        if self.pipe_timer >= self.pipe_interval:
            self.pipe_timer -= self.pipe_interval
            self._spawn_pipe()
            # compute base interval so horizontal gap remains constant
            base_interval = settings.PIPE_SPAWN_INTERVAL * (settings.PIPE_SPEED / self.pipe_speed)
            # pick next interval with ± variance
            factor = 1.0 + random.uniform(-settings.PIPE_VARIANCE, settings.PIPE_VARIANCE)
            self.pipe_interval = base_interval * factor

    def _move_and_score_pipes(self, dt):
        """Move pipes, award score for passed pipes, and remove off-screen pipes."""
        self.pipes.update(dt)
        for pipe in list(self.pipes):
            # scoring: bird passes pipe
            if not pipe.passed and pipe.rect.right < self.bird.pos.x:
                pipe.passed = True
                self.score += 100 if pipe.bounced else 10
                self.pipe_speed += 5
                for p in self.pipes:
                    p.speed = self.pipe_speed
            if pipe.off_screen():
                self.pipes.remove(pipe)

    def _circle_rect_collision(self, cx, cy, radius, rect):
        """
        Return True if circle (cx, cy, radius) intersects the given rectangle.
        """
        # Find closest point on rect to circle center
        closest_x = max(rect.left, min(cx, rect.right))
        closest_y = max(rect.top,  min(cy, rect.bottom))
        # Compute distance to closest point
        dx = cx - closest_x
        dy = cy - closest_y
        return (dx*dx + dy*dy) <= (radius * radius)

    def _check_collisions(self):
        """Check for bird collisions with ground and pipes."""
        self._handle_ground_collision()
        if not self.game_over:
            self._handle_pipe_collisions()

    def _handle_ground_collision(self):
        """Mark game over if bird hits the ground."""
        if self.bird.rect.bottom >= settings.HEIGHT:
            self.game_over = True

    def _handle_pipe_collisions(self):
        """Check circle-rect collisions between bird and each pipe segment."""
        cx, cy = self.bird.pos.x, self.bird.pos.y
        radius = self.bird.image.get_height() / 2
        for pipe in self.pipes:
            # top pipe: always fatal
            if self._circle_rect_collision(cx, cy, radius, pipe.top_rect):
                self.game_over = True
                return
            # bottom pipe: may bounce off top edge
            if self._circle_rect_collision(cx, cy, radius, pipe.bottom_rect):
                cy_clamped = max(pipe.bottom_rect.top, min(cy, pipe.bottom_rect.bottom))
                if pipe.bounce_zone and cy_clamped == pipe.bottom_rect.top and self.bird.velocity > 0:
                    pipe.bounced = True
                    self.bird.velocity = -self.bird.velocity * settings.RESTITUTION
                    self.bird.pos.y = pipe.bottom_rect.top - radius
                    self.bird.rect = self.bird.image.get_rect(center=(int(self.bird.pos.x), int(self.bird.pos.y)))
                    continue
                self.game_over = True
                return

    def draw(self):
        """
        Draw background, sprites, and UI.
        """
        self.screen.fill((135, 206, 235))  # sky blue
        # draw pipes behind the bird
        self.pipes.draw(self.screen)
        # draw bird and other sprites
        self.all_sprites.draw(self.screen)
        # draw instructions and score in white on one line
        text_color = (255, 255, 255)
        info = f"Press SPACE to flap, Q to quit   Score: {self.score}"
        # debug: show pipe speed
        if self.debug:
            info += f"   Speed: {int(self.pipe_speed)}"
        info_surf = self.font.render(info, True, text_color)
        self.screen.blit(info_surf, (10, 10))
        # draw game over overlay in white
        if self.game_over:
            over_text = "Game Over! Press R to restart"
            over_surf = self.font.render(over_text, True, text_color)
            # center the text
            ox = settings.WIDTH // 2 - over_surf.get_width() // 2
            oy = settings.HEIGHT // 2 - over_surf.get_height() // 2
            self.screen.blit(over_surf, (ox, oy))
        # debug: draw collision circle
        if self.debug:
            # circle centered on bird with radius = half sprite height
            radius = int(self.bird.image.get_height() / 2)
            center = (int(self.bird.pos.x), int(self.bird.pos.y))
            pygame.draw.circle(self.screen, (255, 0, 0), center, radius, 1)
        pygame.display.flip()