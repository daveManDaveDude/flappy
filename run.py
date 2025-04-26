"""
run.py: entry point for the Flappy Bird game.
"""
import sys
from game import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
    sys.exit()