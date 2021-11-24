from collections import namedtuple

import numpy as np
import pygame as pg

from data.snake_game.entities import Snake
from data.settings import *


Point = namedtuple('Point', field_names=['x', 'y'])


class AISnake(Snake):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.moves_left = 100

    def _collide_with_point(self, point):
        if point.x < 0 or point.x > WIDTH - CELL_SIZE\
                or point.y < 0 or point.y > HEIGHT - CELL_SIZE:
            return True

        for part in self.body[1:]:
            if point.x == part.rect.x and point.y == part.rect.y:
                return True

        return False

    def get_input_values(self, food):
        dir_r = self.dir == Dirs.RIGHT
        dir_l = self.dir == Dirs.LEFT
        dir_u = self.dir == Dirs.UP
        dir_d = self.dir == Dirs.DOWN

        point_r = Point(self.head.rect.x + self.head.rect.w, self.head.rect.y)
        point_l = Point(self.head.rect.x - self.head.rect.w, self.head.rect.y)
        point_u = Point(self.head.rect.x, self.head.rect.y - self.head.rect.h)
        point_d = Point(self.head.rect.x, self.head.rect.y + self.head.rect.h)

        values = [
            # Опасность спереди
            (dir_r and self._collide_with_point(point_r)) or
            (dir_l and self._collide_with_point(point_l)) or
            (dir_u and self._collide_with_point(point_u)) or
            (dir_d and self._collide_with_point(point_d)),

            # Опасность справа
            (dir_u and self._collide_with_point(point_r)) or
            (dir_d and self._collide_with_point(point_l)) or
            (dir_l and self._collide_with_point(point_u)) or
            (dir_r and self._collide_with_point(point_d)),

            # Опасность слева
            (dir_d and self._collide_with_point(point_r)) or
            (dir_u and self._collide_with_point(point_l)) or
            (dir_r and self._collide_with_point(point_u)) or
            (dir_l and self._collide_with_point(point_d)),

            dir_l,
            dir_r,
            dir_u,
            dir_d,

            food.rect.x < self.head.rect.x,  # еда слева
            food.rect.x > self.head.rect.x,  # еда справа
            food.rect.y < self.head.rect.y,  # еда сверху
            food.rect.y > self.head.rect.y  # еда снизу
        ]
        return np.array(values, dtype=int)

    def change_direction_by_output(self, output):
        # if output[0] > 0.8 and output[1] < output[0]:
        if max(output) == output[0] and output[0] != output[2]:
            if self.dir == Dirs.RIGHT:
                self.change_direction(Dirs.UP)
            elif self.dir == Dirs.UP:
                self.change_direction(Dirs.LEFT)
            elif self.dir == Dirs.LEFT:
                self.change_direction(Dirs.DOWN)
            elif self.dir == Dirs.DOWN:
                self.change_direction(Dirs.RIGHT)

        # elif output[2] > 0.8 and output[1] < output[2]:
        elif max(output) == output[2] and output[0] != output[2]:
            if self.dir == Dirs.RIGHT:
                self.change_direction(Dirs.DOWN)
            elif self.dir == Dirs.DOWN:
                self.change_direction(Dirs.LEFT)
            elif self.dir == Dirs.LEFT:
                self.change_direction(Dirs.UP)
            elif self.dir == Dirs.UP:
                self.change_direction(Dirs.RIGHT)

    def draw(self, screen):
        super().draw(screen)
        score_font = pg.font.SysFont(SCORE_FONT, SCORE_FONT_SIZE_SMALL)
        score_color = pg.Color(SCORE_SMALL_COLOR)
        score_surface = score_font.render(str(self.score), True, score_color)
        score_rect = score_surface.get_rect()
        score_rect.x = self.head.rect.centerx
        score_rect.y = self.head.rect.y
        screen.blit(score_surface, score_rect)
