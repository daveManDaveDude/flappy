"""
utils.py: Utility functions for collision detection and randomization.
"""
import random
import settings

def circle_rect_collision(cx: float, cy: float, radius: float, rect) -> bool:
    """
    Return True if a circle at (cx, cy) with given radius intersects the rect.
    """
    closest_x = max(rect.left, min(cx, rect.right))
    closest_y = max(rect.top,  min(cy, rect.bottom))
    dx = cx - closest_x
    dy = cy - closest_y
    return (dx*dx + dy*dy) <= (radius * radius)

def random_gap(base_gap: int = None) -> int:
    """
    Return a randomized gap size around PIPE_GAP within PIPE_VARIANCE.
    """
    gap = base_gap if base_gap is not None else settings.PIPE_GAP
    variance = settings.PIPE_VARIANCE
    factor = 1.0 + random.uniform(-variance, variance)
    return int(gap * factor)

def random_spawn_interval(pipe_speed: float) -> int:
    """
    Return a randomized pipe spawn interval (ms) adjusted for speed and variance.
    """
    base = settings.PIPE_SPAWN_INTERVAL * (settings.PIPE_SPEED / pipe_speed)
    factor = 1.0 + random.uniform(-settings.PIPE_VARIANCE, settings.PIPE_VARIANCE)
    return int(base * factor)