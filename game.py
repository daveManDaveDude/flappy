import sys
from enum import Enum

import pygame

import settings
import random
from utils import circle_rect_collision, random_gap, random_spawn_interval
from input_handler import InputHandler
from renderer import Renderer
import assets

# Explosion animation sprite
class Explosion(pygame.sprite.Sprite):
    """Explosion animation sprite spawned on bird collision."""
    frames = []
    def __init__(self, x, y):
        super().__init__()
        if not Explosion.frames:
            sheet = assets.load_image('explosion_sheet.png')
            sheet_w, sheet_h = sheet.get_size()
            # sprite sheet layout: 4 columns, 4 rows of frames
            cols, rows = 4, 4
            frame_w, frame_h = sheet_w // cols, sheet_h // rows
            # scale explosion frames by a larger factor for visibility
            EXPLOSION_SCALE = 4
            # target dimensions after scaling
            target_w = (frame_w // settings.SCALE_FACTOR) * EXPLOSION_SCALE
            target_h = (frame_h // settings.SCALE_FACTOR) * EXPLOSION_SCALE
            for row in range(rows):
                for col in range(cols):
                    rect = pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)
                    image = sheet.subsurface(rect).copy()
                    image = pygame.transform.smoothscale(image, (target_w, target_h))
                    Explosion.frames.append(image)
        self.image = Explosion.frames[0]
        self.rect = self.image.get_rect(center=(int(x), int(y)))
        self.frame_index = 0
        self.timer = 0
        # ms per animation frame
        self.frame_duration = settings.FRAME_DURATION

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            self.frame_index += 1
            if self.frame_index >= len(Explosion.frames):
                self.kill()
            else:
                self.image = Explosion.frames[self.frame_index]
                self.rect = self.image.get_rect(center=self.rect.center)

# custom event for spawning pipes
SPAWN_PIPE = pygame.USEREVENT + 1

class GameState(Enum):
    PLAYING = 1
    EXPLODING = 2
    GAME_OVER = 3

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
# Utility functions and handlers
from utils import circle_rect_collision, random_gap, random_spawn_interval
from input_handler import InputHandler
from renderer import Renderer


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
        self.debug = False  # debug mode: draw collider
        self.collision = True  # collision detection enabled
        # input and rendering handlers
        self.input_handler = InputHandler()
        self.renderer = Renderer(self.screen, self.font)
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
        # reset previous gap center history
        self.last_gap_center = None
        # dynamic pipe speed
        self.pipe_speed = settings.PIPE_SPEED
        # reset score and game state
        self.score = 0
        self.state = GameState.PLAYING
        # spawn initial pipe (closer to the bird) and start spawn timer
        initial_x = self.bird.pos.x + settings.INITIAL_PIPE_OFFSET
        self._spawn_pipe(initial_x)
        self._schedule_next_pipe()

    def run(self):
        """
        Main loop: process input, update state, draw, repeat until exit.
        """
        while self.running:
            dt = self.clock.tick(settings.FPS)
            self.handle_events()
            # always update sprite animations (e.g., explosions)
            self.all_sprites.update(dt)
            # update game physics and logic only while playing
            if self.state == GameState.PLAYING:
                # move pipes, spawn as scheduled
                self._update_pipes(dt)
                # handle any collisions
                self._check_collisions()
            # transition to game over after explosion animation
            if self.state == GameState.EXPLODING:
                # if no explosion sprites remain, finalize game over and show burnt bird sprite
                if not any(isinstance(s, Explosion) for s in self.all_sprites):
                    # stop any wing animation
                    self.bird.animating = False
                    # use burnt bird image
                    try:
                        self.bird.image = self.bird.burnt_image
                    except AttributeError:
                        # fallback to base image if burnt sprite unavailable
                        self.bird.image = self.bird.base_image
                    # freeze bird in place
                    self.bird.frozen = True
                    # reposition sprite at last collision position
                    self.bird.rect = self.bird.image.get_rect(
                        center=(int(self.bird.pos.x), int(self.bird.pos.y))
                    )
                    # add bird back to sprites for rendering
                    self.all_sprites.add(self.bird)
                    self.state = GameState.GAME_OVER
            # always render frame
            self.renderer.render(self)
        pygame.quit()

    def handle_events(self):
        """
        Handle all pending pygame events: spawn pipes and process input actions.
        """
        events = pygame.event.get()
        # spawn pipes via custom event
        for event in events:
            if event.type == SPAWN_PIPE and self.state == GameState.PLAYING:
                self._spawn_pipe()
                self._schedule_next_pipe()
        # process user input
        actions = self.input_handler.process(events)
        if actions['quit']:
            self.running = False
        if actions['toggle_debug']:
            # cycle through debug -> disable collisions -> back to normal
            if not self.debug:
                self.debug = True
                self.collision = True
            elif self.debug and self.collision:
                self.collision = False
            else:
                self.debug = False
                self.collision = True
        if actions['restart'] and self.state == GameState.GAME_OVER:
            self.start_new_game()
        if actions['flap'] and self.state == GameState.PLAYING:
            self.bird.flap()
    
    def _spawn_pipe(self, x=None):
        """
        Create a new Pipe at the right edge and add it to the list.
        """
        # determine horizontal spawn position
        if x is None:
            x = settings.WIDTH
        # randomized vertical gap with constrained vertical shift between pipes
        gap = random_gap()
        half_gap = gap / 2.0
        # determine allowable center of gap
        if hasattr(self, 'last_gap_center') and self.last_gap_center is not None:
            prev = self.last_gap_center
            # base allowable center range
            min_c = settings.PIPE_MIN_HEIGHT + half_gap
            max_c = settings.HEIGHT - settings.PIPE_MIN_HEIGHT - half_gap
            # allow larger downward shift (bird diving) than upward (climbing)
            up_shift = settings.MAX_GAP_SHIFT
            down_shift = settings.MAX_GAP_SHIFT_DOWN
            min_c = max(min_c, prev - down_shift)
            max_c = min(max_c, prev + up_shift)
            if min_c > max_c:
                # fallback to full range if constraints invalid
                min_c = settings.PIPE_MIN_HEIGHT + half_gap
                max_c = settings.HEIGHT - settings.PIPE_MIN_HEIGHT - half_gap
        else:
            # first pipe: full vertical range
            min_c = settings.PIPE_MIN_HEIGHT + half_gap
            max_c = settings.HEIGHT - settings.PIPE_MIN_HEIGHT - half_gap
        # choose center position and compute top height
        gap_center = random.uniform(min_c, max_c)
        top_h = int(gap_center - half_gap)
        pipe = Pipe(x, speed=self.pipe_speed, gap=gap, top_height=top_h)
        self.pipes.add(pipe)
        # remember center for next constraint
        self.last_gap_center = gap_center

    def _schedule_next_pipe(self):
        """Schedule the next pipe spawn via a Pygame timer event."""
        interval = random_spawn_interval(self.pipe_speed)
        pygame.time.set_timer(SPAWN_PIPE, interval)

    def _update_pipes(self, dt):
        """
        Update existing pipes, spawn new ones, and remove off-screen pipes.
        """
        # move, score, and cull pipes
        self._move_and_score_pipes(dt)
    
    

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


    def _check_collisions(self):
        """Check for bird collisions with ground and pipes."""
        if not self.collision:
            return
        self._handle_ground_collision()
        if self.state == GameState.PLAYING:
            self._handle_pipe_collisions()

    def _handle_ground_collision(self):
        """Mark game over if bird hits the ground."""
        if self.bird.rect.bottom >= settings.HEIGHT:
            # spawn explosion at bird position and remove bird
            explosion = Explosion(self.bird.rect.centerx, self.bird.rect.centery)
            self.all_sprites.add(explosion)
            self.all_sprites.remove(self.bird)
            self.state = GameState.EXPLODING

    def _handle_pipe_collisions(self):
        """Check circle-rect collisions between bird and each pipe segment."""
        cx, cy = self.bird.pos.x, self.bird.pos.y
        radius = self.bird.image.get_height() / 2
        for pipe in self.pipes:
            # top pipe: always fatal
            if circle_rect_collision(cx, cy, radius, pipe.top_rect):
                # bird hit top pipe: spawn explosion and remove bird
                explosion = Explosion(cx, cy)
                self.all_sprites.add(explosion)
                self.all_sprites.remove(self.bird)
                self.state = GameState.EXPLODING
                return
            # bottom pipe: may bounce off top edge
            if circle_rect_collision(cx, cy, radius, pipe.bottom_rect):
                cy_clamped = max(pipe.bottom_rect.top, min(cy, pipe.bottom_rect.bottom))
                if pipe.bounce_zone and cy_clamped == pipe.bottom_rect.top and self.bird.velocity > 0:
                    pipe.bounced = True
                    self.bird.velocity = -self.bird.velocity * settings.RESTITUTION
                    self.bird.pos.y = pipe.bottom_rect.top - radius
                    self.bird.rect = self.bird.image.get_rect(center=(int(self.bird.pos.x), int(self.bird.pos.y)))
                    continue
                # fatal collision with bottom pipe: spawn explosion and remove bird
                explosion = Explosion(cx, cy)
                self.all_sprites.add(explosion)
                self.all_sprites.remove(self.bird)
                self.state = GameState.EXPLODING
                return

    def draw(self):
        """
        Draw background, sprites, and UI.
        """
        self.screen.fill(settings.BACKGROUND_COLOR)
        # draw pipes behind the bird
        self.pipes.draw(self.screen)
        # draw bird and other sprites
        self.all_sprites.draw(self.screen)
        # draw instructions and score in white on one line
        text_color = settings.TEXT_COLOR
        info = f"Press SPACE to flap, Q to quit   Score: {self.score}"
        # indicate collision detection disabled
        if not self.collision:
            info += "*"
        # debug: show pipe speed
        if self.debug:
            info += f"   Speed: {int(self.pipe_speed)}"
        info_surf = self.font.render(info, True, text_color)
        self.screen.blit(info_surf, (10, 10))
        # draw game over overlay in white
        if self.state == GameState.GAME_OVER:
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
            pygame.draw.circle(self.screen, settings.DEBUG_CIRCLE_COLOR, center, radius, 1)
        pygame.display.flip()