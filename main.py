import iGen
import iNorm
import linearT
import pycosat

def main():
    inequations = iGen.getRandomInequations(2000, 3000 , 10000)
    iNorm.normalize(inequations) # lists are mutable objects, normalize will change it

    cnfs = linearT.transform(inequations)
    unsat = []
    sat = []
    for i in cnfs:
        res = pycosat.solve(i)
        if type(res) is list:
            sat.append(res)
        else:
            unsat.append(i)

    print("We found ", len(sat), " SAT inequations and ", len(unsat), " UNSAT")

if __name__ == "__main__":
    main()
