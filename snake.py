import pygame
import sys

from data.game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
    sys.exit()
