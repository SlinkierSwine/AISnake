import pygame as pg

from data.settings import PLAYER_SPEED, PLAYER_COLOR, Dirs, WIDTH, HEIGHT


class Entity:
    def __init__(self, x, y, w, h, color):
        self.rect = pg.Rect(x, y, w, h)
        self.color = color

    def draw(self, screen):
        pg.draw.rect(screen, color=self.color, rect=self.rect)


class Snake:
    def __init__(self, x, y, w, h):
        self.color = PLAYER_COLOR
        self.head = Entity(x - w, y, w, h, self.color)
        self.body = [
            self.head,
            Entity(x - 2 * w, y, w, h, self.color),
            Entity(x - 3 * w, y, w, h, self.color)
        ]
        self.dir = Dirs.RIGHT
        self.speed = PLAYER_SPEED

    def get_new_head(self):
        return Entity(
            self.head.rect.x,
            self.head.rect.y,
            self.head.rect.w,
            self.head.rect.h,
            self.head.color
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
