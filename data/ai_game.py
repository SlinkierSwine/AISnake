from random import randrange

import neat
import pygame as pg
from pygame import Color

from data.entities import Snake, Food
from .settings import *


class AIGame:
    def __init__(self):
        self.screen = pg.display.set_mode(SIZE)

        self.background = Color(BACKGROUND_COLOR)
        self.player_color_1 = Color(PLAYER_COLOR_1)
        self.player_color_2 = Color(PLAYER_COLOR_2)
        self.score_color = Color(SCORE_COLOR)

        self.running = False
        self.clock = pg.time.Clock()
        self.fps = 60
        self.nets = []
        self.snakes = []
        self.ge = []

        food_pos = (randrange(0, WIDTH, FOOD_SIZE[0]), randrange(0, HEIGHT, FOOD_SIZE[0]))
        self.food = Food(*food_pos, *FOOD_SIZE, FOOD_COLOR_1, FOOD_COLOR_2)
        self.score = 0

        pg.display.set_caption(GAME_NAME)
        # pg.key.set_repeat(1, 25)

    def display_score(self):
        score_font = pg.font.SysFont(SCORE_FONT, SCORE_FONT_SIZE)
        score_surface = score_font.render('Score : ' + str(self.score), True, self.score_color)
        score_rect = score_surface.get_rect()
        score_rect.midtop = (WIDTH / 10, 15)
        self.screen.blit(score_surface, score_rect)

    def update(self):
        self.screen.fill(self.background)
        self.food.draw(self.screen)
        for snake in self.snakes:
            snake.draw(self.screen)

        self.display_score()

        pg.display.update()
        self.clock.tick(self.fps)

    def eval_genomes(self, genomes, config):
        self.running = True

        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            self.snakes.append(Snake(
                *PLAYER_START_POS,
                *PLAYER_SIZE))
            self.ge.append(genome)

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    quit()
                    break
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        for snake in self.snakes:
                            self.ge[self.snakes.index(snake)].fitness -= 1
                            self.nets.pop(self.snakes.index(snake))
                            self.ge.pop(self.snakes.index(snake))
                            self.snakes.pop(self.snakes.index(snake))
            else:
                if not self.snakes:
                    self.running = False
                    break
                for x, snake in enumerate(self.snakes):
                    self.ge[x].fitness += 0.01

                    output = self.nets[self.snakes.index(snake)].activate(
                        (
                            snake.get_input_values(self.food)
                        )
                    )

                    if output[0] > 0.9:
                        if snake.dir == Dirs.RIGHT:
                            snake.change_direction(Dirs.UP)
                        elif snake.dir == Dirs.UP:
                            snake.change_direction(Dirs.LEFT)
                        elif snake.dir == Dirs.LEFT:
                            snake.change_direction(Dirs.DOWN)
                        elif snake.dir == Dirs.DOWN:
                            snake.change_direction(Dirs.RIGHT)

                    if output[2] > 0.9:
                        if snake.dir == Dirs.RIGHT:
                            snake.change_direction(Dirs.DOWN)
                        elif snake.dir == Dirs.DOWN:
                            snake.change_direction(Dirs.LEFT)
                        elif snake.dir == Dirs.LEFT:
                            snake.change_direction(Dirs.UP)
                        elif snake.dir == Dirs.UP:
                            snake.change_direction(Dirs.RIGHT)

                for snake in self.snakes:
                    if snake.move_and_collide():
                        self.ge[self.snakes.index(snake)].fitness -= 5
                        self.nets.pop(self.snakes.index(snake))
                        self.ge.pop(self.snakes.index(snake))
                        self.snakes.pop(self.snakes.index(snake))

                    elif snake.eat(self.food):
                        food_pos = (randrange(0, WIDTH, FOOD_SIZE[0]), randrange(0, HEIGHT, FOOD_SIZE[0]))
                        self.food = Food(*food_pos, *FOOD_SIZE, FOOD_COLOR_1, FOOD_COLOR_2)
                        self.score += 1
                        self.ge[self.snakes.index(snake)].fitness += 30

                self.update()

    def run(self, config_file):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_file)

        # Create the population, which is the top-level object for a NEAT run.
        p = neat.Population(config)

        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        # p.add_reporter(neat.Checkpointer(5))

        # Run for up to 50 generations.
        winner = p.run(self.eval_genomes, 50)
        import pickle
        pickle.dump(winner, open("winner.pickle", "wb"))

        # show final stats
        print('\nBest genome:\n{!s}'.format(winner))


