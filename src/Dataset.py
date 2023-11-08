"""
File contenente la definizione e implementazione della classe Dataset.
Dataset contiene i dati storici che vengono letti e definisce le varie operazioni
di manipolazione dei dati.
"""

import pandas as pd
import os
from Utility import *
import numpy as np
from KB import KB
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


class Dataset:
    """
    Metodo costruttore della classe.

    :param srcPath: percorso sorgente del file csv contenente i vari dati da leggere.
    """
    def __init__(self, srcPath: str) -> None:
        try:
            self.name = os.path.basename(f'{srcPath}').split('.')[0]    #name of the dataset
            self.data = pd.read_csv(f'{srcPath}', low_memory = False)   #data of the dataset
        except:
            raise IOError("Can't get the dataset. Path invalid or file inexistent.")

    """
    Metodo di accesso che restiuisce i dati che compongono il dataset.
    
    :return data: insieme di dati che compongono il dataset.
    """
    def getData(self) -> pd.DataFrame:
        return self.data


    """
    Metodo di accesso che restituisce il nome del dataset.
    """
    def getNameDataset(self) -> str:
        return self.name
    
    
    """
    Metodo che restituisce il dataset contenente le variabili indipendenti.
    """
    def getInputData(self) -> pd.DataFrame:
        return self.data.drop('PriceClass', axis = 1)


    """
    Metodo che restituisce il target del dataset.
    """
    def getTarget(self) -> pd.DataFrame:
        return self.data['PriceClass']
    

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
        #self.data = self.data.drop("NumberOfReviewsLtm",axis=1)
        self.data = self.data.drop("HostResponseTime",axis=1)
        self.data = self.data.drop("License",axis=1)

        #filtriamo le righe i cui prezzi risultano errati dall'analisi
        self.data = self.data[self.data['Price'] >= 25]
        self.data = self.data[self.data['Price'] <= 680]
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

        #risolvo conversione di accommodates nel tipo di dato desiderato (serve per convertirlo poi intero nella kb)
        self.data['Accommodates'] = self.data['Accommodates'].astype(int)
        "Trasformo valori NaN delle beds in accommodates"
        self.data['Bedrooms'] = self.data['Bedrooms'].astype('str')
        self.data['Beds'].fillna(self.data['Accommodates'], inplace=True)
        self.data['Bedrooms'] = self.data['Bedrooms'].astype(int)
        self.data['Beds'] = self.data['Beds'].astype(int)

        "Trasformo i valori di Bedrooms maggiori di Accommodates"
        self.data.loc[self.data['Bedrooms'] > self.data['Accommodates'], 'Bedrooms'] = self.data['Accommodates']
        self.data.loc[self.data['Beds'] > self.data['Accommodates'], 'Beds'] = self.data['Accommodates']

        "Elimino i valori errati di Baths"
        self.data['Baths'] = np.where(self.data['RoomType'] == 'Hotel Room', 1, self.data['Baths'])

        self.data = self.data.loc[self.data['Baths'] <= 6]

        "Converto tutto in minuscolo "

        self.data = self.data.map(converti_in_minuscolo)

        ' Funzione per convertire spazi in _ '
        self.data = self.data.map(converti_spazi_in_)

        #creazione delle classi di prezzo
        self.data['Price'] = self.data['Price'].astype(int)
        economicThreshold = 75   #i prezzi inferiori alla soglia 75 sono considerati economici 
        mediumThreshold = 205      #i prezzi compresi tra 130 e 205 sono considerati medi; i prezzi maggiori di 205 sono considerati lussuosi
        self.data['PriceClass'] = pd.cut(self.data['Price'],
                                         bins = [0, economicThreshold, mediumThreshold, self.data['Price'].max()],
                                         labels = ['Economic', 'Medium', 'Premium'])
        
        print('Done.')


    """
    Metodo che processa il dataset 'calendar' permettendo l'estrazione delle date
    in un formato utile all' elaborazione con KB.
    """
    def extractDate(self) -> None:
        print('Preprocessing availability...', end = ' ')
        self.data = self.data[self.data['available'] == 't']  #consideriamo solo i valori true
        print('Done')
        print('Extracting Date...', end = ' ')
        self.data[['Year', 'Month', 'Day']] = self.data['date'].str.split('-', expand = True)
        self.data = self.data.dropna()  #eliminiamo valori nulli presenti
        print('Done.')
    """
    Metodo che permette di aggiungere delle informazioni al dataset grazie all'utilizzo della
    KnowledgeBase (KN)
    """
    def addInformationsFromKB(self, kb: KB) -> None:
        print('Adding information from KB...')
        results = kb.ask('isInTuristNeigh(H, N)')
        turisticNeigh = [item['H'] for item in results]
        boolMap = np.isin(self.data['Id'].astype(str), turisticNeigh)
        self.data['inTuristicNeighbourhood'] = boolMap
        self.data['inTuristicNeighbourhood'] = self.data['inTuristicNeighbourhood'].astype(str)
        self.data['inTuristicNeighbourhood'] = self.data['inTuristicNeighbourhood'].str.lower()
        results = kb.ask('isInLuxuryNeigh(H, N)')
        luxuryNeigh = [item['H'] for item in results]
        boolMap = np.isin(self.data['Id'].astype(str), luxuryNeigh)
        self.data['inLuxuryNeighbourhood'] = boolMap
        self.data['inLuxuryNeighbourhood'] = self.data['inLuxuryNeighbourhood'].astype(str)
        self.data['inLuxuryNeighbourhood'] = self.data['inLuxuryNeighbourhood'].str.lower()
        print('New informations added to KB')


    """
    Metodo che va a processare i dati per poter effettuare l'apprendimento.
    Si eliminano le colonne che potrebbe non influire sulla previsione del prezzo.
    """
    def processLearning(self) -> None:
        print('Processing data for learning...', end = ' ')
        self.name += 'Encoded'
        self.data.drop(['Id', 'HostId', 'HostName', 'HostSince', 'HostResponseRate',
                        'HostIsSuperhost', 'Price', 'Availability365', 'Latitude', 'Longitude','MinimumNights',
                        'MaximumNights','NumberOfReviews','CalculatedHostListingsCount','NumberOfReviewsLtm', 'Beds', 'Rating'],
                       axis = 1,
                       inplace = True)
        #self.data.drop(["Wifi", "Heating", "Kitchen", "CarbonMonoxideAlarm", "PetsAllowed", "TV", "Refrigerator", "Elevator", "AirConditioning", "Parking",
        #                "inLuxuryNeighbourhood", "Rating", "Baths", 'Neighbourhood', 'MinimumNights','MaximumNights',
        #                'NumberOfReviews','CalculatedHostListingsCount','NumberOfReviewsLtm', 'Beds'],
        #               axis = 1,
        #               inplace = True)

        #self.data.drop('NumberOfReviews', axis = 1, inplace = True)
        #self.data.drop('CalculatedHostListingsCount', axis = 1, inplace = True)
        print('Done.')
        self.encode()
    
    """
    Metodo che va a processare i fati per effettuare il clusering.
    """
    def processClustering(self) -> None:
        print('Processing for clustering...', end = ' ')
        self.name += 'Cluster'
        self.data.drop(['Id', 'HostId', 'HostName', 'HostSince', 'HostResponseRate',
                        'HostIsSuperhost', 'Price', 'Availability365', 'Latitude', 'Longitude', 'MinimumNights',
                        'MaximumNights','NumberOfReviews','CalculatedHostListingsCount','NumberOfReviewsLtm', 'Beds'],
                       axis = 1,
                       inplace = True)
        self.data = pd.get_dummies(self.data, columns = ['Neighbourhood', 'RoomType'])
        self.data.dropna(inplace = True)
        self.data = self.data.replace({True: 1, False: 0, 'true': 1, 'false': 0, 'Economic' : 0, 'Medium' : 1, 'Premium': 2})
        scalingColumns = ['Accommodates','Bedrooms', 'Rating', 'Baths', 'PriceClass']
        scaler = StandardScaler()
        self.data[scalingColumns] = scaler.fit_transform(self.data[scalingColumns])
        print('Done.')
       
        
    """
    Metodo che va ad applicare al dataset la procedura di One-hot-encode
    per codificare le variabili discrete presenti.
    """
    def encode(self) -> None:
        print('Encoding and scaling dataset...', end = ' ')
        
        self.data = pd.get_dummies(self.data, columns = ['Neighbourhood', 'RoomType'])
        #self.data.drop(['RoomType_hotel_room','RoomType_shared_room'],
        #               axis = 1,
        #               inplace = True)
        self.data.dropna(inplace = True)
        self.data = self.data.replace({True: 1, False: 0, 'true': 1, 'false': 0, 'Economic' : 0, 'Medium' : 1, 'Premium': 2})
        scalingColumns = ['Accommodates', 'Bedrooms', 'Baths']
        scaler = StandardScaler()
        self.data[scalingColumns] = scaler.fit_transform(self.data[scalingColumns])
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
