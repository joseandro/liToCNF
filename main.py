import iGen
import iNorm
import exponT

def main():
    inequations = iGen.getRandomInequations(10, 5, 3)
    iNorm.normalize(inequations) # lists are mutable objects, normalize will change it

    print(exponT.transform(inequations))

if __name__ == "__main__":
    main()
