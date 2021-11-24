import os

import pygame
import sys

from data.snake_ai.ai_game import AIGame

if __name__ == '__main__':
    pygame.init()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    game = AIGame()
    game.run_nn(config_path)
    sys.exit()
