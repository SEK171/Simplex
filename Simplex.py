# implementation of the simplex algorithm by SEK171

# requires the package numpy


# library to handle matricies
import numpy as np


def extract_point(base, tab):
    point = [0 for _ in range(base.shape[0])]
    tabi = 1
    pointi = 0
    i = 1

    while (i < len(base)):
        if base[i - 1] == tabi:
            point[pointi] = tab[tabi, -1]
            tabi += 1
            pointi += 1
            i = 0
        i += 1
    return np.array(point)


def test_optimale(tab, base):
    # this is done by checking the the z row and etc..
    not_solvable = 1
    solution_found = 1
    unique = 1
    for i, x in enumerate(base):
        # si pas var de base
        if not x:
            # check if the current value is negative
            if tab[0][i + 1] < 0:
                # still work to do or no solution
                solution_found = 0
                # check the rows
                for y in tab[:][i + 1]:
                    # check if it is positive or not to see if we can continue
                    if y > 0:
                        not_solvable = 0
            # if zero
            elif tab[0][i + 1] == 0:
                # we found a zero the solution is not unique
                unique = 0
            else:
                # the value is positive we may pass it
                pass

        # return values corresponding to the found result
        if solution_found:
            solution = extract_point(base, tab)
            if unique:
                print("la solution est: ")
                print(solution)
                print("au plus la solution est unique")
                print(f"x1 = {solution[0]}, x2 = {solution[1]}")
                print(f"max z = {np.sum(c * solution[0:2].T)}")
                return 2
            else:
                print("la solution est: ")
                print(solution)
                print("au plus la solution n'est pas unique")
                print(f"x1 = {solution[0]}, x2 = {solution[1]}")
                print(f"max z = {np.sum(c * solution[0:2].T)}")
                return 1
        else:
            if not_solvable:
                print("pas de solution finie")
                return -1
            else:
                return 0


def pivot(tab, base):
    # le minimum des valeurs negative
    pivot_col = np.argmin(tab[0, 1:-1]) + 1

    # divisions are the bi/ail
    divisions = []
    for i in range(1, tab.shape[0]):
        if tab[i, pivot_col] > 0:
            divisions.append(tab[i, -1] / tab[i, pivot_col])
        else:
            divisions.append(np.inf)
    # the value of the pivot row is the minimum of divisions
    pivot_row = np.argmin(divisions) + 1
    # the value of the pivot
    pivot_element = tab[pivot_row, pivot_col]

    # divide the pivot line by the pivot element
    tab[pivot_row, :] /= pivot_element

    # for the other lines except the pivot line
    for i in range(tab.shape[0]):
        if i != pivot_row:
            # here you can element wise multiply the lines with the pivot line
            tab[i, :] -= tab[i, pivot_col] * tab[pivot_row, :]

    # position d'element sortant
    exiting_position = base.tolist().index(pivot_row)
    # update the base
    base[pivot_col - 1] = base[exiting_position]
    base[exiting_position] = 0

    return tab, base


def simplex(tab, base):
    optimale = test_optimale(tab, base)

    while not optimale:
        tab, base = pivot(tab, base)
        optimale = test_optimale(tab, base)


# define the problem
# max z = cX
# SC:
#     AX <= b
#     X >= 0

c = np.array([5, 8])  # 5*x1 + 8*x2
A = np.array([[1, 1],  # x1 + x2
              [1, -2],  # x1 -2*x2
              [-1, 4]])  # -x1 + 4x2
b = np.array([[2, 0, 1]]).T  # < 2, < 0, < 1

n = A.shape[0]  # dimention/nbr des var d'ecart
I = np.identity(n)

z = np.array([[1] + [-1 * i for i in c] + [0 for _ in range(n + 1)]])

table = np.concatenate((np.array([[0 for _ in range(n)]]).T, A, I, b), 1)
tab = np.concatenate((z, table))

base = np.array([0, 0, 1, 2, 3])

# main
simplex(tab, base)
