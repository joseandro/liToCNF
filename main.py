import iGen
import iNorm
import linearT

def main():
    inequations = iGen.getRandomInequations(10, 5, 13)
    iNorm.normalize(inequations) # lists are mutable objects, normalize will change it

    linearT.transform(inequations)


if __name__ == "__main__":
    main()
