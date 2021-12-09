import Puzzle
from copy import deepcopy, copy
import sys
from time import time
from queue import LifoQueue

MAX_DEPTH = 20

strategies = [
    ['R', 'D', 'U', 'L'],
    ['R', 'D', 'L', 'U'],
    ['D', 'R', 'U', 'L'],
    ['D', 'R', 'L', 'U'],
    ['L', 'U', 'D', 'R'],
    ['L', 'U', 'R', 'D'],
    ['U', 'L', 'D', 'R'],
    ['U', 'L', 'R', 'D']
]


class Dfs:
    def __init__(self, file_name: str, number_of_stretegies=0):
        self.table = Puzzle.Puzzle()
        self.table.setup(file_name)
        self.time = time()
        self.parent_table = deepcopy(self.table)
        self.current_strategy = strategies[number_of_stretegies]
        self.open_list = LifoQueue()
        self.closed_list = {}
        self.steps_count = 0
        self.file_name = file_name  # Для того чтобы при нахождении решения мы записывали файл по типу
        self.solved_moves = ''  # SOLVED_{file_name}
        self.counter = 0
        self.visited = 1
        self.max_depth = 0

        print(f'Table :')
        self.parent_table.print_table()
        print(self.file_name)
        self.solve(self.table)
        self.write_to_file()

    def solve(self, table: Puzzle):
        self.open_list.put(table)

        while True:

            self.check_closed_list()

            # print(len(self.closed_list))

            if self.table.is_solved():
                self.time = time() - self.time
                return self.table, self.count_info(), self.solved_moves[::-1], self.time

            zero_children = self.table.get_children()

            for i in range(len(self.current_strategy)):
                direction_number = zero_children.get(self.current_strategy[-1-i])

                if direction_number is not None:

                    # future_table = deepcopy(self.table)
                    future_table = Puzzle.Puzzle()
                    future_table.set_table(self.table)
                    future_table.change_position(0, direction_number)
                    future_table.set_parent_table(self.table)
                    future_table.add_move(self.current_strategy[i])
                    future_table.set_depth(self.table.get_depth() + 1)

                    self.open_list.put(future_table)

            # self.closed_list.append(self.table)
            self.closed_list[len(self.closed_list) + 1] = self.table.hash_code()

    def check_closed_list(self):
        self.visited += 1

        self.table = self.open_list.get()

        if self.table.get_depth() > self.max_depth: # Dla statystyki
            self.max_depth = self.table.get_depth()

        if self.table.get_depth() > MAX_DEPTH: # Ograniczenie
            return self.check_closed_list()

        # for i in self.closed_list:
        #     if i.is_equal(self.table):
        #         return self.check_closed_list()

        if self.table.hash_code() in self.closed_list.values():
            return self.check_closed_list()

    def count_info(self):
        # solved_table = deepcopy(self.table)
        # while solved_table.hash_code() != self.parent_table.hash_code():
        #     self.steps_count += 1
        #     self.solved_moves += solved_table.get_move()
        #     solved_table = solved_table.get_parent_table()
        self.solved_moves = self.table.get_move()
        self.steps_count = len(self.solved_moves)
        return self.steps_count

    def get_steps(self) -> int:
        return self.steps_count

    def get_moves(self) -> str:
        return self.solved_moves

    def get_table(self) -> []:
        return self.table

    def get_time(self) -> float:
        return self.time

    def write_to_file(self):
        code_name = ''
        for i in self.current_strategy:
            code_name += i
        file_name = 'Solves_BFS/' \
                    + self.file_name.replace('Setups/', '').replace('.txt', '') \
                    + '_dfs_' \
                    + str(code_name)
        file_stats_name = file_name + "_stats.txt"
        file_name += "_sol.txt"

        if self.table == 'Error':
            with open(file_name, 'w') as file:
                file.write("-1")

        else:
            with open(file_name, 'w') as file:
                file.write(str(self.steps_count) + '\n' + str(self.get_moves()))

            with open(file_stats_name, 'w') as file:
                time_for_file = f"{1000 * (time() - self.time):.{3}f}"

                file.write(str(self.steps_count) + '\n' + str(self.visited) +
                           '\n' + str(len(self.closed_list)) + '\n' + str(self.max_depth) +
                           '\n' + time_for_file)


