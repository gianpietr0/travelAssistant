"""
File contenente la definizione e implementazione del Main del programma.
"""


from Execution import Execution
import sys

import pandas as pd
from ModelPrediction import ModelPrediciton
from Dataset import Dataset
from KB import KB
import seaborn as sns
import matplotlib.pyplot as plt




class Main:
    """
    Main del sistema.
    """
    def main():
        try:
            mode = sys.argv[1]
            if mode == 'admin':
                Execution.runAdmin()
            elif mode == 'user':
                Execution.runUser()
            else:
                print("Invalid run option.\nPlease use user or admin insted.")
        except:
            print('Missing run option.\nPlease use user or admin.')

if __name__ == '__main__':
    Main.main()

#data = pd.read_csv('../dataset/datasetListingsPreprocessedEncoded.csv')
#variabili = ["Accommodates", "Bedrooms", "Rating", "Baths", "Shared", "Wifi", "Heating", "Kitchen",
#             "CarbonMonoxideAlarm", "PetsAllowed", "TV", "Refrigerator", "Elevator", "AirConditioning",
#             "Parking", "inTuristicNeighbourhood", "inLuxuryNeighbourhood"]
#variabili = ['MinimumNights','MaximumNights','NumberOfReviews','CalculatedHostListingsCount','NumberOfReviewsLtm']
#
#for variabile in variabili:
#    plt.figure(figsize=(8, 6))
#    sns.boxplot(x="PriceClass", y=variabile, data=data)
#    plt.xlabel("PriceClass")
#    plt.ylabel(variabile)
#    plt.title(f"Boxplot di {variabile} rispetto a PriceClass")
#    plt.show()
#
#
## Lista delle variabili binarie per cui desideri creare i bar plot
#variabili_binarie = ["Wifi", "Heating", "Kitchen", "CarbonMonoxideAlarm", "PetsAllowed", "TV", "Refrigerator", "Elevator", "AirConditioning", "Parking", "inTuristicNeighbourhood",
#                     "inLuxuryNeighbourhood"]
#variabili_binarie = ['Neighbourhood_barking_and_dagenham','Neighbourhood_barnet','Neighbourhood_bexley','Neighbourhood_brent','Neighbourhood_bromley','Neighbourhood_camden',
#                     'Neighbourhood_city_of_london',
#                     'Neighbourhood_croydon','Neighbourhood_ealing','Neighbourhood_enfield','Neighbourhood_greenwich','Neighbourhood_hackney','Neighbourhood_hammersmith_and_fulham',
#                     'Neighbourhood_haringey','Neighbourhood_harrow','Neighbourhood_havering','Neighbourhood_hillingdon','Neighbourhood_hounslow','Neighbourhood_islington',
#                     'Neighbourhood_kensington_and_chelsea','Neighbourhood_kingston_upon_thames','Neighbourhood_lambeth','Neighbourhood_lewisham','Neighbourhood_merton',
#                     'Neighbourhood_newham','Neighbourhood_redbridge','Neighbourhood_richmond_upon_thames','Neighbourhood_southwark','Neighbourhood_sutton','Neighbourhood_tower_hamlets',
#                     'Neighbourhood_waltham_forest','Neighbourhood_wandsworth','Neighbourhood_westminster','RoomType_entire_home/apt','RoomType_hotel_room','RoomType_private_room',
#                     'RoomType_shared_room']
#for variabile in variabili_binarie:
#    plt.figure(figsize=(8, 6))
#    sns.countplot(x=variabile, hue="PriceClass", data=data)
#    plt.xlabel(variabile)
#    plt.ylabel("Conteggio")
#    plt.title(f"Grafico a barre di {variabile} rispetto a PriceClass")
#    plt.legend(title="PriceClass")
#    plt.show()