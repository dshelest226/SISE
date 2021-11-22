import Puzzle
from copy import deepcopy
import sys
from time import time

sys.setrecursionlimit(99999999)

strategys = [
             ['R', 'D', 'U', 'L'],
             ['R', 'D', 'L', 'U'],
             ['D', 'R', 'U', 'L'],
             ['D', 'R', 'L', 'U'],
             ['L', 'U', 'D', 'R'],
             ['L', 'U', 'R', 'D'],
             ['U', 'L', 'D', 'R'],
             ['U', 'L', 'R', 'D']
]

# Стратегии :

# prawo - dół - góra - lewo;
# prawo - dół - lewo - góra;
# dół - prawo - góra - lewo;
# dół - prawo - lewo - góra.
# lewo - góra - dół - prawo.
# lewo - góra - prawo - dół;
# góra - lewo - dół - prawo;
# góra - lewo - prawo - dół;

# to do list
# Нам нужно три стека , в которых будут хранится элементы класса Puzzle
# Что если вместо хэша использовать строку, которая будет состоять из значений ячеек в соответсвии с их местоположением
# На пример : 1230567891011121314415
# Нужно проверить буду ли они уникальны


class Bfs:
    def __init__(self, file_name: str):
        self.table = Puzzle.Puzzle()
        self.table.setup(file_name)
        self.time = time()
        self.parent_table = deepcopy(self.table)
        self.current_strategy = ['R', 'D', 'U', 'L']
        self.open_list = []
        self.closed_list = []
        self.steps_count = 0
        self.file_name = file_name  # Для того чтобы при нахождении решения мы записывали файл по типу
        self.solved_moves = ''       # SOLVED_{file_name}

        print(f'Table :')
        self.parent_table.print_table()
        print(self.file_name)
        self.solve(self.table)
        self.write_to_file()

    def solve(self, table: Puzzle):
        self.table = table

        if self.table.is_solved():
            self.time = time() - self.time
            return self.table, self.count_info(), self.solved_moves[::-1], self.time

        zero_cell = self.table.find_cell(0)
        zero_children = zero_cell.get_children(self.table)

        for i in range(len(self.current_strategy)):
            direction_number = zero_children.get(self.current_strategy[i])

            if direction_number is not None:
                # print(direction_number.get())

                future_table = deepcopy(self.table)
                future_table.change_position(0, direction_number.get())
                future_table.set_parent_table(self.table)
                future_table.set_move(self.current_strategy[i])

                self.open_list.append(future_table)

        self.closed_list.append(self.table.string_hash)
        # print()
        # print(len(self.open_list))
        # print(len(self.closed_list))
        # self.table.print_table()

        return self.solve(self.get_table_from_open_list())

    def check_closed_list(self, table: Puzzle):
        for i in self.closed_list:
            if i == table.string_hash():
                return False
        return True

    def get_table_from_open_list(self):
        table = deepcopy(self.open_list[0])
        self.open_list.remove(self.open_list[0])
        if not self.check_closed_list(table):
            self.get_table_from_open_list()
        return table

    def count_info(self):
        solved_table = deepcopy(self.table)
        while solved_table.string_hash() != self.parent_table.string_hash():
            # print(f"Step back : {self.steps_count}")
            # solved_table.print_table()
            self.steps_count += 1
            self.solved_moves += solved_table.get_move()
            solved_table = solved_table.get_parent_table()
        return self.steps_count

    def get_steps(self) -> int:
        return self.steps_count

    def get_moves(self) -> str:
        return self.solved_moves[::-1]

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
                    + '_bfs_' \
                    + str(code_name) \
                    + '_sol.txt'
        with open(file_name, 'w') as file:
            file.write(str(self.steps_count) + '\n' + str(self.get_moves()))
