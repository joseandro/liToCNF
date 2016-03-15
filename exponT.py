# This module transforms inequations to CNF in exponential time
# Author: Joseandro Luiz

import numpy as np

def checkIntersection(group, vector):
    for val in group:
        if len(np.intersect1d(val, vector)) == len(vector):
            return True
    return False

def transform(iq):
    """
    This function transforms inequations to CNF in exponential time

    @type  iq: list
    @param iq: List containing dict representing the inequations.
        a: coefficients,
        x: negative coefficients representation
        s: expression's signal
           0 : less or equal than
           1 : bigger or equal than
        b: inequations' right side result.
    @rtype:   list
    @return: A list containing dicts in the format DIMACS:
    """

    result = []
    for i, v in enumerate(iq) :
        print(v)
        clauses = []
        a = v['a']
        x = v['x']
        for indexForOuterA, valueForOuterA in enumerate(a): # define minimal covers
            clause = []
            sum = v['b'] # initial condition
            sum = sum - valueForOuterA
            try:
                x.index(indexForOuterA)
            except ValueError:
                clause.append(indexForOuterA+1)
            else:
                clause.append(-1*(indexForOuterA+1))

            if sum < 0 and checkIntersection(clauses, clause) == False:
                clauses.append(sorted(clause)) # If a valid clause is not in the list we add it
                continue # move to the next outer loop


            for indexForInnerA, valueForInnerA in enumerate(a):
                if indexForInnerA != indexForOuterA :
                    sum = sum - valueForInnerA

                    try:
                        x.index(indexForInnerA)
                    except ValueError:
                        clause.append(indexForInnerA+1)
                    else:
                        clause.append(-1*(indexForInnerA+1))

                    if sum < 0 :
                        if checkIntersection(clauses, clause) == False:
                            break
                        else :
                            sum = sum + valueForInnerA # backtrack operation
                            clause.pop()
                            continue

            if sum < 0 and checkIntersection(clauses, clause) == False:
                clauses.append(sorted(clause)) # If a valid clause is not in the list we add it
        result.append(clauses)
    return result