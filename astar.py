import puzzle
from copy import deepcopy
from time import time
from collections import deque

directions = ['U', 'D', 'L', 'R']
max_time = 30


class AStar:
    def __init__(self, file_name : str, heuristic : str):
        self.table = puzzle.Puzzle()
        self.table.setup(file_name)
        self.parent_table = puzzle.Puzzle()
        self.parent_table.setup(file_name)

        self.heuristic = 'manh' if heuristic == 'manh' else 'hamm'
        self.open_list = deque([self.table])
        self.closed_list = set()
        # Stats :
        self.time = time()
        self.visited = 1
        self.counter = 0
        self.depth = 0
        self.moves = ''

    def solve(self):
        while True:
            self.open_list = deque(sorted(list(self.open_list), key=lambda elem: elem.get_f_a()))
            self.table = self.open_list.popleft()
            self.counter += 1

            if self.table.is_solved():
                return self.return_solution(), self.return_stats()

            if time() - self.time > max_time:
                return '-1', self.return_stats(True)

            children = self.table.get_children()

            for i in range(len(children)):
                if children.get(directions[i]) is not None:
                    future_table = deepcopy(self.table)
                    future_table.change_position(0, children.get(directions[i]))
                    future_table.set_move(directions[i])
                    future_table.set_parent_table(self.table)
                    future_table.set_depth(self.table.get_depth() + 1)
                    f_a = future_table.get_depth() + self.heuristic_function(future_table)

                    future_table.set_f_a(f_a)
                    self.visited += 1
                    if self.depth < future_table.get_depth():   # Max depth
                        self.depth = future_table.get_depth()

                    if future_table.hash_code() not in self.closed_list:
                        self.open_list.appendleft(future_table)
                        self.closed_list.add(future_table.hash_code())

    def heuristic_function(self, table : puzzle) -> int:
        counter = 0

        if self.heuristic == 'manh':
            for row in range(len(table.get_table())):
                for col in range(len(table.get_table()[row])):
                    if puzzle.solved_board[row][col] != table.get_table()[row][col]:
                        current_x, current_y = self.table.find_cell(puzzle.solved_board[row][col])
                        counter += abs(row - current_x) + abs(col - current_y)

        if self.heuristic == 'hamm':
            for row in range(len(table.get_table())):
                for col in range(len(table.get_table()[row])):
                    if table.get_table()[row][col] != puzzle.solved_board[row][col]:
                        counter += 1

        return counter

    def return_solution(self):
        self.set_solved_moves()
        return str(self.table.get_depth()) + '\n' + str(self.moves)

    def return_stats(self, fail=False):
        stats = ''
        if not fail:
            stats += str(self.table.get_depth()) + '\n'  # długość znalezionego rozwiązania
        if fail:
            stats += '-1' + '\n'
        stats += str(self.visited) + '\n'  # liczbę stanów odwiedzonych;
        stats += str(self.counter) + '\n'  # liczbę stanów przetworzonych;
        stats += str(self.depth) + '\n'  # maksymalną osiągniętą głębokość rekursji;
        stats += str('{:.3f}'.format((time() - self.time) * 1000))  # czas
        return stats

    def set_solved_moves(self):
        solved_table = deepcopy(self.table)
        while solved_table.hash_code() != self.parent_table.hash_code():
            self.moves += solved_table.get_move()
            solved_table = solved_table.get_parent_table()
        self.moves = self.moves[::-1]
