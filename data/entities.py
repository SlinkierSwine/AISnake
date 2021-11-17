import pygame as pg

from data.settings import PLAYER_SPEED, PLAYER_COLOR_1, Dirs, WIDTH, HEIGHT, PLAYER_COLOR_2


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
            Entity(x - 3 * w, y, w, h, self.color_1, self.color_2)
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
        if self.head.rect.x < 0 or self.head.rect.x > WIDTH\
                or self.head.rect.y < 0 or self.head.rect.y > HEIGHT:
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
