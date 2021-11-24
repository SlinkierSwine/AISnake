from random import randrange

import pygame as pg
from pygame import Color

from data.snake_game.entities import Snake, Food
from data.settings import *


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode(SIZE)

        self.background = Color(BACKGROUND_COLOR)
        self.player_color_1 = Color(PLAYER_COLOR_1)
        self.player_color_2 = Color(PLAYER_COLOR_2)
        self.score_color = Color(SCORE_COLOR)

        self.running = False
        self.clock = pg.time.Clock()
        self.fps = FPS
        self.player = Snake(
            *PLAYER_START_POS,
            *PLAYER_SIZE,
        )

        self._spawn_food()

        pg.display.set_caption(GAME_NAME)

    def _display_score(self, score):
        score_font = pg.font.SysFont(SCORE_FONT, SCORE_FONT_SIZE)
        score_surface = score_font.render('Score : ' + str(score), True, self.score_color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (WIDTH / 8, 15)
        self.screen.blit(score_surface, score_rect)

    def _update(self):
        self.screen.fill(self.background)
        self.food.draw(self.screen)
        self.player.draw(self.screen)

        self._display_score(self.player.score)

        pg.display.update()
        self.clock.tick(self.fps)

    def _spawn_food(self):
        food_pos = (randrange(0, WIDTH, FOOD_SIZE[0]), randrange(0, HEIGHT, FOOD_SIZE[0]))
        self.food = Food(*food_pos, *FOOD_SIZE)

    def run(self):
        self.running = True

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    break

                elif event.type == pg.KEYDOWN:

                    if event.key in [pg.K_w, pg.K_UP]:
                        self.player.change_direction(Dirs.UP)
                    elif event.key in [pg.K_s, pg.K_DOWN]:
                        self.player.change_direction(Dirs.DOWN)
                    elif event.key in [pg.K_a, pg.K_LEFT]:
                        self.player.change_direction(Dirs.LEFT)

                    elif event.key in [pg.K_d, pg.K_RIGHT]:
                        self.player.change_direction(Dirs.RIGHT)

                    if event.key == pg.K_ESCAPE:
                        self.running = False
                        break
            else:

                if self.player.move_and_collide():
                    self.running = False
                    break

                if self.player.eat(self.food):
                    self._spawn_food()

                self._update()

