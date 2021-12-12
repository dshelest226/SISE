import puzzle
from copy import deepcopy
from time import time
from queue import Queue

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


class Bfs:
    def __init__(self, file_name: str, strategy_number=0):
        self.table = puzzle.Puzzle()
        self.table.setup(file_name)
        self.time = time()
        self.parent_table = deepcopy(self.table)
        self.current_strategy = strategies[strategy_number]
        self.open_list = Queue()
        self.closed_list = set()
        self.steps_count = 0
        self.file_name = file_name
        self.solved_moves = ''
        self.counter = 1
        self.visited = 1
        self.depth = 0

    def solve(self):
        self.open_list.put(self.table)

        while True:

            self.check_closed_list()

            if self.table.is_solved():
                self.count_info()
                return self.return_solution(), self.return_stats()

            self.counter += 1

            zero_children = self.table.get_children()

            for i in range(len(self.current_strategy)):
                direction_number = zero_children.get(self.current_strategy[i])

                if direction_number is not None:

                    future_table = deepcopy(self.table)
                    future_table.change_position(0, direction_number)
                    future_table.set_parent_table(self.table)
                    future_table.set_move(self.current_strategy[i])
                    future_table.set_depth(self.table.get_depth() + 1)

                    self.open_list.put(future_table)

            self.closed_list.add(self.table.hash_code())

    def check_closed_list(self):
        self.table = self.open_list.get()
        self.depth = self.table.get_depth() if self.depth < self.table.get_depth() else self.depth
        self.visited += 1
        if self.table.hash_code() in self.closed_list:
            return self.check_closed_list()

    def count_info(self):
        solved_table = deepcopy(self.table)
        while solved_table.hash_code() != self.parent_table.hash_code():
            self.steps_count += 1
            self.solved_moves += solved_table.get_move()
            solved_table = solved_table.get_parent_table()
        self.solved_moves = self.solved_moves[::-1]
        return self.steps_count

    def get_steps(self) -> int:
        return self.steps_count

    def get_moves(self) -> str:
        return self.solved_moves[::-1]

    def get_table(self) -> []:
        return self.table

    def get_time(self) -> float:
        return self.time

    def return_solution(self):
        return str(len(self.solved_moves)) + '\n' + str(self.get_moves())

    def return_stats(self):
        stats = ''
        stats += str(len(self.get_moves())) + '\n'  # długość znalezionego rozwiązania
        stats += str(self.visited) + '\n'  # liczbę stanów odwiedzonych;
        stats += str(self.counter) + '\n'  # liczbę stanów przetworzonych;
        stats += str(self.depth) + '\n'  # maksymalną osiągniętą głębokość rekursji;
        stats += str('{:.3f}'.format((time() - self.time) * 1000))  # czas
        return stats
