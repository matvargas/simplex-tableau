import logging
from tableau import Tableau
from fractions import Fraction

class Simplex:

    def get_tableau_costs_vector(tableau):
        return tableau[0][int((len(tableau.T) - 1) / 3): len(tableau.T) - 1]

    def get_tableau_costs_vector_starting_index(tableau):
        return int((len(tableau.T) - 1) / 3)

    def get_tableau_b_vector(tableau):
        return tableau.T[len(tableau.T) - 1][1:]

    def get_tableau_a_matrix(tableau):
        return tableau[1:, int((len(tableau.T) - 1) / 3): len(tableau.T) - 1]

    def pivotate(tableau, pivotal_line, pivotal_colum, pivot):
        logging.debug('\n =================================== \n =   PIVOTATING   = \n ===================================')

        # Divide the pivotal line by pivot
        # tableau = tableau[pivotal_line, :] / pivot


    def define_viable_bases(tableau):

        logging.debug('\n =================================== \n =   DEFINING VIABLE BASES   = \n ===================================')

        # If B vector has all values greater than zero, because the entri format is always <=, 
        # the base will be the matrix formed by gap_vars.

        is_b_positive = True

        if any (n < 0 for n in tableau.T[len(tableau.T) - 1]):
            is_b_positive = False

        viable_bases = []

        if is_b_positive:
            logging.debug("B vector has only positive values")
            viable_bases.extend(range(int((len(tableau.T) - 1)/3) + int((len(tableau.T) - 1)/3), len(tableau.T) - 1 ))
            logging.debug("Viable bases: {}".format(viable_bases))
        else:
            logging.debug("B vector has at least one negative value")

        return viable_bases

    def pivotating(value, pivotal_row, column_index, matrix_tableau):

        logging.debug("Dividing pivotal row from A[{}][:]".format(pivotal_row))

        Tableau.print_tableau(matrix_tableau)

        for n in range(len(matrix_tableau[pivotal_row, :])):
            if matrix_tableau[pivotal_row][n] != 0:
                v = Fraction(matrix_tableau[pivotal_row][n] / value)
                matrix_tableau[pivotal_row][n] = Fraction(matrix_tableau[pivotal_row][n], v)

        logging.debug("Zeroing column {} from tableau[:][{}]".format(matrix_tableau[:, column_index], column_index))

        for n in range(len(matrix_tableau[:, column_index])):
            if n != pivotal_row and matrix_tableau[n][column_index] != 0:
                v = Fraction(matrix_tableau[n][column_index]/value)
                v = v * -1
                logging.debug("Value which will be used to zero tableau[{}][{}] is {} ".format(n, column_index, v))
                matrix_tableau[n][column_index] = matrix_tableau[n][column_index] + v

        Tableau.print_tableau(matrix_tableau)

        for row in range(len(matrix_tableau[:, column_index])):
            if row != pivotal_row and matrix_tableau[row][column_index] != 0:
                v = Fraction(matrix_tableau[row][column_index]/value)
                v = v * -1

                for column in range(len(matrix_tableau[:, :])):
                    logging.debug("Value which will be used to zero tableau[{}][{}] is {} ".format(row, column, v))
                    matrix_tableau[n][column_index] = matrix_tableau[n][column_index] + v

        Tableau.print_tableau(matrix_tableau)

    def define_lower_value(a_column, b_vector):

        lowest_value = Fraction(99999999, 1)
        pivot_row = -1

        logging.debug('A column corresponding ' + str(a_column))
        for n in range(0, len(b_vector)):
            logging.debug('b/a[n] = ' + str(b_vector[n]) + '/' + str(a_column[n]))
            if b_vector[n] != 0 and a_column[n] != 0:
                value = Fraction(b_vector[n], a_column[n])
                if value < lowest_value:
                    lowest_value = value
                    # Since we are using the A column excluding the costs vector value,
                    # we need to shift the row number at the and plus 1
                    pivot_row = n + 1

        msg = "Lowest value is {} on row #{} ".format(lowest_value, pivot_row)
        logging.debug(msg)

        return lowest_value, pivot_row

    def do_simplex(tableau):
        
        # viable_bases = Simplex.define_viable_bases(tableau.matrix_tableau)

        logging.debug('\n ======================== \n =   STARTING SIMPLEX   = \n ========================')

        c_vector = Simplex.get_tableau_costs_vector(tableau.matrix_tableau)
        b_vector = Simplex.get_tableau_b_vector(tableau.matrix_tableau)
        a_matrix = Simplex.get_tableau_a_matrix(tableau.matrix_tableau)
        c_starting_index = Simplex.get_tableau_costs_vector_starting_index(tableau.matrix_tableau)

        logging.warn('!!!!!!! VERIFY THE STARTING INDEX OF COSTS VECTOR !!!!!!!!! --> ' + str(c_starting_index))

        count = 0

        pivotal_column = -1

        # Iterate over costs vector looking for < 0 values
        while any(n < 0 for n in Simplex.get_tableau_costs_vector(tableau.matrix_tableau)) and count < 1:
            for cost_index, cost in enumerate(Simplex.get_tableau_costs_vector(tableau.matrix_tableau)):
                if cost < 0:

                    logging.debug('Index of cost = ' + str(cost_index) + ' cost ' + str(cost))

                    # Find the lower value over b[i]/a[c_index][i]
                    lower_value, pivotal_row = Simplex.define_lower_value(a_matrix[:, cost_index], b_vector)

                    # Pivotating
                    Simplex.pivotating(lower_value, pivotal_row, cost_index + c_starting_index, tableau.matrix_tableau)

            count += 1





