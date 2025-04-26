"""
input_handler.py: Process Pygame events into game actions.
"""
import pygame
from pygame.locals import QUIT, KEYDOWN, K_q, K_d, K_r, K_SPACE

class InputHandler:
    """
    Translates raw Pygame events into high-level game actions.
    """
    def process(self, events):
        """
        Given a list of Pygame events, return a dict of actions:
        - quit: True if the game should exit
        - toggle_debug: True if debug mode toggled
        - restart: True if game restart requested
        - flap: True if bird flap requested
        """
        actions = {
            'quit': False,
            'toggle_debug': False,
            'restart': False,
            'flap': False,
        }
        for event in events:
            if event.type == QUIT:
                actions['quit'] = True
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    actions['quit'] = True
                elif event.key == K_d:
                    actions['toggle_debug'] = True
                elif event.key == K_r:
                    actions['restart'] = True
                elif event.key == K_SPACE:
                    actions['flap'] = True
        return actions