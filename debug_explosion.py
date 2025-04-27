"""
debug_explosion.py: Utility to visualize loaded explosion sprite frames.
Run this script to load and display all Explosion frames side-by-side,
then press any key or close the window to exit.
"""
import pygame
import math
import sys

from game import Explosion

def main():
    # Initialize pygame and set a temporary video mode for image conversion
    pygame.init()
    pygame.display.set_mode((1, 1))
    # Trigger frame loading by instantiating a dummy Explosion
    _ = Explosion(0, 0)
    frames = Explosion.frames
    if not frames:
        print("No explosion frames loaded.")
        pygame.quit()
        return

    # Determine grid layout (approx. square)
    num_frames = len(frames)
    cols = int(math.ceil(math.sqrt(num_frames)))
    rows = int(math.ceil(num_frames / cols))

    # Frame dimensions
    frame_w, frame_h = frames[0].get_size()
    # Window size to show grid
    width = cols * frame_w
    height = rows * frame_h
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Explosion Frames Debug")

    # Fill background
    screen.fill((30, 30, 30))
    # Blit each frame
    for idx, img in enumerate(frames):
        x = (idx % cols) * frame_w
        y = (idx // cols) * frame_h
        screen.blit(img, (x, y))
        print(f"Frame {idx}: size={img.get_size()}")

    pygame.display.flip()
    print("Displayed explosion frames. Press any key or close window to exit.")

    # Wait for user input to close
    running = True
    while running:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                running = False
    pygame.quit()

if __name__ == '__main__':
    main()
    sys.exit()