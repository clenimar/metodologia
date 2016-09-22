import csv

from main import main as ordenar


TRAT = {
        "1": ['sequencial', 'S'],
        "2": ['sequencial', 'M'],
        "3": ['sequencial', 'L'],
        "4": ['paralelo', 'S'],
        "5": ['paralelo', 'M'],
        "6": ['paralelo', 'L']
}
N_TRAT = 6
N_REPETICOES = 20


def experimento():
    for t in TRAT:
        print "tratamento %s" % t
        for n in range(1, N_REPETICOES + 1):
            o = ordenar(TRAT[t][0], TRAT[t][1])
            print "repeticao #%d: %s" % (n, o)
