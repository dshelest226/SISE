import Puzzle
from collections import deque
import sys
from time import time

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


class dfs_test:
    def __init__(self, file_name : str):
        self.moves = deque()
        self.table = Puzzle.Puzzle()
        self.table.setup(file_name)
        self.strategy = strategies[0]
        # self.last_move = ''
        self.time = time()

    def get_element_id(self, elem):
        for i in range(len(self.strategy)):
            if self.strategy[i] == elem:
                return i
        return -1

    # def solve(self):
    #     while True:
    #         self.table.print_table()
    #         print(self.moves)
    #
    #         isChanged = False
    #
    #         if self.table.is_solved() :
    #             return self.table
    #
    #         if len(self.moves) == MAX_DEPTH:
    #             self.rollback()
    #             # if self.moves[-1] == self.strategy[-1]:
    #             #     self.table.change_with_direction_reverse(self.moves[-1])
    #             #     self.last_move = self.moves.pop()
    #             self.change_after_remove(self.table.get_children(), False)
    #
    #         elif len(self.moves) < MAX_DEPTH:
    #             children = self.table.get_children()
    #             for i in range(len(self.strategy)):
    #                 if not isChanged and children.get(self.strategy[i]) is not None:
    #                     isChanged = True
    #                     self.table.change_position(0,
    #                                                children.get(self.strategy[i])
    #                                                )
    #                     self.moves.append(self.strategy[i])
    #             if not isChanged:
    #                 self.rollback()
    #                 self.change_after_remove(self.table.get_children(), False)
    #
    # def change_after_remove(self, children : dict, isChanged : bool):
    #     for i in range(self.get_element_id(self.last_move) + 1, len(self.strategy)):
    #         if not isChanged and children.get(self.strategy[i]) is not None:
    #             isChanged = True
    #             self.table.change_position(0,
    #                                        children.get(self.strategy[i])
    #                                        )
    #             self.moves.append(self.strategy[i])
    #         if not isChanged:
    #             self.rollback()
    #             self.change_after_remove(self.table.get_children(), False)
    #
    # def last_move_check(self):
    #     if self.moves == self.strategy[-1]:
    #         self.table.change_with_direction_reverse(self.moves[-1])
    #         self.last_move = self.moves.pop()
    #         return True
    #     return False
    #
    # def rollback(self):
    #
    #     self.table.change_with_direction_reverse(self.moves[-1])
    #     self.last_move = self.moves.pop()
    #
    #     last_element = True
    #
    #     while last_element:
    #         if self.last_move == self.strategy[-1]:
    #             last_element = True
    #             self.table.change_with_direction_reverse(self.moves[-1])
    #             self.last_move = self.moves.pop()
    #             self.change_after_remove(self.table.get_children(), False)
    #         else :
    #             last_element = False

    def solve(self, rollback=False, rollback_last=False, last_move='', was_rollback=False, cannot_move=False):
        test = 0
        while True :
            action = True
            print(self.moves)
            test += 1
            print(f'counter {test}')
            # print(self.moves)

            if self.table.is_solved():
                # print(time() - self.time)
                print(self.moves)
                print('==========')
                return self.table

            if len(self.moves) == MAX_DEPTH and not(rollback or rollback_last or was_rollback) and action:
                action = False

                if self.moves[-1] == self.strategy[-1]:
                    rollback_last = True

                else :
                    rollback = True

                last_move = self.moves[-1]
                # return self.solve(rollback, rollback_last, last_move, was_rollback)

            if (rollback or rollback_last) and action:
                action = False
                if rollback:
                    rollback = False
                    last_move = self.moves.pop()
                    self.table.change_with_direction_reverse(last_move)

                    if self.moves[-1] == self.strategy[-1] and (last_move == self.strategy[-1] or cannot_move):
                        cannot_move = False
                        rollback_last = True
                    was_rollback = True


                    # return self.solve(rollback, rollback_last, last_move, was_rollback)

                if rollback_last:
                    rollback_last = False
                    last_move = self.moves.pop()
                    self.table.change_with_direction_reverse(last_move)
                    # last_move = self.moves.pop()
                    # self.table.change_with_direction_reverse(last_move)

                    was_rollback = True
                    if last_move == self.strategy[-1]:
                        rollback_last = True  # Может тут ставить rollback_last ?
                        was_rollback = False
                    # return self.solve(rollback, rollback_last, last_move, was_rollback)

            if action and was_rollback and not (rollback or rollback_last):
                action = False
                was_rollback = False
                children = self.table.get_children()
                changed = False
                for i in range(self.get_element_id(last_move) + 1, len(self.strategy)):
                    if children.get(self.strategy[i]) is not None and not changed:
                        self.table.change_position(0,
                                                   children.get(self.strategy[i]))
                        changed = True
                        self.moves.append(self.strategy[i])
                        last_move = self.strategy[i]

                if not changed:
                    cannot_move = True
                    rollback = True

                # return self.solve(rollback, rollback_last, last_move, was_rollback, cannot_move)

            if action and not (was_rollback or rollback_last or rollback) :
                action = False
                children = self.table.get_children()
                changed = False
                for i in range(len(self.strategy)):
                    if children.get(self.strategy[i]) is not None and not changed:
                        self.table.change_position(0,
                                                   children.get(self.strategy[i]))
                        changed = True
                        self.moves.append(self.strategy[i])
                        last_move = self.strategy[i]

                if not changed:
                    cannot_move = True
                    rollback = True

                # return self.solve(rollback, rollback_last, last_move, was_rollback, cannot_move)



