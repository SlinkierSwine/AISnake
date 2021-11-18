import pygame
import sys

from data.game import Game

if __name__ == '__main__':
    pygame.init()
    pygame.key.set_repeat(1, 25)
    game = Game()
    game.run()
    sys.exit()
