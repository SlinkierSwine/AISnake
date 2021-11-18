import pickle
from random import randrange

import neat
import pygame as pg

from data.entities import Food, AISnake
from .game import Game
from .settings import *


class AIGame(Game):
    def __init__(self):
        super().__init__()

        self.player = None
        self.fps = 60

        self.nets = []
        self.snakes = []
        self.ge = []

    def update(self):
        self.screen.fill(self.background)
        self.food.draw(self.screen)
        for snake in self.snakes:
            snake.draw(self.screen)

        self.display_score()

        pg.display.update()
        self.clock.tick(self.fps)

    def setup_nn(self, genome, config, is_winner=False):
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.nets.append(net)
        self.snakes.append(AISnake(
            *PLAYER_START_POS,
            *PLAYER_SIZE))
        if not is_winner:
            self.ge.append(genome)

    def change_fitness(self, index, value, is_winner=False):
        if not is_winner:
            self.ge[index].fitness += value

    def delete_genome(self, snake):
        self.nets.pop(self.snakes.index(snake))
        self.ge.pop(self.snakes.index(snake))
        self.snakes.pop(self.snakes.index(snake))

    def eval_genomes(self, genomes, config, is_winner=False):
        self.running = True

        for genome_id, genome in genomes:
            self.setup_nn(genome, config)

        while self.running:
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    quit()
                    break

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE and not is_winner:
                        for snake in self.snakes:
                            self.change_fitness(self.snakes.index(snake), -1, is_winner)
                            self.delete_genome(snake)

            else:

                if not self.snakes:
                    self.running = False
                    break

                for x, snake in enumerate(self.snakes):

                    if not snake.moves_left:
                        self.change_fitness(self.snakes.index(snake), -15, is_winner)
                        self.delete_genome(snake)
                        continue

                    self.change_fitness(x, +0.1, is_winner)

                    output = self.nets[self.snakes.index(snake)].activate((snake.get_input_values(self.food)))
                    # print(output)
                    snake.change_direction_by_output(output)

                    if snake.move_and_collide():
                        self.change_fitness(self.snakes.index(snake), -10, is_winner)
                        self.delete_genome(snake)

                    elif snake.eat(self.food):
                        food_pos = (randrange(0, WIDTH, FOOD_SIZE[0]), randrange(0, HEIGHT, FOOD_SIZE[0]))
                        self.food = Food(*food_pos, *FOOD_SIZE, FOOD_COLOR_1, FOOD_COLOR_2)
                        self.score += 1
                        self.change_fitness(self.snakes.index(snake), 30, is_winner)
                        snake.moves_left += 100
                    else:
                        self.change_fitness(x, -0.01, is_winner)
                        snake.moves_left -= 1

                self.update()

    def run_nn(self, config_file):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_file)

        p = neat.Population(config)

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner = p.run(self.eval_genomes, 50)
        import pickle
        pickle.dump(winner, open("winner.pickle", "wb"))

        print('\nBest genome:\n{!s}'.format(winner))

    def run_winner(self, config_file, winner_path):
        with open(winner_path, 'rb') as f:
            winner = pickle.load(f)

        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_file)
        self.eval_genomes(((0, winner), ), config, is_winner=True)


