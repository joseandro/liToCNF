# This module transforms inequations to CNF in linear time
# Author: Joseandro Luiz
# Based on JP Warners' paper on linear transformation

import numpy as np

global_index = 0
arr_pk_u = []
arr_pk_v = []
arr_pk_w = []
arr_ck_p = []
px = []
a  = {}

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

def populateControls(I):
    global arr_pk_u, arr_pk_v, arr_pk_w, arr_ck_p, a
    resetUniqueIdSeeder()

    arr_pk_u = []
    arr_pk_v = []
    arr_pk_w = []
    arr_ck_p = []
    a  = {}
    M = len(I)+1

    # We split it this way so that these lists will contain continuous
    # intervals.
    for i in range(0, M):
        arr_pk_u.append(getUniqueId())

    for i in range(0, M):
        arr_pk_v.append(getUniqueId())

    for i in range(0, M):
        arr_pk_w.append(getUniqueId())

    for i in range(0, M):
        arr_ck_p.append(getUniqueId())

def transAiAndDoTransMult(ai, isNeg, M):
    global a

    # keep in mind that negative coefficients require
    # pxi to be negated as well in here
    ai = str("{0:b}".format(ai))
    pxi = getUniqueId()
    result = []

    isRepeated = False

    # We reuse coefficients that were already calculated
    if a.get(ai) is None:
        a[ai] = []
    else:
        isRepeated = True
    
    # Formula 16
    for i in range(0, M): # loop from 0 up to M-1, inclusive
        pki = None
        if isRepeated == True:
            pki = a.get(ai)[i]
        else:
            pki = getUniqueId()
            a.get(ai).append(pki)

        if len(ai) - 1 >= i :
            if int(ai[i]) == 1:
                # propositions pk(i), k E Bai can be eliminated by substituting them by pxi
                # k E Ba(i)
                # (-pk(i) - pxi) * (pk(i) + pxi)
                if isNeg :
                    result.append([-1 * pki, -1 * pxi])
                    result.append([pki, pxi])
                else:
                    # (-pk(i) + pxi) * (pk(i) - pxi)
                    result.append([-1 * pki, pxi])
                    result.append([pki, -1 * pxi])
            else:
                # k E/ Ba(i)
                # -pk(i)
                result.append([-1 * pki])
        else:
            # k E/ Ba(i)
            # -pk(i)
            result.append([-1 * pki])

    return result


def calculateM(_arr):
    arr =  sorted(_arr)
    aMax = arr[-1]

    if aMax == 0:
        return 1

    return 1 + int(np.floor(np.log2(aMax)))

def transAiXi(U, a, x, M): 
    if len(U) == 1:
        return transAiAndDoTransMult(a[U[0]], U[0] in x, M)

    _ = splitArray(U)
    V = _['floor']
    W = _['ceiling']
    
    M_U = calculateM(U) + int(np.floor(np.log2(len(U))))
    return transAiXi(V, a, x, M) + transAiXi(W, a, x, M) + transPlus(U, V, W, M_U)


def transPlus(U, V, W, M):
    global arr_pk_u, arr_pk_v, arr_pk_w, arr_ck_p
    result = []
    
    # Formula 11
    result.append([arr_pk_u[0], arr_pk_v[0],-1*arr_pk_w[0]])
    result.append([arr_pk_u[0], -1*arr_pk_v[0], arr_pk_w[0]])

    ck_plus = arr_ck_p[0]
    
    # Formula 12
    result.append([ck_plus, -1*arr_pk_v[0], -1*arr_pk_w[0]])

    for i in range(1, M+1): #loops from 0 up to M, inclusive
        pk_u = arr_pk_u[i]
        pk_v = arr_pk_v[i]
        pk_w = arr_pk_w[i]
        
        ck_minus = ck_plus
        ck_plus = arr_ck_p[i]

        if i == M - 1 and M % 2 == 1:
            pk_w = None

        if pk_w is None:
            # Formula 13
            result.append([pk_u, -1*pk_v, ck_minus])
            result.append([pk_u, -1*pk_v, -1*ck_minus])
            result.append([pk_u, pk_v, ck_minus])
            result.append([pk_u, pk_v, -1*ck_minus])
            
            # Formula 14 will never be executed here
        else :
            # Formula 13
            result.append([pk_u, -1*pk_v, pk_w, ck_minus])
            result.append([pk_u, -1*pk_v, -1*pk_w, -1*ck_minus])
            result.append([pk_u, pk_v, -1*pk_w, ck_minus])
            result.append([pk_u, pk_v, pk_w, -1*ck_minus])

            # Formula 14
            if (i < M - 1):
                result.append([ck_plus, -1*pk_v, -1*pk_w])
                result.append([ck_plus, -1*pk_v, -1*ck_minus])
                result.append([ck_plus, -1*pk_w, -1*ck_minus])
    return result

def calculateILeftSide(a, x):
    M = calculateM(a)
    populateControls(range(0, len(a)))
    left = transAiXi(range(0, len(a)), a, x, M)

    return left


def calculateIRightSide(b):
    M = calculateM([b])

    b = str("{0:b}".format(b))
    result = []
    p = []

    for k in range(0, M+1):
        p.append(getUniqueId())

    for k in range(0, M+1):
        clause = []
        if (len(b) -1 >= k and int(b[k]) == 0) or (len(b) -1 < k):
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

        iLeftSide = calculateILeftSide(a, x)
        iRightSide = calculateIRightSide(b)

        result.append(iLeftSide+iRightSide) # Concatenate both lists containing CNFs only data
        # print("Total number of clauses = ", len(iLeftSide+iRightSide))
    return result