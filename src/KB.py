"""
Classe che contiene la definizione e implementazione della classe KB, la quale si occupa 
della realizzazione e della manipolazione di una Knowledge Base.
"""

from pyswip import Prolog
import pandas as pd
from tqdm import tqdm


class KB:
   """
   Metodo costruttore della classe.

   :param path: percorso in cui creare/si trova il file che rappresenta la base di conoscenza.
   """
   def __init__(self, path: str) -> None:
     self.prolog = Prolog()
     self.housing = f'{path}housingFacts.pl'       #nome del file rappresentante la KB circa gli alloggi
     self.turism = f'{path}turismFacts.pl'         #nome del file rappresentante la KB circa le attrazioni turistiche

   

   """
   Metodo che permette di scrivere i fatti sulla KB circa gli alloggi a partire dai dati letti dal dataset di riferimento.

   :param listings: dataset da leggere e da cui acquisire i fatti relativi agli alloggi per la KB.
   """
   def createFactsListings(self, listings: pd.DataFrame) -> None:
     facts = [':- discontiguous prop/3.\n']
       #rappresentazione individui (quartieri)
     for item in listings['Neighbourhood'].unique():
        facts.append(f'neighbourhood({item}).\n')
       #rappresentazione relazioni quartieri
     facts.append("luxuryNeighbourhood('kensington_and_chelsea').\n")
     facts.append("luxuryNeighbourhood('westminster').\n")
     facts.append("luxuryNeighbourhood('city_of_london').\n")
     facts.append("luxuryNeighbourhood('hammersmith_and_fulham').\n")
     facts.append("luxuryNeighbourhood('richmond_upon_thames').\n")
     facts.append("luxuryNeighbourhood('islington').\n")
     facts.append("luxuryNeighbourhood('southwark').\n")
     
     facts.append("turisticNeighbourhood('westminster').\n")
     facts.append("turisticNeighbourhood('camden').\n")
     facts.append("turisticNeighbourhood('southwark').\n")
     facts.append("turisticNeighbourhood('greenwich').\n")
     facts.append("turisticNeighbourhood('city_of_london').\n")
     facts.append("turisticNeighbourhood('lambeth').\n")
     facts.append("turisticNeighbourhood('kensington_and_chelsea').\n")
     facts.append("turisticNeighbourhood('richmond_upon_thames').\n")
     for i, item in tqdm(listings.iterrows(), total = len(listings), desc = 'Creating facts housing'):
         #rappresentazione individui(alloggi - host)
          facts.append(f"housing('{item.iloc[0]}').\n")    #alloggio
          facts.append(f"host('{item.iloc[1]}').\n")    #host
           #rappresentazione relazioni (proprietà alloggi)
          facts.append(f"prop('{item.iloc[0]}','neighbourhood','{item.iloc[6]}').\n") #quartiere alloggio
          facts.append(f"prop('{item.iloc[0]}','price',{item.iloc[11]}).\n") #prezzo notte
          facts.append(f"prop('{item.iloc[0]}','roomType','{item.iloc[9]}').\n") #tipo alloggio
          facts.append(f"prop('{item.iloc[0]}','latitude',{item.iloc[7]}).\n") #latitudine alloggio
          facts.append(f"prop('{item.iloc[0]}','longitude',{item.iloc[8]}).\n") #longitudine alloggio
          facts.append(f"prop('{item.iloc[0]}','host','{item.iloc[1]}').\n") #host dell' alloggio
          facts.append(f"prop('{item.iloc[0]}','minNights',{item.iloc[12]}).\n") #numero minimo delle notti di un alloggio
          facts.append(f"prop('{item.iloc[0]}','maxNights',{item.iloc[13]}).\n") #numero massimo delle notti di un alloggio
          facts.append(f"prop('{item.iloc[0]}','bedrooms',{item.iloc[18]}).\n")       #numero camere da lette nell'alloggio
          facts.append(f"prop('{item.iloc[0]}','beds',{item.iloc[19]}).\n") #numero letti nell'alloggio
          facts.append(f"prop('{item.iloc[0]}','bath',{item.iloc[21]}).\n") #numero bagni nell'alloggio
          if bool(item.iloc[22]):
             facts.append(f"sharedBath('{item.iloc[0]}').\n")  #alloggio contiene bagno condiviso
          if bool(item.iloc[23]):
             facts.append(f"hasWifi('{item.iloc[0]}').\n")  #alloggio contiene wifi
          if bool(item.iloc[24]):
             facts.append(f"hasheating('{item.iloc[0]}').\n")  #alloggio contiene riscaldamento
          if bool(item.iloc[25]):
             facts.append(f"hasKitchen('{item.iloc[0]}').\n")  #alloggio contiene cucina
          if bool(item.iloc[26]):
             facts.append(f"hasAlarm('{item.iloc[0]}').\n")  #alloggio contiene allarme di monossido di carbonio
          if bool(item.iloc[27]):
             facts.append(f"allowPets('{item.iloc[0]}').\n")  #alloggio consente ingresso animali
          if bool(item.iloc[28]):
             facts.append(f"hasTV('{item.iloc[0]}').\n")  #alloggio contiene TV
          if bool(item.iloc[29]):
             facts.append(f"hasRefrigerator('{item.iloc[0]}').\n")  #alloggio contienefrigorifero
          if bool(item.iloc[22]):
             facts.append(f"hasElevator('{item.iloc[0]}').\n")  #alloggio ascensore
          if bool(item.iloc[22]):
             facts.append(f"hasAirConditioning('{item.iloc[0]}').\n")  #alloggio contiene aria condizionata
          if bool(item.iloc[22]):
             facts.append(f"hasParking('{item.iloc[0]}').\n")  #alloggio contiene parcheggio
     with open(self.housing, 'w') as file:
        file.writelines(sorted(facts))
     print('Fatcs of housing created and saved.')


   """
   Metodo che permette di scrivere dei fatti sulla KB circa le attrazioni turistiche acquisendo i dati
   dal dataset di riferimento.

   :param turism: dataset contenente le informazioni circa le attrazioni turistiche della citta.
   """
   def createFactsTurism(self, turism: pd.DataFrame) -> None:
     facts = []
     for i, item in tqdm(turism.iterrows(), total = len(turism), desc = 'Creating facts turism'):
        #rappresentazione individui
        facts.append(f"attraction('{item.iloc[0]}').\n")
        #rappresentazioni relazioni
        facts.append(f"prop('{item.iloc[0]}','latitude',{item.iloc[1]}).\n")
        facts.append(f"prop('{item.iloc[0]}','longitude',{item.iloc[2]}).\n")
        facts.append(f"prop('{item.iloc[0]}','neighbourhood','{item.iloc[3]}').\n")
     with open(self.turism, 'w') as file:
        file.writelines(sorted(facts))
     print('Facts of turistic attractions created and saved.')
   
   """
   Metodo che permette di interagire con la KB permettendo di formulare delle query da porre al sistema.

   :param query: query che viene posta sulla KB.
   :return: lista contenente i risultati della query.
   """
   def ask(self, query: str) -> list:
      try:
         print('Running query mode...', end = ' ')
         self.prolog.consult('../knowledgeBase.')
         print('Ready.')
         results = list(self.prolog.query(query))
         print('Query completed.')
         return results
      except:
         print('Error. Query invalid.')