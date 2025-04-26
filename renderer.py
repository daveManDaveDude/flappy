"""
renderer.py: Responsible for drawing game state to the screen.
"""
import settings
import pygame

class Renderer:
    """
    Encapsulates all rendering logic for the game.
    """
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def render(self, game):
        """
        Draw background, pipes, bird, UI, and debug overlays.
        """
        # Clear screen
        self.screen.fill(settings.BACKGROUND_COLOR)
        # Draw pipes behind the bird
        game.pipes.draw(self.screen)
        # Draw bird and other sprites
        game.all_sprites.draw(self.screen)
        # Draw UI: instructions and score
        text_color = settings.TEXT_COLOR
        info = f"Press SPACE to flap, Q to quit   Score: {game.score}"
        if game.debug:
            info += f"   Speed: {int(game.pipe_speed)}"
        info_surf = self.font.render(info, True, text_color)
        self.screen.blit(info_surf, (10, 10))
        # Game over message
        if game.state.name == 'GAME_OVER':
            over_text = "Game Over! Press R to restart"
            over_surf = self.font.render(over_text, True, text_color)
            ox = settings.WIDTH // 2 - over_surf.get_width() // 2
            oy = settings.HEIGHT // 2 - over_surf.get_height() // 2
            self.screen.blit(over_surf, (ox, oy))
        # Debug: draw collision circle
        if game.debug:
            radius = int(game.bird.image.get_height() / 2)
            center = (int(game.bird.pos.x), int(game.bird.pos.y))
            pygame.draw.circle(self.screen, settings.DEBUG_CIRCLE_COLOR, center, radius, 1)
        # Flip buffers
        pygame.display.flip()