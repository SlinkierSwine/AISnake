# Game
HEIGHT = 600
WIDTH = 600
SIZE = WIDTH, HEIGHT
GAME_NAME = 'AISnake'
BACKGROUND_COLOR = 0, 0, 0
CELL_SIZE = 30
SCORE_COLOR = 250, 250, 250
SCORE_FONT = 'consolas'
SCORE_FONT_SIZE = 20

# Player
PLAYER_COLOR = 250, 250, 250
PLAYER_SIZE = CELL_SIZE, CELL_SIZE
PLAYER_START_POS = WIDTH // 2 - CELL_SIZE, HEIGHT // 2 - CELL_SIZE
PLAYER_SPEED = CELL_SIZE

# Food
FOOD_COLOR = 0, 250, 0
FOOD_SIZE = CELL_SIZE, CELL_SIZE


class Dirs:
    # Directions
    RIGHT = 1
    LEFT = -1
    UP = 2
    DOWN = -2