import Puzzle


class Cell:
    def __init__(self, number : int):
        self.number = number
        self.children = {}

    def set(self, number: int):
        self.number = number

    def get(self) -> int:
        return self.number

    def __set_chidlren__(self, table : Puzzle):

        cell_location_row = table.find_cell_location(self)[0]
        cell_location_column = table.find_cell_location(self)[1]

        if self.check_around(table, 'U'):
            self.children['U'] = table.get_table()[cell_location_row - 1][cell_location_column]
            if cell_location_row - 1 < 0:
                self.children['U'] = None
        else :
            self.children['U'] = None

        if self.check_around(table, 'D'):
            self.children['D'] = table.get_table()[cell_location_row + 1][cell_location_column]
        else:
            self.children['D'] = None

        if self.check_around(table, 'L'):
            self.children['L'] = table.get_table()[cell_location_row][cell_location_column - 1]
            if cell_location_column - 1 < 0:
                self.children['L'] = None
        else:
            self.children['L'] = None

        if self.check_around(table, 'R'):
            self.children['R'] = table.get_table()[cell_location_row][cell_location_column + 1]
        else:
            self.children['R'] = None

    def check_around(self, table : Puzzle, direction: str):

        cell_location_row = table.find_cell_location(self)[0]
        cell_location_column = table.find_cell_location(self)[1]

        if direction == 'U':
            try:
                if table.get_table()[cell_location_row - 1][cell_location_column]:
                    return True
            except IndexError:
                return False

        if direction == 'D':
            try:
                if table.get_table()[cell_location_row + 1][cell_location_column]:
                    return True
            except IndexError:
                return False
        if direction == 'L':
            try:
                if table.get_table()[cell_location_row][cell_location_column - 1]:
                    return True
            except IndexError:
                return False
        if direction == 'R':
            try:
                if table.get_table()[cell_location_row][cell_location_column + 1]:
                    return True
            except IndexError:
                return False

    def get_children(self, table : Puzzle):
        self.__set_chidlren__(table)
        return self.children

