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
        pconn, cconn = Pipe()
    
        n = 3

        p = Process(target=parallelquicksort, \
                args=(input, cconn, n))
        p.start()
    
        outcome = pconn.recv()

        p.join()

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

def parallelquicksort(lista, conn, procNum):
    if procNum <= 0 or len(lista) <= 1:
        conn.send(quicksort(lista))
        conn.close()
        return

    pivo = lista.pop(random.randint(0, len(lista)-1))

    menoresP = []
    for x in lista:
        if x < pivo:
            menoresP.append(x)
 
    maioresP = []
    for x in lista:
        if x >= pivo:
            maioresP.append(x)


    pconnMenores, cconnMenores = Pipe()

    menoresProc = Process(target=parallelquicksort, \
            args=(menoresP, cconnMenores, procNum - 1))

    pconnMaiores, cconnMaiores = Pipe()
    maioresProc = Process(target=parallelquicksort, \
            args=(maioresP, cconnMaiores, procNum - 1))


    menoresProc.start()
    maioresProc.start()

    conn.send(pconnMenores.recv() + [pivo] + pconnMaiores.recv())
    conn.close()

    menoresProc.join()
    maioresProc.join()


if __name__ == '__main__':
    main()





