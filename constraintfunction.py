from constraint import *


def disjoint_sets(problem, set1, set2):
    for var1 in set1:
        for var2 in set2:
            problem.addConstraint(lambda x, y: x != y, (var1, var2))


def sort_craps_table(d0, d1, d2, d3):
    return d0 < d1 < d2 < d3
