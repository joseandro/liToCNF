# This module validates inequations along with their solutions
# Author: Joseandro Luiz

def isValid(cnf, res):
    """
    This function validates a CNF

    @rtype:   bool
    """
    # Turn all variables from CNF positive (we have to compare them later)
    andBoolClause = None
    for i in cnf :
        orBoolClause = None
        for j, val in enumerate(i) :
            isFound = False
            modVal = val
            orBool = None

            if modVal < 0:
                modVal *= -1
            try:
                if res.index(modVal) >= 0:
                    isFound = True
            except ValueError:
                pass

            if isFound == True:
                if j > 0:
                    orBool  = True
                else:
                    orBool  = False
            elif i[j] > 0:
                orBool  = False
            else:
                orBool  = True

            if orBoolClause == None:
                orBoolClause = orBool
            else:
                orBoolClause = orBoolClause or orBool

        if andBoolClause is None:
            andBoolClause = orBoolClause
        else:
            andBoolClause = andBoolClause and orBoolClause
    return andBoolClause