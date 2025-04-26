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
        self.pipes = []
        self.pipe_timer = 0
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
        # update pipes and handle off-screen removal
        for pipe in list(self.pipes):
            pipe.update(dt)
            # scoring: when bird passes beyond pipe's right edge
            if not pipe.passed and (pipe.x + pipe.width) < self.bird.pos.x:
                pipe.passed = True
                # award 100 points if a bounce occurred on this pipe, else 10
                self.score += 100 if getattr(pipe, 'bounced', False) else 10
            # remove off-screen pipes
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
        """
        Check for collisions between the bird and any pipe; mark game over.
        """
        # 1) ground collision: end game if bird hits bottom of screen
        if self.bird.rect.bottom >= settings.HEIGHT:
            self.game_over = True
            return
        # 2) circle-rectangle collision tests
        cx, cy = self.bird.pos.x, self.bird.pos.y
        radius = self.bird.image.get_height() / 2
        for pipe in self.pipes:
            # top pipe: collision always fatal (no bounce)
            tr = pipe.top_rect
            if self._circle_rect_collision(cx, cy, radius, tr):
                self.game_over = True
                break
            # bottom pipe: allow bounce on top edge when bird is falling, else fatal
            br = pipe.bottom_rect
            if self._circle_rect_collision(cx, cy, radius, br):
                # determine collision edge (clamp cy to rect)
                cy_clamped = max(br.top, min(cy, br.bottom))
                # bounce only on top edge when descending
                if cy_clamped == br.top and self.bird.velocity > 0:
                    # mark bounce for scoring
                    pipe.bounced = True
                    # invert and dampen velocity
                    self.bird.velocity = -self.bird.velocity * settings.RESTITUTION
                    # reposition bird just above the bottom pipe segment
                    self.bird.pos.y = br.top - radius
                    self.bird.rect = self.bird.image.get_rect(center=(int(self.bird.pos.x), int(self.bird.pos.y)))
                    # skip further collision checks for this frame
                    continue
                # any other collision on bottom pipe is fatal
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
        # draw instructions and score in white on one line
        text_color = (255, 255, 255)
        info = f"Press SPACE to flap, Q to quit   Score: {self.score}"
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