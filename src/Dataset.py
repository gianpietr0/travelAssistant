"""
File contenente la definizione e implementazione della classe Dataset.
Dataset contiene i dati storici che vengono letti e definisce le varie operazioni
di manipolazione dei dati.
"""

import pandas as pd
import os
import re
from Utility import *


class Dataset:
    """
    Metodo costruttore della classe.

    :param srcPath: percorso sorgente del file csv contenente i vari dati da leggere.
    """
    def __init__(self, srcPath: str) -> None:
        try:
            self.name = os.path.basename(f'{srcPath}').split('.')[0]    #name of the dataset
            self.data = pd.read_csv(f'{srcPath}', low_memory = False)                       #data of the dataset
        except:
            raise IOError("Can't get the dataset. Path invalid or file inexistent.")


    """
    Elabora i dati del dataset facendo varie operazioni costruendo nuove colonne ed eliminando valori inutili.
    """
    def preprocessData(self) -> None:
        print('Preprocessing dataset...', end = ' ')
        self.name += 'Preprocessed'
        self.data.columns = self.data.columns.str.replace('_', ' ').str.title().str.replace(' ', '')
        "Elimino colonne inutili"
        self.data = self.data.drop("NeighbourhoodGroup",axis=1)
        self.data = self.data.drop("ReviewsPerMonth",axis=1)
        self.data = self.data.drop("NumberOfReviewsLtm",axis=1)
        self.data = self.data.drop("HostResponseTime",axis=1)
        self.data = self.data.drop("License",axis=1)

        "Creo una nuova colonna Bedrooms"
        self.data['Bedrooms'] = self.data['Name'].str.extract(r'(\d+)\s*(?:bedroom|bedrooms)', expand=False)

        "Creo una nuova colonna contenente il numero di letti"
        self.data['Beds'] = self.data['Name'].str.extract(r'(\d+)\s*(?:bed|beds)', expand=False)

        "Creo una nuova colonna contenente il numero di letti"
        pattern = r"★\s*([\d.]+)"
        self.data['Rating'] = self.data['Name'].str.extract(pattern)

        "Trasformo valori Nan dei Rating in 0"
        self.data['Rating'] = self.data['Rating'].astype('str')
        self.data['Rating'] = self.data['Rating'].replace('nan', '0.0')
        self.data['Rating'] = self.data['Rating'].astype(float)

        "Trasformo valori Nan di host response rate  in 0"
        self.data['HostResponseRate'] = self.data['HostResponseRate'].astype('str')
        self.data['HostResponseRate'] = self.data['HostResponseRate'].replace('nan', '0%')
        # Rimuovere il simbolo "%" e convertire in decimale
        self.data['HostResponseRate'] = self.data['HostResponseRate'].str.rstrip('%').astype(float) / 100

        "Trasformo valori NaN delle bedrooms in 1"
        self.data['Bedrooms'] = self.data['Bedrooms'].astype('str')
        self.data['Bedrooms'] = self.data['Bedrooms'].replace('nan', '1')
        self.data['Bedrooms'] = self.data['Bedrooms'].astype(int)

        "Creo una nuova colonna bath"
        self.data['Baths'] = self.data['Name'].apply(extract_value)

        "Trasformo valori NaN di bath in 1"
        self.data['Baths'] = self.data['Baths'].astype('str')
        self.data['Baths'] = self.data['Baths'].replace('nan', '1')
        self.data['Baths'] = self.data['Baths'].astype(float)
        self.data['Baths'] = self.data['Baths'].replace(0 , 1)

        # Applicare la funzione alla colonna "Baths" per arrotondare i valori
        self.data['Baths'] = self.data['Baths'].apply(round_baths)

        "Creo una nuova colonna shared booleana per indicare il tipo di bagno"
        self.data['Shared'] = self.data['Name'].str.contains('shared bath|shared baths')

        "Creo una nuova colonna shared booleana per indicare il wifi"
        self.data['Wifi'] = self.data['Amenities'].str.contains('Wifi')

        "Creo una nuova colonna shared booleana per indicare il riscaldamento"
        self.data['Heating']= self.data['Amenities'].str.contains('Heating')

        "Creo una nuova colonna shared booleana per indicare la cucina"
        self.data['Kitchen']= self.data['Amenities'].str.contains('Kitchen')

        "Creo una nuova colonna shared booleana per indicare se c'è un rilevatore di monossido di carbonio"
        self.data['CarbonMonoxideAlarm']= self.data['Amenities'].str.contains('Carbon monoxide alarm')

        "Creo una nuova colonna shared booleana per indicare se sono ammessi animali"
        self.data['PetsAllowed']= self.data['Amenities'].str.contains('Pets allowed')

        "Creo una nuova colonna shared booleana per indicare se c'è la TV"
        self.data['TV']= self.data['Amenities'].str.contains('TV|Tv')

        "Creo una nuova colonna shared booleana per indicare se c'è il frigo"
        self.data['Refrigerator']= self.data['Amenities'].str.contains('Refrigerator')

        "Creo una nuova colonna shared booleana per indicare se c'è l'ascensore"
        self.data['Elevator']= self.data['Amenities'].str.contains('Elevator')

        "Creo una nuova colonna shared booleana per indicare se c'è l'aria condizionata"
        self.data['AirConditioning']= self.data['Amenities'].str.contains('air conditioning')

        "Creo una nuova colonna shared booleana per indicare se c'è il parcheggio"
        self.data['Parking']= self.data['Amenities'].str.contains('parking')

        "Metto false ai valori nan della colonna HostIsSuperhost"
        self.data['HostIsSuperhost'] = self.data['HostIsSuperhost'].astype('str')
        self.data['HostIsSuperhost'] = self.data['HostIsSuperhost'].replace('nan','False')
        self.data['HostIsSuperhost'] = self.data['HostIsSuperhost'].replace('f','False')
        self.data['HostIsSuperhost'] = self.data['HostIsSuperhost'].replace('t','True')

        "Elimino le righe contenenti NaN in HostSince"
        self.data['HostSince'] = self.data['HostSince'].astype('str')
        self.data = self.data.drop(self.data[self.data['HostSince'] == 'nan'].index)

        "Elimino i valori >30 nelle NottiMax "
        self.data['MaximumNights'] = self.data['MaximumNights'].apply(lambda x: 30 if x > 30 else x)

        "Elimino le colonne inutili"
        self.data = self.data.drop('Amenities',axis=1)
        self.data = self.data.drop('Name',axis=1)
        self.data = self.data.drop('LastReview',axis=1)

        "Converto tutto in minuscolo "

        self.data = self.data.map(converti_in_minuscolo)

        ' Funzione per convertire spazi in _ '
        self.data = self.data.map(converti_spazi_in_)
        
        print('Done.')

    """
    Salva il dataset in un file CSV nel percorso specificato in input.
    
    :param dstPath: percorso di destinazione in cui viene salvato il dataset.
    """
    def save(self, dstPath: str) -> None:
        try:
            self.data.to_csv(f'{dstPath}{self.name}.csv', index = False)
            print(f"File '{self.name}' saved.")
        except:
            raise IOError('Error during saving. Path invalid.')
