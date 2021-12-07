import Puzzle
from copy import deepcopy
from Bfs import *
from Dfs import *
from glob import glob
from numpy import genfromtxt


def print_hi():
    strategy = 0
    # for i in glob("./Setups/*"):
        # for strategy in range(8):
    i = './Setups\\4x4_06_00007.txt'
    # try:
    dfs = Dfs(i.replace("\\", "/"), strategy)
    print()
    dfs.get_table().print_table()
    print(f'\nStep count : {dfs.get_steps()}')
    print(f'SOLVED MOVES : {dfs.get_moves()}')
    print(f'Time : {dfs.get_time()}')
    del dfs
# except :
#         print(i)
#         print("No solution")

    # a = Puzzle.Puzzle()
    # a.setup('./Setups/4x4_07_00207.txt')
    # a.print_table()
    # b = deepcopy(a)
    # print(hash(str(a.get_table())))

if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
