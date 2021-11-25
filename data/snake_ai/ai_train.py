from data.snake_ai.ai_game import AIGame


class Train(AIGame):
    def __init__(self):
        super().__init__(no_window=True)

        self.highest_score = 0
        self.running = False
        self.is_winner = False

        self.nets = []
        self.snakes = []
        self.ge = []
        self._spawn_food()

    def eval_genomes(self, genomes, config):
        self.running = True

        for genome_id, genome in genomes:
            self._setup_nn(genome, config)

        while self.running:

            if not self.snakes:
                self.running = False
                break

            for x, snake in enumerate(self.snakes):

                if not snake.moves_left:
                    self._change_fitness(self.snakes.index(snake), -4 * snake.length)
                    self._delete_snake(snake)
                    continue

                self._change_fitness(x, +0.1)

                output = self.nets[self.snakes.index(snake)].activate((snake.get_input_values(self.food)))
                snake.change_direction_by_output(output)

                if snake.move_and_collide():
                    self._change_fitness(self.snakes.index(snake), -2.5 * snake.length)
                    self._delete_snake(snake)

                elif snake.eat(self.food):
                    self._spawn_food()
                    self._change_fitness(self.snakes.index(snake), 20)
                    snake.moves_left += 100
                else:
                    self._change_fitness(x, -0.01)
                    snake.moves_left -= 1

