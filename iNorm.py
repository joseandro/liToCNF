# This module provides means to normalize inequations
# Author: Joseandro Luiz

def normalize(iq):
    """
    This function normalizes negative coefficients in inequations.

    @type  iq: list
    @param iq: Defines a and b, where ai E [-C, +C] and b E [0, C].
    @rtype:   void
    """

    # Lets decrypt it!
    for val in iq :
        a = val['a']
        a.sort() # this will help to define the sets of MC

        s = val['s']
        b = val['b']
        x = []

        if (int(s) == 1): # In this case we must to transform the equation to <=
            for i, valA in enumerate(a):
                a[i] *= -1
            b = -1 * int(b)
            s = 0

        for i, valA in enumerate(a) :
            if valA < 0 :
                a[i] = -1*valA
                x.append(i) # store the a's indexes where coefficients are negative
                b += -1*valA

        if b < 0 :
            a = False

        val['a'] = a
        val['s'] = s
        val['b'] = b
        val['x'] = x

