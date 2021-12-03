from Cell import *
from copy import deepcopy
from numpy import genfromtxt


SOLVED_BOARD = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]


class Puzzle:
    def __init__(self):
        self.table = [[] for i in range(4)]
        self.parent_table = None  # Записываем родительский сетап
        self.moved_to = None  # Для рапорта требуется последовательность движений

    def setup(self, file_name : str):
        # Загрузка из файла
        data_from_file = genfromtxt(file_name, delimiter='', skip_header=1, dtype=int)
        for i in range(4):
            for j in range(4):
                self.table[i].append(Cell(data_from_file[i][j]))

    def change_position(self, number_1: int, number_2: int):
        cell_1 = self.find_cell(number_1)
        cell_2 = self.find_cell(number_2)

        cell_1.set(number_2)
        cell_2.set(number_1)

    def find_cell(self, number: int) -> Cell:
        for i in self.table:
            for j in i:
                if j.get() == number:
                    return j

    def get_table(self) -> []:
        return self.table

    def set_table(self, table):
        self.table = deepcopy(table)

    def set_parent_table(self, table):
        self.parent_table = table

    def get_parent_table(self) -> []:
        return self.parent_table

    def get_move(self) -> str:
        return self.moved_to

    def set_move(self, move : str):
        self.moved_to = move

    def find_cell_location(self, cell : Cell):
        for i in range(4):
            for j in range(4):
                if self.table[i][j].get() == cell.get():
                    return i, j

    def find_number_location(self, number) -> []:
        for i in range(4):
            for j in range(4):
                if self.table[i][j] == number:
                    return i, j

    def is_solved(self) -> bool:
        for i in range(4):
            for j in range(4):
                if self.table[i][j].get() != SOLVED_BOARD[i][j]:
                    return False
        return True

    def print_table(self):
        for i in self.table:
            row = '[ '
            for j in i:
                row += str(j.get()) + ' '
            row += ' ]'
            print(row)

    def string_hash(self):
        test_hash = ''
        for i in self.table:
            for j in i:
                test_hash += str(j.get())
        return test_hash

    def is_equal(self, that_table : Puzzle) -> bool:
        for i in range(4):
            for j in range(4):
                if self.table[i][j] != that_table.get_table()[i][j]:
                    return False

        return True
