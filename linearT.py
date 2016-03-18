# This module transforms inequations to CNF in linear time
# Author: Joseandro Luiz

import numpy as np
global_index = 0

def splitArray(arr):
    ceiling = arr[:len(arr)/2]
    floor = arr[len(arr)/2:]

    return {'ceiling': ceiling, 'floor' : floor }

def calculateM(_arr):
    arr =  sorted(_arr)
    aMax = arr[-1]

    return np.ceil(np.log2(aMax))

def binarySum(a, b):
    return bin(a + b)

def binaryMult(a, b):
    return bin(a * b)

def calculateIRightSide(b, M):
    pass

def getUniqueID():
    global global_index
    global_index += 1
    return global_index

def resetUniqueIDSeeder():
    global global_index
    global_index = 0

def transAiXi(U, a, x, M):
    if len(U) == 1:
        return transAiAndDoTransMult(a[U[0]], U[0] in x, M)

    _ = splitArray(U)
    V = _['floor']
    W = _['ceiling']

    return transAiXi(V, a, x, M) + transAiXi(W, a, x, M) + transPlus(U, V, W, M)

def transPlus(U, V, W, M):
    result = []

    p0_U = getUniqueID()
    p0_V = getUniqueID()
    p0_W = getUniqueID()
    c01_U = getUniqueID()

    # Formula 11
    result.append([p0_U, p0_V,-1*p0_W])
    result.append([p0_U, -1*p0_V, p0_W])
    result.append([-1*p0_U, -1*p0_V,-1*p0_W])
    result.append([-1*p0_U, p0_V, p0_W])

    # Formula 12
    result.append([c01_U, -1*p0_V, -1*p0_W])
    result.append([-1*c01_U, p0_V])
    result.append([-1*c01_U, p0_W])

    for i in range(0, M):
        pk_U = getUniqueID()
        pk_V = getUniqueID()
        pk_W = getUniqueID()
        ck_m1_k_U = getUniqueID()
        ck_k_p1_U = getUniqueID()

        if i == 0:
            # Formula 13
            result.append([p0_U, -1*p0_V, p0_W, c01_U])
            result.append([p0_U, -1*p0_V, -1*p0_W, -1*c01_U])
            result.append([p0_U, p0_V, -1*p0_W, c01_U])
            result.append([p0_U, p0_V, p0_W, -1*c01_U])
            result.append([-1*p0_U, p0_V, p0_W, c01_U])
            result.append([-1*p0_U, p0_V, -1*p0_W, -1*c01_U])
            result.append([-1*p0_U, -1*p0_V, -1*p0_W, c01_U])
            result.append([-1*p0_U, -1*p0_V, p0_W, -1*c01_U])

            # Formula 14
            result.append([ck_k_p1_U, -1*pk_V, -1*pk_W])
            result.append([ck_k_p1_U, -1*pk_V, -1*c01_U])
            result.append([ck_k_p1_U, -1*pk_W, -1*c01_U])
            result.append([-1*ck_k_p1_U, pk_V, pk_W])
            result.append([-1*ck_k_p1_U, pk_V, c01_U])
            result.append([-1*ck_k_p1_U, pk_W, c01_U])

        else:
            # Formula 13
            result.append([pk_U, -1*pk_V, pk_W, ck_m1_k_U])
            result.append([pk_U, -1*pk_V, -1*pk_W, -1*ck_m1_k_U])
            result.append([pk_U, pk_V, -1*pk_W, ck_m1_k_U])
            result.append([pk_U, pk_V, pk_W, -1*ck_m1_k_U])
            result.append([-1*pk_U, pk_V, pk_W, ck_m1_k_U])
            result.append([-1*pk_U, pk_V, -1*pk_W, -1*ck_m1_k_U])
            result.append([-1*pk_U, -1*pk_V, -1*pk_W, ck_m1_k_U])
            result.append([-1*pk_U, -1*pk_V, pk_W, -1*ck_m1_k_U])

            # Formula 14
            result.append([ck_k_p1_U, -1*pk_V, -1*pk_W])
            result.append([ck_k_p1_U, -1*pk_V, -1*ck_m1_k_U])
            result.append([ck_k_p1_U, -1*pk_W, -1*ck_m1_k_U])
            result.append([-1*ck_k_p1_U, pk_V, pk_W])
            result.append([-1*ck_k_p1_U, pk_V, ck_m1_k_U])
            result.append([-1*ck_k_p1_U, pk_W, ck_m1_k_U])

    return result


def transAiAndDoTransMult(ai, isNeg, M):
    # keep in mind that negative coefficients require
    # pxi to be negated as well in here
    ai = str("{0:b}".format(ai))
    result = []
    for i in range(0, M):
        if len(ai) - 1 >= i :
            if int(ai[i]) == 1:
                # k E Ba(i)
                # (-pk(i) - pxi) * (pk(i) + pxi)
                if isNeg :
                    result.append([-1*getUniqueID(), -1*getUniqueID()])
                    result.append([getUniqueID(), getUniqueID()])
                else:
                    # (-pk(i) + pxi) * (pk(i) - pxi)
                    result.append([-1*getUniqueID(), getUniqueID()])
                    result.append([getUniqueID(), -1*getUniqueID()])
            else:
                # k E/ Ba(i)
                # -pk(i)
                result.append(-1*getUniqueID())
        else:
            # k E/ Ba(i)
            # -pk(i)
            result.append(-1*getUniqueID())
    return result

def calculateILeftSide(a, x, M):
    resetUniqueIDSeeder()
    return transAiXi(range(0, len(a)), a, x, M)

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
        M = int(round(calculateM(a)))

        iLeftSide = calculateILeftSide(a,x, M)
        iRightSide = calculateIRightSide(b, M)

        print("Left side : ")
        print(iLeftSide)

        print("Right side : ")
        print(iRightSide)
