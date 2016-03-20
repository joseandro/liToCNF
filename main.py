import iGen
import iNorm
import linearT
import pycosat
import time
import sValidator
import pylab

def getNumOfVars(iq):
    vars = []

    # List flatenning
    for i, valI in enumerate(iq):
        for j, valJ in enumerate(valI):
            if (valJ < 0):
                valJ *= -1
            vars.append(valJ)

    # Remove all duplicates from vars and return len
    return len(list(set(vars)))

def main():
    # inequations = iGen.getRandomInequations(20000, 3 , 1000)
    # inequations1 = [{ "a": [300,
    #                        300,
    #                        285,
    #                        285,
    #                        265,
    #                        265,
    #                        230,
    #                        230,
    #                        190,
    #                        200,
    #                        400,
    #                        200,
    #                        400,
    #                        200,
    #                        400,
    #                        200,
    #                        400,
    #                        200,
    #                        400],
    #                  "s" : 0,
    #                  "b" : 2700}]
    # inequations2 = [{ "a": [2,4,5],
    #                  "s" : 0,
    #                  "b" : 6}]
    # inequations3 = [{ "a": [2,2],
    #                  "s" : 0,
    #                  "b" : 2}]
    # # iNorm.normalize(inequations1) # lists are mutable objects, normalize will change it
    # # iNorm.normalize(inequations2) # lists are mutable objects, normalize will change it
    # iNorm.normalize(inequations1) # lists are mutable objects, normalize will change it
    #
    # cnfs = linearT.transform(inequations1)
    # unsat = []
    # sat = []
    # for i in cnfs:
    #     res = pycosat.solve(i)
    #     if type(res) is list:
    #         sat.append(res)
    #     else:
    #         unsat.append(i)

    unsat = 0
    sat = 0
    diffs = []
    diffsL = []
    res = []

    _m_n = []

    for i in range(0, 30):
        N = 10
        C = 20

        for j in range(0, 20, 2):
            M = j + 2

            inequations = iGen.getRandomInequations(C, N, M)
            iNorm.normalize(inequations) # lists are mutable objects, normalize will change it

            startL = time.time()
            cnfs = linearT.transform(inequations)
            endL = time.time()

            for i in cnfs:
                start = time.time()
                res = pycosat.solve(i)
                end = time.time()

                if type(res) is list:
                    res.append(True)
                    sat += 1
                    # isSat = sValidator.isValid(i, res)
                    # if isSat == False:
                    #     print("Combination is not valid!")
                else:
                    res.append(False)
                    unsat += 1

                _m = len(i) # Number of clauses
                _n = getNumOfVars(i)

                _m_n.append(_m/_n)

                diff = end - start
                diffL = endL - startL
                diffs.append(diff)
                diffsL.append(diffL)
    print("% SAT = ", 100*sat/(sat+unsat))
    print("Average time = ", sum(diffs) / len(diffs))

    pylab.plot(_m_n, diffs)
    pylab.xlabel('m/n')
    pylab.ylabel('avg time')
    pylab.title('SAT Phase Transition', bbox={'facecolor': '0.8', 'pad': 5})
    pylab.savefig("graphs/"+str(time.time())+'.png')

    pylab.plot(_m_n, diffsL)
    pylab.xlabel('m/n')
    pylab.ylabel('avg time')
    pylab.title('Linear Transf Time', bbox={'facecolor': '0.8', 'pad': 5})
    pylab.savefig("graphs/linear_"+str(time.time())+'.png')

if __name__ == "__main__":
    main()
