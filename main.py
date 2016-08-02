# -*- coding: UTF-8 -*-

import random
import sys
from multiprocessing import Process, Pipe

# TODO: definp
DEFAULT_INPUT = 'default_input.txt'
DEFAULT_OUTPUT = None

# algorithm names:
SEQUENTIAL = 'sequencial'
PARALLEL = 'paralelo'


def main():
    print(sys.argv)
    if len(sys.argv) <= 1:
        print("tá perdido, moral? "
              "modo de uso: \n"
              " ./ordenar <algoritmo> <entrada>.txt \n"
              "ex.: ./ordenar sequencial nomes.txt")

    # read input args
    alg = sys.argv[1]
    input = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_INPUT
    output = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_OUTPUT

    input = prepare_input(input)

    if alg == SEQUENTIAL:
        outcome = quicksort(input)
    elif alg == PARALLEL:
        outcome = parallelquicksort(input)

    if output is DEFAULT_OUTPUT:
        for line in outcome:
            print(line)
    else:
        with open(output, 'w') as o:
            for line in outcome:
                o.write(line + '\n')


def prepare_input(input):
    """Read a text file user provides and return a list."""
    with open(input, 'r') as i:
        list = i.read().splitlines()
        return list


def quicksort(input=None):
    if len(input) <= 1:
        return input
    pivot = input.pop(random.randint(0, len(input) - 1))

    return quicksort([x for x in input if x < pivot]) \
           + [pivot] \
           + quicksort([x for x in input if x >= pivot])

def parallelquicksort(input=None):
    if input is None: print('ho')
    return sorted(input)


if __name__ == '__main__':
    main()





