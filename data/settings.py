import os

from data.config import read_config


config = read_config(os.path.join('data', 'config.cfg'))


# Game
CELL_SIZE = int(config['GAME']['CELL_SIZE'])
HEIGHT = int(config['GAME']['HEIGHT']) * CELL_SIZE
WIDTH = int(config['GAME']['WIDTH']) * CELL_SIZE
SIZE = WIDTH, HEIGHT
GAME_NAME = 'AISnake'
FPS = int(config['GAME']['FPS'])

BACKGROUND_COLOR = 0, 0, 0
SCORE_COLOR = 250, 250, 250
SCORE_SMALL_COLOR = 250, 0, 0
SCORE_FONT = 'consolas'
SCORE_FONT_SIZE = 20
SCORE_FONT_SIZE_SMALL = 15

# Player
PLAYER_COLOR_1 = 250, 250, 250
PLAYER_COLOR_2 = 150, 150, 150
PLAYER_SIZE = CELL_SIZE, CELL_SIZE
PLAYER_START_POS = WIDTH // 2 - CELL_SIZE, HEIGHT // 2 - CELL_SIZE
PLAYER_SPEED = CELL_SIZE

# Food
FOOD_COLOR_1 = 0, 250, 0
FOOD_COLOR_2 = 0, 150, 0
FOOD_SIZE = CELL_SIZE, CELL_SIZE

# N-n
GENERATIONS = int(config['NN']['GENERATIONS'])


class Dirs:
    # Directions
    RIGHT = 1
    LEFT = -1
    UP = 2
    DOWN = -2
