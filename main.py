# -*- coding: UTF-8 -*-

import random
import time
from multiprocessing import Process, Pipe


# algorithm names:
SEQUENTIAL = 'sequencial'
PARALLEL = 'paralelo'

# input files
ENTRADAS = {
        'S': ['small1.txt', 'small2.txt', 'small3.txt', 'small4.txt', 'small5.txt'],
        'M': ['medium1.txt', 'medium2.txt', 'medium3.txt', 'medium4.txt', 'medium5.txt'],
        'L': ['large1.txt', 'large2.txt', 'large3.txt', 'large4.txt', 'large5.txt']
}
C_ENTRADA = {
        'S': '1000',
        'M': '10000',
        'L': '1000000'
        }


def get_input_path(tipo_entrada):
    r = random.randint(0, 4)
    return 'input_samples/' + ENTRADAS[tipo_entrada][r]


def main(algoritmo, tipo_entrada):
    path = get_input_path(tipo_entrada)
    lista = prepare_input(path)

    if algoritmo == SEQUENTIAL:
        i = time.time()
        quicksort(lista)
        e = time.time()
        return "%s;%s;%s" % (algoritmo, C_ENTRADA[tipo_entrada], str(e-i))
    elif algoritmo == PARALLEL:
        i = time.time()
        pconn, cconn = Pipe()
        n = 3
        p = Process(target=parallelquicksort,
                    args=(lista, cconn, n))
        p.start()
        pconn.recv()

        p.join()
        e = time.time()
        return "%s;%s;%s" % (algoritmo, C_ENTRADA[tipo_entrada], str(e-i))


def prepare_input(path):
    """Read a text file user provides and return a list."""
    with open(path, 'r') as i:
        lista = i.read().splitlines()
        return lista


def quicksort(input=None):
    if len(input) <= 1:
        return input
    pivot = input.pop(random.randint(0, len(input) - 1))

    return (quicksort([x for x in input if x < pivot]) +
           [pivot] +
           quicksort([x for x in input if x >= pivot]))


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

    menoresProc = Process(target=parallelquicksort,
                          args=(menoresP, cconnMenores, procNum - 1))

    pconnMaiores, cconnMaiores = Pipe()
    maioresProc = Process(target=parallelquicksort,
                          args=(maioresP, cconnMaiores, procNum - 1))


    menoresProc.start()
    maioresProc.start()

    conn.send(pconnMenores.recv() + [pivo] + pconnMaiores.recv())
    conn.close()

    menoresProc.join()
    maioresProc.join()


if __name__ == '__main__':
    main()

