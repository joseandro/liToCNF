# This module provides means to randomly generate inequations
# Author: Joseandro Luiz

from random import randint
import numbers

def getRandomInequations(C, N, M):
    """
    This function creates and returns inequations based on its given
    parameters.

    @type  C: int
    @param C: Defines a and b, where ai E [-C, +C] and b E [0, C].
    @type  N: int
    @param N: Number of variables.
    @type  M: int
    @param M: Number of inequalities.
    @rtype:   list
    @return: A list containing dicts:
     a: coefficients,
     s: expression's signal
         0 : less or equal than
         1 : bigger or equal than
     b: inequations' right side result.
    """
    result = []
    if isinstance(C, numbers.Integral) and isinstance(N, numbers.Integral) and isinstance(M, numbers.Integral):
        for i in range(M):  # Number of inequations
            b = randint(0, C)
            s = randint(0, 1)  # Expression signal

            a = []
            sum = 0
            while True:
                for j in range(N):  # Number of coefficients
                    coeff = randint(-1 * C, C)
                    a.append(coeff)

                    if (coeff < 0):
                        coeff *= -1
                    sum += coeff
                if sum > b:
                    break

            dicta = {"a": a, "s": s, "b": b}
            result.append(dicta)
    else:
        print("Check your parameters, this function only takes integers")
    return result
