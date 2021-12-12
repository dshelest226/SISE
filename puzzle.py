from copy import deepcopy
from numpy import genfromtxt


solved_board = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]


class Puzzle:
    def __init__(self):
        self.table = [[] for i in range(4)]
        self.parent_table = None
        self.moved_to = ""
        self.children = {}  # Kierunki w których możemy poruszać
        self.depth = 0
        self.f_a = 0  # Tylko dla Astar

    def setup(self, file_name : str):
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

    def set_table(self, table):
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

    def find_cell_location(self, cell : int):
        for i in range(4):
            for j in range(4):
                if self.table[i][j] == cell:
                    return i, j

    def is_solved(self) -> bool:
        return self.table == solved_board

    def print_table(self):
        for i in self.table:
            row = '[ '
            for j in i:
                row += str(j) + ' '
            row += ' ]'
            print(row)

    def check_around(self):

        cell_location_row = self.find_cell(0)[0]
        cell_location_column = self.find_cell(0)[1]

        self.children['U'] = None
        self.children['D'] = None
        self.children['L'] = None
        self.children['R'] = None

        try:
            if self.table[cell_location_row - 1][cell_location_column] and not cell_location_row - 1 < 0:
                self.children['U'] = self.table[cell_location_row - 1][cell_location_column]
        except IndexError:
            pass

        try:
            if self.table[cell_location_row + 1][cell_location_column]:
                self.children['D'] = self.table[cell_location_row + 1][cell_location_column]
        except IndexError:
            pass

        try:
            if self.table[cell_location_row][cell_location_column - 1] and not cell_location_column - 1 < 0:
                self.children['L'] = self.table[cell_location_row][cell_location_column - 1]
        except IndexError:
            pass

        try:
            if self.table[cell_location_row][cell_location_column + 1]:
                self.children['R'] = self.table[cell_location_row][cell_location_column + 1]
        except IndexError:
            pass

    def get_children(self):
        self.check_around()
        return self.children

    def hash_code(self):
        return hash(str(self.table))

    def get_f_a(self):
        return self.f_a

    def set_f_a(self, new : int):
        self.f_a = new

    def change_with_direction_reverse(self, direction : str):
        self.get_children()

        if direction == 'U' :
            direction = 'D'

        elif direction == 'D' :
            direction = 'U'

        elif direction == 'L' :
            direction = 'R'

        elif direction == 'R' :
            direction = 'L'

        direction_number = self.children.get(direction)
        self.change_position(0, direction_number)
