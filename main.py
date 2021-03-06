import logging
from tableau import Tableau
from simplex import Simplex
import sys

if len(sys.argv) >= 2:
    if sys.argv[1] == '-d':
        logging.basicConfig(level=logging.DEBUG)

def main():

    logging.debug('\n ======================== \n =   Reading Data   = \n ========================')

    vars_and_restrictions = input()
    vars_and_restrictions = vars_and_restrictions.split()

    r = int(vars_and_restrictions[0])
    v = int(vars_and_restrictions[1])

    logging.debug("Number of restrictions: {}".format(r))
    logging.debug("Number of variables: {}".format(v))

    c_input = input()
    c_list = list(c_input.split())
    c = []
    for i in range(len(c_list)):
        c.append(float(c_list[i]))

    logging.debug("Costs vector: {}".format(c))

    a = []
    b = []
    for i in range(r):
        line = input().split()
        a_row = []
        for j in range(len(line)):
            if j < v :
                a_row.append(float(line[j]))
            else:
                b.append(float(line[j]))
        a.append(a_row)

    logging.debug("Matrix A[]: {}".format(a))
    logging.debug("Vector B[]: {}".format(b))

    tableau = Tableau(r, v, c, a, b)
    Tableau.print_tableau(tableau.matrix_tableau)
    Simplex.do_simplex(tableau)

main()