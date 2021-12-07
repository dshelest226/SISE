from Cell import *
from copy import deepcopy
from numpy import genfromtxt


SOLVED_BOARD = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]


class Puzzle:
    def __init__(self):
        self.table = [[] for i in range(4)]
        self.parent_table = None  # Записываем родительский сетап
        self.moved_to = ""  # Для рапорта требуется последовательность движений
        self.children = {}
        self.depth = 0


    def setup(self, file_name : str):
        # Загрузка из файла
        data_from_file = genfromtxt(file_name, delimiter='', skip_header=1, dtype=int)
        for i in range(4):
            for j in range(4):
                self.table[i].append(data_from_file[i][j])

    def change_position(self, number_1: int, number_2: int):
        x_1, y_1 = self.find_cell(number_1)
        x_2, y_2 = self.find_cell(number_2)

        self.table[x_1][y_1] = number_2
        self.table[x_2][y_2] = number_1

    def find_cell(self, number: int):
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                if self.table[i][j] == number:
                    return i, j

    def get_table(self) -> []:
        return self.table

    def set_table(self, table : Puzzle):
        # self.table = deepcopy(table)
        self.table = deepcopy(table.get_table())

    def set_parent_table(self, table):
        self.parent_table = table

    def get_parent_table(self) -> []:
        return self.parent_table

    def get_depth(self) -> int:
        return self.depth

    def set_depth(self, new_depth : int):
        self.depth = new_depth

    def get_move(self) -> str:
        return self.moved_to

    def set_move(self, move : str):
        self.moved_to = move

    def add_move(self, move : str):
        self.moved_to += move

    def find_cell_location(self, cell : int):
        for i in range(4):
            for j in range(4):
                if self.table[i][j] == cell:
                    return i, j

    def find_number_location(self, number) -> []:
        for i in range(4):
            for j in range(4):
                if self.table[i][j] == number:
                    return i, j

    def is_solved(self) -> bool:
        for i in range(4):
            for j in range(4):
                if self.table[i][j] != SOLVED_BOARD[i][j]:
                    return False
        return True

    def print_table(self):
        for i in self.table:
            row = '[ '
            for j in i:
                row += str(j) + ' '
            row += ' ]'
            print(row)

    def is_equal(self, that_table : Puzzle) -> bool:
        for i in range(4):
            for j in range(4):
                if self.table[i][j] != that_table.get_table()[i][j]:
                    return False

        return True

    def __set_chidlren__(self):

        cell_location_row = self.find_cell_location(0)[0]
        cell_location_column = self.find_cell_location(0)[1]

        if self.check_around(self.table, 'U'):
            self.children['U'] = self.table[cell_location_row - 1][cell_location_column]
            if cell_location_row - 1 < 0:
                self.children['U'] = None
        else :
            self.children['U'] = None

        if self.check_around(self.table, 'D'):
            self.children['D'] = self.table[cell_location_row + 1][cell_location_column]
        else:
            self.children['D'] = None

        if self.check_around(self.table, 'L'):
            self.children['L'] = self.table[cell_location_row][cell_location_column - 1]
            if cell_location_column - 1 < 0:
                self.children['L'] = None
        else:
            self.children['L'] = None

        if self.check_around(self.table, 'R'):
            self.children['R'] = self.table[cell_location_row][cell_location_column + 1]
        else:
            self.children['R'] = None

    def check_around(self, table : Puzzle, direction: str):

        cell_location_row = self.find_cell_location(0)[0]
        cell_location_column = self.find_cell_location(0)[1]

        if direction == 'U':
            try:
                if self.table[cell_location_row - 1][cell_location_column]:
                    return True
            except IndexError:
                return False

        if direction == 'D':
            try:
                if self.table[cell_location_row + 1][cell_location_column]:
                    return True
            except IndexError:
                return False
        if direction == 'L':
            try:
                if self.table[cell_location_row][cell_location_column - 1]:
                    return True
            except IndexError:
                return False
        if direction == 'R':
            try:
                if self.table[cell_location_row][cell_location_column + 1]:
                    return True
            except IndexError:
                return False

    def get_children(self):
        self.__set_chidlren__()
        return self.children

    def hash_code(self):
        return hash(str(self.table))
