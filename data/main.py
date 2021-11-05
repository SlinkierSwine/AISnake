from random import randrange

import pygame as pg
from pygame import Color

from data.entities import Snake, Food
from .settings import *


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode(SIZE)

        self.background = Color(BACKGROUND_COLOR)
        self.player_color = Color(PLAYER_COLOR)
        self.score_color = Color(SCORE_COLOR)

        self.running = False
        self.clock = pg.time.Clock()
        self.fps = 10
        self.player = Snake(
            *PLAYER_START_POS,
            *PLAYER_SIZE,
        )
        food_pos = (randrange(0, WIDTH, FOOD_SIZE[0]), randrange(0, HEIGHT, FOOD_SIZE[0]))
        self.food = Food(*food_pos, *FOOD_SIZE, FOOD_COLOR)
        self.score = 0

        pg.display.set_caption(GAME_NAME)

    def display_score(self):
        score_font = pg.font.SysFont(SCORE_FONT, SCORE_FONT_SIZE)
        score_surface = score_font.render('Score : ' + str(self.score), True, self.score_color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (WIDTH / 10, 15)
        self.screen.blit(score_surface, score_rect)

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
                    if event.key in [pg.K_a, pg.K_LEFT]:
                        self.player.change_direction(Dirs.LEFT)
                    if event.key in [pg.K_s, pg.K_DOWN]:
                        self.player.change_direction(Dirs.DOWN)
                    if event.key in [pg.K_d, pg.K_RIGHT]:
                        self.player.change_direction(Dirs.RIGHT)
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                        break
            else:
                self.screen.fill(self.background)
                self.food.draw(self.screen)
                self.player.draw(self.screen)

                if self.player.move_and_collide():
                    self.running = False
                    break
                if self.player.eat(self.food):
                    food_pos = (randrange(0, WIDTH, FOOD_SIZE[0]), randrange(0, HEIGHT, FOOD_SIZE[0]))
                    self.food = Food(*food_pos, *FOOD_SIZE, FOOD_COLOR)
                    self.score += 1

                self.display_score()

                pg.display.update()
                self.clock.tick(self.fps)
