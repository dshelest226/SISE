from bfs import Bfs
from dfs import Dfs
from astar import AStar
import argparse


def write_to_files(sol_info, sol_stat, sol_file, stat_file):

    with open(sol_file, 'w') as file:
        file.write(sol_info)

    with open(stat_file, 'w') as file:
        file.write(sol_stat)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Algorithm, Order/Heuristic,"
                                                 "Source file, Solution file, Statistics file.")
    parser.add_argument('algorithm')
    parser.add_argument('order')
    parser.add_argument('source_file')
    parser.add_argument('solution_file')
    parser.add_argument('statistic_file')
    args = parser.parse_args()

    stategy_code = {
        'RDUL' : 0, 'RDLU' : 1,
        'DRUL' : 2, 'DRLU' : 3,
        'LUDR' : 4, 'LURD' : 5,
        'ULDR' : 6, 'ULRD' : 7
    }

    solution_info = ''
    stats_info = ''

    if args.algorithm.lower() == 'bfs' :
        if stategy_code.get(args.order.upper()) is not None:
            code = stategy_code.get(args.order.upper())
            sol = Bfs(args.source_file, code)
            solution_info, stats_info = sol.solve()
        else :
            print('ORDER ERROR')

    elif args.algorithm.lower() == 'dfs' :
        if stategy_code.get(args.order.upper()) is not None:
            code = stategy_code.get(args.order.upper())
            sol = Dfs(args.source_file, code)
            solution_info, stats_info = sol.solve()
        else:
            print('ORDER ERROR')

    elif args.algorithm.lower() == 'astr':
        if args.order.lower() in ['manh', 'hamm']:
            sol = AStar(args.source_file, args.order.lower())
            solution_info, stats_info = sol.solve()
        else:
            print('ORDER ERROR')

    else :
        print('Alghorytm error')

    write_to_files(solution_info, stats_info, args.solution_file, args.statistic_file)



