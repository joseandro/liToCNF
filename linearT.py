# This module transforms inequations to CNF in linear time
# Author: Joseandro Luiz

import numpy as np

def checkIntersection(group, vector):
    for val in group:
        if len(np.intersect1d(val, vector)) == len(vector):
            return True
    return False

def splitArray(arr):
    ceiling = arr[:len(arr)/2]
    floor = arr[len(arr)/2:]

    return {'ceiling': ceiling, 'floor' : floor }

def calculateM(_arr):
    arr =  sorted(_arr)
    aMax = arr[-1]

    return np.ceil(np.log2(aMax))

def fromIntToBin(num):
    return "{0:b}".format(num)

def fromBinToInt(bin):
    return int(bin, 2)

def binarySum(a, b):
    return bin(a + b)

def binaryMult(a, b):
    return bin(a * b)

def calculateIRightSide(b, M):
    pass

def calculateILeftSide(a, x, M):
    U = I = range(1, len(a)+1)
    _ = splitArray(I)

    V = _['floor']
    W = _['ceiling']
    


def transform(iq):
    """
    This function transforms inequations to CNF in linear time

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

    for i, v in enumerate(iq) :
        a = v['a']

        if len(a) < 1 :
            continue # Empty arrays are not allowed

        x = v['x']
        b = v['b']
        M = calculateM(a)

        iLeftSide = calculateILeftSide(a,x, M)
        iRightSide = calculateIRightSide(b, M)