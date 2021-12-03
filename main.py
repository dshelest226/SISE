from Puzzle import *
from copy import deepcopy
from Bfs import *
from glob import glob
from numpy import genfromtxt


def print_hi():
    for i in glob("./Setups/*"):
    # i = './Setups\\4x4_05_00006.txt'
        try:
            bfs = Bfs(i.replace("\\", "/"))
            print()
            bfs.get_table().print_table()
            print(f'\nStep count : {bfs.get_steps()}')
            print(f'SOLVED MOVES : {bfs.get_moves()}')
            print(f'Time : {bfs.get_time()}')
            del bfs
        except :
            print(i)
            print("No solution")

if __name__ == '__main__':
    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
