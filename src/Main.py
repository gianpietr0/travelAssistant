"""
File contenente la definizione e implementazione del Main del programma.
"""

from Dataset import Dataset
from KB import KB

class Main:
    """
    Main del sistema.
    """
    def main():
        housing = Dataset('../dataset/datasetListings.csv')
        print('Read dataset of Housings.')
        housing.preprocessData()
        housing.save('../dataset/')
        turism = Dataset('../dataset/turisticPoint.csv')
        print('Read dataset of turistic attractions.')
        kb = KB('../knowledgeBase/')
        kb.createFactsListings(housing.getData())
        kb.createFactsTurism(turism.getData())
        housing.addInformationsFromKB(kb)
        housing.save('../dataset/')

if __name__ == '__main__':
    Main.main()
