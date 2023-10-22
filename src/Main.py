"""
File contenente la definizione e implementazione del Main del programma.
"""

from Dataset import Dataset

class Main:
    """
    Main del sistema.
    """
    def main():
        dataset = Dataset('../dataset/datasetListings.csv')
        dataset.preprocessData()
        dataset.save('../dataset/')
        


if __name__ == '__main__':
    Main.main()
