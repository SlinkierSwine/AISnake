import pygame as pg
from collections import namedtuple
import numpy as np

from data.settings import PLAYER_SPEED, PLAYER_COLOR_1, Dirs, WIDTH, HEIGHT, PLAYER_COLOR_2, CELL_SIZE

Point = namedtuple('Point', field_names=['x', 'y'])


class Entity:
    def __init__(self, x, y, w, h, color_1, color_2):
        self.rect = pg.Rect(x, y, w, h)
        self.color_1 = color_1
        self.color_2 = color_2

    def draw(self, screen):
        pg.draw.rect(screen, color=self.color_1, rect=self.rect)
        pg.draw.rect(screen, color=self.color_2, rect=self.rect, width=3)


class Snake:
    def __init__(self, x, y, w, h):
        self.color_1 = PLAYER_COLOR_1
        self.color_2 = PLAYER_COLOR_2
        self.head = Entity(x - w, y, w, h, self.color_1, self.color_2)
        self.body = [
            self.head,
            Entity(x - 2 * w, y, w, h, self.color_1, self.color_2),
            Entity(x - 3 * w, y, w, h, self.color_1, self.color_2),
            Entity(x - 4 * w, y, w, h, self.color_1, self.color_2)
        ]
        self.dir = Dirs.RIGHT
        self.speed = PLAYER_SPEED

    def get_new_head(self):
        return Entity(
            self.head.rect.x,
            self.head.rect.y,
            self.head.rect.w,
            self.head.rect.h,
            self.head.color_1,
            self.head.color_2
        )

    def collide(self):
        if self.head.rect.x < 0 or self.head.rect.x > WIDTH - CELL_SIZE\
                or self.head.rect.y < 0 or self.head.rect.y > HEIGHT - CELL_SIZE:
            return True

        for part in self.body[1:]:
            if self.head.rect.x == part.rect.x and self.head.rect.y == part.rect.y:
                return True

        return False

    def eat(self, food):
        if self.head.rect.x != food.rect.x or self.head.rect.y != food.rect.y:
            self.body.pop()
            return False
        return True

    def move_and_collide(self):
        new_head = self.get_new_head()

        if self.dir == Dirs.RIGHT:
            new_head.rect.x += self.speed
        elif self.dir == Dirs.UP:
            new_head.rect.y -= self.speed
        elif self.dir == Dirs.LEFT:
            new_head.rect.x -= self.speed
        elif self.dir == Dirs.DOWN:
            new_head.rect.y += self.speed

        self.head = new_head
        self.body.insert(0, self.head)
        return self.collide()

    def change_direction(self, direction):
        if abs(self.dir) != abs(direction):
            self.dir = direction

    def draw(self, screen):
        for part in self.body:
            part.draw(screen)


class Food(Entity):
    pass


class AISnake(Snake):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.moves_left = 100

    def collide_with_point(self, point):
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
            (dir_r and self.collide_with_point(point_r)) or
            (dir_l and self.collide_with_point(point_l)) or
            (dir_u and self.collide_with_point(point_u)) or
            (dir_d and self.collide_with_point(point_d)),

            # Danger right
            (dir_u and self.collide_with_point(point_r)) or
            (dir_d and self.collide_with_point(point_l)) or
            (dir_l and self.collide_with_point(point_u)) or
            (dir_r and self.collide_with_point(point_d)),

            # Danger left
            (dir_d and self.collide_with_point(point_r)) or
            (dir_u and self.collide_with_point(point_l)) or
            (dir_r and self.collide_with_point(point_u)) or
            (dir_l and self.collide_with_point(point_d)),

            dir_l,
            dir_r,
            dir_u,
            dir_d,

            food.rect.x < self.head.rect.x,  # food left
            food.rect.x > self.head.rect.x,  # food right
            food.rect.y < self.head.rect.y,  # food up
            food.rect.y > self.head.rect.y  # food down
        ]
        return np.array(values, dtype=int)

    def change_direction_by_output(self, output):
        if output[0] > 0.8 and output[1] < output[0]:
            if self.dir == Dirs.RIGHT:
                self.change_direction(Dirs.UP)
            elif self.dir == Dirs.UP:
                self.change_direction(Dirs.LEFT)
            elif self.dir == Dirs.LEFT:
                self.change_direction(Dirs.DOWN)
            elif self.dir == Dirs.DOWN:
                self.change_direction(Dirs.RIGHT)

        elif output[2] > 0.8 and output[1] < output[2]:
            if self.dir == Dirs.RIGHT:
                self.change_direction(Dirs.DOWN)
            elif self.dir == Dirs.DOWN:
                self.change_direction(Dirs.LEFT)
            elif self.dir == Dirs.LEFT:
                self.change_direction(Dirs.UP)
            elif self.dir == Dirs.UP:
                self.change_direction(Dirs.RIGHT)
