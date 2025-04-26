"""
settings.py: configuration constants for Flappy Bird game.
"""

# Screen settings
WIDTH = 800
HEIGHT = 600
FPS = 60

# Physics constants (per-second units)
GRAVITY = 200.0      # downward acceleration (px/sec^2)
JUMP_VELOCITY = -105.0  # flap impulse velocity (px/sec)
RESTITUTION = 0.8    # bounce damping (1.0 = perfect bounce)

# Bird settings
BIRD_RADIUS = 20

# Asset scaling
SCALE_FACTOR = 8     # images are scaled down by this factor

# Animation settings
FRAME_DURATION = 80  # ms per animation frame

# Pipe settings
PIPE_WIDTH = 50            # width of each pipe (px)
PIPE_GAP = 150             # vertical gap between top and bottom pipes (px)
PIPE_SPEED = 100           # horizontal speed of pipes (px/sec)
PIPE_SPAWN_INTERVAL = 3500 # ms between spawning new pipes
PIPE_MIN_HEIGHT = 50       # minimum height for top/bottom pipe segment (px)