import os
import pickle

import neat
import pygame as pg

import visualize
from data.snake_ai.ai_entities import AISnake
from data.snake_game.game import Game
from data.settings import *


class AIGame(Game):
    def __init__(self, no_window=False):
        if not no_window:
            super().__init__()
        else:
            self._spawn_food()

        self.player = None
        self.is_winner = False
        self.fps = FPS
        self.highest_score = 0

        self.nets = []
        self.snakes = []
        self.ge = []

    def _update(self):
        self.screen.fill(self.background)
        self.food.draw(self.screen)
        for snake in self.snakes:
            snake.draw(self.screen)

        if self.is_winner:
            if self.snakes:
                self._display_score(self.snakes[0].score)
        else:
            self._display_score(self.highest_score, text='Highest score: ')

        pg.display.update()
        self.clock.tick(self.fps)

    def _setup_nn(self, genome, config):
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.nets.append(net)
        self.snakes.append(AISnake(
            *PLAYER_START_POS,
            *PLAYER_SIZE))
        self.ge.append(genome)

    def _change_fitness(self, index, value):
        if not self.is_winner:
            self.ge[index].fitness += value

    def _delete_snake(self, snake):
        index = self.snakes.index(snake)
        if self.highest_score < snake.score:
            self.highest_score = snake.score
            self._change_fitness(index, self.highest_score)
        self.nets.pop(index)
        self.ge.pop(index)
        self.snakes.pop(index)

    def eval_genomes(self, genomes, config):
        self.running = True

        for genome_id, genome in genomes:
            self._setup_nn(genome, config)

        while self.running:
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    quit()
                    break

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE and not self.is_winner:
                        for snake in self.snakes:
                            self._change_fitness(self.snakes.index(snake), -5)
                            self._delete_snake(snake)

            else:

                if not self.snakes:
                    self.running = False
                    break

                for x, snake in enumerate(self.snakes):

                    if not snake.moves_left:
                        self._change_fitness(self.snakes.index(snake), -4)
                        self._delete_snake(snake)
                        continue

                    self._change_fitness(x, 0.1)

                    output = self.nets[self.snakes.index(snake)].activate((snake.get_input_values(self.food)))
                    snake.change_direction_by_output(output)

                    if snake.move_and_collide():
                        self._change_fitness(self.snakes.index(snake), -4)
                        self._delete_snake(snake)

                    elif snake.eat(self.food):
                        self._spawn_food()
                        self._change_fitness(self.snakes.index(snake), 3)
                        snake.moves_left += 100
                    else:
                        self._change_fitness(x, -0.01)
                        snake.moves_left -= 1

                self._update()

    def run_nn(self, config_file):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_file)

        p = neat.Population(config)

        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        winner = p.run(self.eval_genomes, GENERATIONS)
        import pickle
        pickle.dump(winner, open("winner.pickle", "wb"))

        print('\nBest genome:\n{!s}'.format(winner))

        from pathlib import Path
        Path("stats").mkdir(parents=True, exist_ok=True)

        visualize.plot_stats(stats, ylog=True, view=True, filename=os.path.join('stats', "feedforward-fitness.svg"))
        visualize.plot_species(stats, view=True, filename=os.path.join('stats', "feedforward-speciation.svg"))

        node_names = {
            2: 'Right',
            1: 'Left',
            0: 'Forward',
            -1: 'Danger forward',
            -2: 'Danger right',
            -3: 'Danger left',
            -4: 'Dir left',
            -5: 'Dir right',
            -6: 'Dir up',
            -7: 'Dir down',
            -8: 'Food left',
            -9: 'Food right',
            -10: 'Food up',
            -11: 'Food down',
        }
        visualize.draw_net(config, winner, True, node_names=node_names)

        visualize.draw_net(config, winner, view=True, node_names=node_names,
                           filename=os.path.join('stats', "winner-feedforward.gv"))
        visualize.draw_net(config, winner, view=True, node_names=node_names,
                           filename=os.path.join('stats', "winner-feedforward-enabled.gv"), show_disabled=False)
        visualize.draw_net(config, winner, view=True, node_names=node_names,
                           filename=os.path.join('stats', "winner-feedforward-enabled-pruned.gv"), show_disabled=False, prune_unused=True)

    def run_winner(self, config_file, winner_path):
        with open(winner_path, 'rb') as f:
            winner = pickle.load(f)

        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_file)
        self.is_winner = True
        self.eval_genomes(((0, winner), ), config)
        return self.highest_score


