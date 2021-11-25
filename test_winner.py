import os

import pygame
import sys

from data.snake_ai.ai_game import AIGame

if __name__ == '__main__':
    pygame.init()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    winner_path = os.path.join(local_dir, 'winner.pickle')
    game = AIGame()
    highest_score = game.run_winner(config_path, winner_path)
    print()
    print('Highest score:', highest_score)
    sys.exit()
