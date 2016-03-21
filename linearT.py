# This module transforms inequations to CNF in linear time
# Author: Joseandro Luiz
# Based on JP Warners' paper on linear transformation

import numpy as np

global_index = 0
pk = []
px = []
ck = []

def splitArray(arr):
    ceiling = arr[:len(arr)/2]
    floor = arr[len(arr)/2:]

    return {'ceiling': ceiling, 'floor' : floor }

def getUniqueId():
    global global_index
    global_index += 1
    return global_index

def resetUniqueIdSeeder():
    global global_index
    global_index = 0

def populateControls(M):
    global pk, px, ck
    resetUniqueIdSeeder()

    pk = []
    px = []
    ck = []

    # We split it this way so that these lists will contain continuous
    # intervals.
    for i in range(0, M+1):
        px.append(getUniqueId())

    for i in range(0, M+1):
        pk.append(getUniqueId())

    for i in range(0, M+1):
        arr = []
        for j in range(0, M+1):
            arr.append(j)
        ck.append(arr)

def transAiAndDoTransMult(ai, isNeg, M):
    # keep in mind that negative coefficients require
    # pxi to be negated as well in here
    ai = str("{0:b}".format(ai))
    result = []

    global px

    # Formula 16
    for i in range(0, M+1): # loop from 0 up to M, inclusive
        if len(ai) - 1 >= i :
            if int(ai[i]) == 1:
                # propositions pk(i), k E Bai can be eliminated by substituting them by pxi

                # k E Ba(i)
                # (-pk(i) - pxi) * (pk(i) + pxi)
                if isNeg :
                    result.append([-1 * px[i], -1 * px[i]])
                    result.append([px[i], px[i]])
                else:
                    # (-pk(i) + pxi) * (pk(i) - pxi)
                    result.append([-1 * px[i], px[i]])
                    result.append([px[i], -1 * px[i]])
            else:
                # k E/ Ba(i)
                # -pk(i)
                result.append([-1 * getUniqueId()])
        else:
            # k E/ Ba(i)
            # -pk(i)
            result.append([-1 * getUniqueId()])

    return result


def calculateM(_arr):
    arr =  sorted(_arr)
    aMax = arr[-1]

    if aMax == 0:
        return 1

    return 1 + int(np.round(np.log2(aMax)))

def transAiXi(U, a, x, M):
    M_U = calculateM(U) + int(np.round(np.log2(len(U))))

    if len(U) == 1:
        return transAiAndDoTransMult(a[U[0]], U[0] in x, M_U)

    _ = splitArray(U)
    V = _['floor']
    W = _['ceiling']

    return transAiXi(V, a, x, M) + transAiXi(W, a, x, M) + transPlus(M_U)

def transPlus(M):
    result = []

    p0_U = getUniqueId()
    p0_V = getUniqueId()
    p0_W = getUniqueId()
    c01_U = getUniqueId()

    # Formula 11
    result.append([p0_U, p0_V,-1*p0_W])
    result.append([p0_U, -1*p0_V, p0_W])

    # Formula 12
    result.append([c01_U, -1*p0_V, -1*p0_W])

    for i in range(1, M+1): #loops from 0 up to M, inclusive
        pk_U = getUniqueId()
        pk_V = getUniqueId()
        pk_W = getUniqueId()
        ck_m1_k_U = getUniqueId()
        ck_k_p1_U = getUniqueId()

        # Formula 13
        result.append([pk_U, -1*pk_V, pk_W, ck_m1_k_U])
        result.append([pk_U, -1*pk_V, -1*pk_W, -1*ck_m1_k_U])
        result.append([pk_U, pk_V, -1*pk_W, ck_m1_k_U])
        result.append([pk_U, pk_V, pk_W, -1*ck_m1_k_U])

        # Formula 14
        if (i < M):
            result.append([ck_k_p1_U, -1*pk_V, -1*pk_W])
            result.append([ck_k_p1_U, -1*pk_V, -1*ck_m1_k_U])
            result.append([ck_k_p1_U, -1*pk_W, -1*ck_m1_k_U])

    return result

def calculateILeftSide(a, x, M):
    populateControls(M)
    left = transAiXi(range(0, len(a)), a, x, M)

    return left


def calculateIRightSide(b, M):
    M = calculateM([b])
    M = M + int(np.round(np.log2(M)))

    b = str("{0:b}".format(b))
    result = []
    p = []
    counter = 0

    for k in range(0, M+1):
        p.append(getUniqueId())

    for k in range(0, M+1):
        clause = []
        if (len(b) -1 >= k and int(b[k]) == 0) or (len(b) -1 < k):
            counter += 1
            clause.append(-1*p[k])
            if len(b) - 1 >= k: # we still can loop through B
                for j in range(k+1, M):
                    if len(b) -1 >= j and int(b[j]) == 1:
                        clause.append(-1*p[j])
            result.append(clause)

    return result

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
    result = []
    for v in iq :
        a = v['a']

        if a == False:
            result.append(False)
            continue # Equation is invalid

        if len(a) < 1:
            result.append(False)
            continue # Empty arrays are not allowed

        x = v['x']
        b = v['b']
        M = calculateM(a)

        iLeftSide = calculateILeftSide(a,x, M)
        iRightSide = calculateIRightSide(b, M)

        result.append(iLeftSide+iRightSide) # Concatenate both lists containing CNFs only data
        # print("Total number of clauses = ", len(iLeftSide+iRightSide))
    return result