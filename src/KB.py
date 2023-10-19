"""
Classe che contiene la definizione e implementazione della classe KB, la quale si occupa 
della realizzazione e della manipolazione di una Knowledge Base.
"""

from pyswip import Prolog
import os
import pandas as pd
from tqdm import tqdm


class KB:
    """
    Metodo costruttore della classe.

    :param path: percorso in cui creare/si trova il file che rappresenta la base di conoscenza.
    """
    def __init__(self, path: str) -> None:
        self.prolog = Prolog()
        self.fileName = f'{path}knowledgeBase.pl'       #nome del file rappresentante la KB
        if not os.path.exists(self.fileName):
            with open(self.fileName, 'w') as file:
                pass
            print('File KB created.')
    

    """
    Metodo che va a scrivere dei fatti sulla KB a partire dai dati letti dal dataset di riferimento.

    :param dataset: dataset da leggere e da cui acquisire i fatti per la KB.
    """
    def createFacts(self, dataset: pd.DataFrame) -> None:
        with open(self.fileName, 'w') as file:        #TO REVISE  Mettere A come modalità di accesso
            for i, item in tqdm(dataset.iterrows(), total = len(dataset), desc = 'Creating facts'):
                #rappresentazione individui
                file.write(f"housing({item.iloc[0]}).\n")    #alloggio
                file.write(f"host({item.iloc[1]}).\n")    #host
                #rappresentazione relazioni
                file.write(f"prop({item.iloc[0]},neighbourhood,{item.iloc[6]}).\n") #quartiere alloggio
                file.write(f"prop({item.iloc[0]},price,{item.iloc[11]}).\n") #prezzo notte
                file.write(f"prop({item.iloc[0]},roomType,{item.iloc[9]}).\n") #tipo alloggio
                file.write(f"prop({item.iloc[0]},latitude,{item.iloc[7]}).\n") #latitudine alloggio
                file.write(f"prop({item.iloc[0]},longitude,{item.iloc[8]}).\n") #longitudine alloggio
                file.write(f"prop({item.iloc[0]},host,{item.iloc[1]}).\n") #host dell' alloggio
                file.write(f"prop({item.iloc[0]},minNights,{item.iloc[12]}).\n") #numero minimo delle notti di un alloggio
                file.write(f"prop({item.iloc[0]},maxNights,{item.iloc[13]}).\n") #numero massimo delle notti di un alloggio
                file.write(f"prop({item.iloc[0]},bedrooms,{item.iloc[18]}).\n")       #numero camere da lette nell'alloggio
                file.write(f"prop({item.iloc[0]},beds,{item.iloc[19]}).\n") #numero letti nell'alloggio
                file.write(f"prop({item.iloc[0]},bath,{item.iloc[21]}).\n") #numero bagni nell'alloggio
                if bool(item.iloc[22]):
                    file.write(f"sharedBath({item.iloc[0]}).\n")  #alloggio contiene bagno condiviso
                if bool(item.iloc[23]):
                    file.write(f"hasWifi({item.iloc[0]}).\n")  #alloggio contiene wifi
                if bool(item.iloc[24]):
                    file.write(f"hasheating({item.iloc[0]}).\n")  #alloggio contiene riscaldamento
                if bool(item.iloc[25]):
                    file.write(f"hasKitchen({item.iloc[0]}).\n")  #alloggio contiene cucina
                if bool(item.iloc[26]):
                    file.write(f"hasAlarm({item.iloc[0]}).\n")  #alloggio contiene allarme di monossido di carbonio
                if bool(item.iloc[27]):
                    file.write(f"allowPets({item.iloc[0]}).\n")  #alloggio consente ingresso animali
                if bool(item.iloc[28]):
                    file.write(f"hasTV({item.iloc[0]}).\n")  #alloggio contiene TV
                if bool(item.iloc[29]):
                    file.write(f"hasRefrigerator({item.iloc[0]}).\n")  #alloggio contienefrigorifero
                if bool(item.iloc[22]):
                    file.write(f"hasElevator({item.iloc[0]}).\n")  #alloggio ascensore
                if bool(item.iloc[22]):
                    file.write(f"hasAirConditioning({item.iloc[0]}).\n")  #alloggio contiene aria condizionata
                if bool(item.iloc[22]):
                    file.write(f"hasParking({item.iloc[0]}).\n")  #alloggio contiene parcheggio
                

#test main

kb = KB('../knowledgeBase/')
data = pd.read_csv('../dataset/datasetListings.csv')
for index, col in enumerate(data.columns):
    print(index, col)
kb.createFacts(data)
