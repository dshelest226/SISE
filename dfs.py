import puzzle
from collections import deque
from time import time

max_depth = 20

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
    def __init__(self, file_name : str, strategy_number=0):
        self.file_name = file_name
        self.moves = deque()
        self.table = puzzle.Puzzle()
        self.table.setup(file_name)
        self.strategy = strategies[strategy_number]
        self.cannot_move = False
        self.rollback = False
        self.rollback_last = False
        self.was_rollback = False
        self.last_move = ''
        # Stats :
        self.depth = 0
        self.time = time()
        self.counter = 0

    def return_solution(self):
        moves = ''
        for i in self.moves:
            moves += i
        return str(len(self.moves)) + '\n' + str(moves)

    def return_stats(self):
        stats = ''
        stats += str(len(self.moves)) + '\n'  # długość znalezionego rozwiązania
        stats += str(self.counter) + '\n'     # liczbę stanów odwiedzonych;
        stats += str(self.counter) + '\n'     # liczbę stanów przetworzonych;
        stats += str(self.depth) + '\n'       # maksymalną osiągniętą głębokość rekursji;
        stats += str('{:.3f}'.format((time() - self.time) * 1000))  # czas

        return stats

    def get_element_id(self, elem):
        for i in range(len(self.strategy)):
            if self.strategy[i] == elem:
                return i

    def move(self):
        start = self.get_element_id(self.last_move) + 1 if self.was_rollback else 0

        children = self.table.get_children()
        changed = False
        for i in range(start, len(self.strategy)):
            if children.get(self.strategy[i]) is not None and not changed:
                self.table.change_position(0,
                                           children.get(self.strategy[i]))
                changed = True
                self.moves.append(self.strategy[i])
                self.last_move = self.strategy[i]
                self.counter += 1

        if not changed:
            self.cannot_move = True
            self.rollback = True

    def solve(self):
        while True :
            action = True

            self.depth = len(self.moves) if self.depth < len(self.moves) else self.depth

            if self.table.is_solved():
                return self.return_solution(), self.return_stats()

            if len(self.moves) == max_depth and not(self.rollback or self.rollback_last or self.was_rollback) and action:
                action = False

                if self.moves[-1] == self.strategy[-1]:
                    self.rollback_last = True

                else :
                    self.rollback = True

                self.last_move = self.moves[-1]

            if (self.rollback or self.rollback_last) and action:
                action = False

                self.last_move = self.moves.pop()
                self.table.change_with_direction_reverse(self.last_move)
                self.was_rollback = True

                if self.rollback:
                    self.rollback = False
                    if self.moves[-1] == self.strategy[-1] and (self.last_move == self.strategy[-1] or self.cannot_move):
                        self.cannot_move = False
                        self.rollback_last = True

                if self.rollback_last:
                    self.rollback_last = False
                    if self.last_move == self.strategy[-1]:
                        self.rollback_last = True
                        self.was_rollback = False

            if action and not (self.rollback or self.rollback_last):
                self.move()
                self.was_rollback = False



