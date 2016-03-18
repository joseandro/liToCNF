import iGen
import iNorm
import linearT

def main():
    inequations = iGen.getRandomInequations(100, 3, 20)
    iNorm.normalize(inequations) # lists are mutable objects, normalize will change it

    linearT.transform(inequations)


if __name__ == "__main__":
    main()
