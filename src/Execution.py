"""
File contenente la definizione della classe Execution
che rappresenta i due possibili flussi di esecuzione
del programma (admin o user).
"""
from Dataset import Dataset
from KB import KB
from ModelPrediction import ModelPrediciton
from lib.learnProblem import Data_from_file
from lib.learnKMeans import K_means_learner
from  lib.searchProblem import Search_problem_from_explicit_graph, Path, Arc
from lib.searchGeneric import AStarSearcher
from lib.searchMPP import SearcherMPP
import copy
import re
import time
import matplotlib.pyplot as plt
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np


class Execution():
    """
    Metodo che esegue tutte le varie attività relative all'aspetto 
    'admin'.
    """
    def runAdmin():
        #processing dataset and creating KB
        print('Reading dataset housings...', end = ' ')
        housing = Dataset('../dataset/datasetListings.csv')
        print('Read dataset of Housings.')
        housing.preprocessData()
        housing.save('../dataset/')
        print('Reading dataset of turism attractions...', end = ' ')
        turism = Dataset('../dataset/turisticPoint.csv')
        print('Read dataset of turistic attractions.')
        print('Reading dataset of availability...', end = ' ')
        calendar = Dataset('../dataset/calendar.csv')
        print('Read dataset of availability.')
        calendar.extractDate()
        print('Reading dataset of transports...', end = ' ')
        stations = Dataset('../dataset/stations.csv')
        lines = Dataset('../dataset/lines.csv')
        connections = Dataset('../dataset/connections.csv')
        print('Done.')
        kb = KB('../knowledgeBase/')
        kb.createfacts(housing.getData(), turism.getData(), calendar.getData(), stations.getData(), lines.getData(), connections.getData())
        housing.addInformationsFromKB(kb)
        housing.save('../dataset/')
        
        #unsupervised learning
        housingCluster = copy.deepcopy(housing)
        housingCluster.processClustering()
        housingCluster.save('../dataset/')
        Execution.runClustering(housingCluster, housing)

        
        #supervised learning
        housing.processLearning()
        housing.save('../dataset/')
        model = ModelPrediciton(housing.getInputData(), housing.getTarget())
        model.trainModel()

        #search problem 
        stations = kb.ask('station(X).')
        nodes = []
        arcs = []
        for item in stations:
            nodes.append(item['X'])
        results = kb.ask('connection(Station1, Station2, _).')
        for item in results:
            match1 = re.search(r'\d+', item['Station2'])
            match2 = re.search(r'\d+', item['Station1'])
            station1 = int(match1.group())
            station2 = int(match2.group())
            distance = kb.ask(f'distance(station({station1}), station({station2}), D).')
            arcs.append(Arc(station1, station2, distance[0]['D']))
        hmap = {}   #euristica
        for item in nodes:
            results = kb.ask(f'distance(station(183), station({item}), D).')    #distanza verso un obiettivo fittizio
            heuristic = results[0]['D']
            hmap[item] = heuristic
        problemSize = [2,6,8,14,21,23]  #dimensione dei problemi di esperimento
        timeAlgorithm1 = [] #lista del tempo impiegato nei vari algoritmi
        timeAlgorithm2 = []

        #attempt 1
        problem = Search_problem_from_explicit_graph("Find railway path",
                                                     nodes = nodes,
                                                     arcs = arcs,
                                                     start = 42,
                                                     goals = {183}
                                                     )
        problemHeuristic = Search_problem_from_explicit_graph("Find railway path",
                                                     nodes = nodes,
                                                     arcs = arcs,
                                                     start = 42,
                                                     goals = {183},
                                                     hmap = hmap
                                                     )
        startTime = time.perf_counter()
        searcher = SearcherMPP(problem)
        solutionPath = searcher.search()
        endTime = time.perf_counter()
        elapsedTime = (endTime - startTime)
        timeAlgorithm1.append(elapsedTime)
        #problem.setSolution(solutionPath)
        #problem.show()
        if solutionPath:
            print('Solution path: ', solutionPath)
            print(f'Tempo di ricerca : {elapsedTime} secondi.')
        else:
            print('Nessuna soluzione trovata.')
        #heuristic
        startTime = time.perf_counter()
        searcher = SearcherMPP(problemHeuristic)
        solutionPath = searcher.search()
        endTime = time.perf_counter()
        elapsedTime = (endTime - startTime)
        timeAlgorithm2.append(elapsedTime)
        #problem.setSolution(solutionPath)
        #problem.show()
        if solutionPath:
            print('Solution path: ', solutionPath)
            print(f'Tempo di ricerca con euristica : {elapsedTime} secondi.')
        else:
            print('Nessuna soluzione trovata.')
        
        

        #attempt 2
        problem = Search_problem_from_explicit_graph("Find railway path",
                                                     nodes = nodes,
                                                     arcs = arcs,
                                                     start = 233,
                                                     goals = {183}
                                                     )
        problemHeuristic = Search_problem_from_explicit_graph("Find railway path",
                                                     nodes = nodes,
                                                     arcs = arcs,
                                                     start = 233,
                                                     goals = {183},
                                                     hmap = hmap
                                                     )
        startTime = time.perf_counter()
        searcher = SearcherMPP(problem)
        solutionPath = searcher.search()
        endTime = time.perf_counter()
        elapsedTime = (endTime - startTime)
        timeAlgorithm1.append(elapsedTime)
        #problem.setSolution(solutionPath)
        #problem.show()
        if solutionPath:
            print('Solution path: ', solutionPath)
            print(f'Tempo di ricerca : {elapsedTime} secondi.')
        else:
            print('Nessuna soluzione trovata.')
        #heuristic
        startTime = time.perf_counter()
        searcher = SearcherMPP(problemHeuristic)
        solutionPath = searcher.search()
        endTime = time.perf_counter()
        elapsedTime = (endTime - startTime)
        timeAlgorithm2.append(elapsedTime)
        #problem.setSolution(solutionPath)
        #problem.show()
        if solutionPath:
            print('Solution path: ', solutionPath)
            print(f'Tempo di ricerca con euristica : {elapsedTime} secondi.')
        else:
            print('Nessuna soluzione trovata.')
        
        
        #attempt 3
        problem = Search_problem_from_explicit_graph("Find railway path",
                                                     nodes = nodes,
                                                     arcs = arcs,
                                                     start = 285,
                                                     goals = {183}
                                                     )
        problemHeuristic = Search_problem_from_explicit_graph("Find railway path",
                                                     nodes = nodes,
                                                     arcs = arcs,
                                                     start = 285,
                                                     goals = {183},
                                                     hmap = hmap
                                                     )
        startTime = time.perf_counter()
        searcher = SearcherMPP(problem)
        solutionPath = searcher.search()
        endTime = time.perf_counter()
        elapsedTime = (endTime - startTime)
        timeAlgorithm1.append(elapsedTime)
        #problem.setSolution(solutionPath)
        #problem.show()
        if solutionPath:
            print('Solution path: ', solutionPath)
            print(f'Tempo di ricerca : {elapsedTime} secondi.')
        else:
            print('Nessuna soluzione trovata.')
        #heuristic
        startTime = time.perf_counter()
        searcher = SearcherMPP(problemHeuristic)
        solutionPath = searcher.search()
        endTime = time.perf_counter()
        elapsedTime = (endTime - startTime)
        timeAlgorithm2.append(elapsedTime)
        #problem.setSolution(solutionPath)
        #problem.show()
        if solutionPath:
            print('Solution path: ', solutionPath)
            print(f'Tempo di ricerca con euristica : {elapsedTime} secondi.')
        else:
            print('Nessuna soluzione trovata.')
        
        #attempt 4
        problem = Search_problem_from_explicit_graph("Find railway path",
                                                     nodes = nodes,
                                                     arcs = arcs,
                                                     start = 123,
                                                     goals = {183}
                                                     )
        problemHeuristic = Search_problem_from_explicit_graph("Find railway path",
                                                     nodes = nodes,
                                                     arcs = arcs,
                                                     start = 123,
                                                     goals = {183},
                                                     hmap = hmap
                                                     )
        startTime = time.perf_counter()
        searcher = SearcherMPP(problem)
        solutionPath = searcher.search()
        endTime = time.perf_counter()
        elapsedTime = (endTime - startTime)
        timeAlgorithm1.append(elapsedTime)
        #problem.setSolution(solutionPath)
        #problem.show()
        if solutionPath:
            print('Solution path: ', solutionPath)
            print(f'Tempo di ricerca : {elapsedTime} secondi.')
        else:
            print('Nessuna soluzione trovata.')
        #heuristic
        startTime = time.perf_counter()
        searcher = SearcherMPP(problemHeuristic)
        solutionPath = searcher.search()
        endTime = time.perf_counter()
        elapsedTime = (endTime - startTime)
        timeAlgorithm2.append(elapsedTime)
        #problem.setSolution(solutionPath)
        #problem.show()
        if solutionPath:
            print('Solution path: ', solutionPath)
            print(f'Tempo di ricerca con euristica : {elapsedTime} secondi.')
        else:
            print('Nessuna soluzione trovata.')
        
        #attempt 5
        problem = Search_problem_from_explicit_graph("Find railway path",
                                                     nodes = nodes,
                                                     arcs = arcs,
                                                     start = 300,
                                                     goals = {183}
                                                     )
        problemHeuristic = Search_problem_from_explicit_graph("Find railway path",
                                                     nodes = nodes,
                                                     arcs = arcs,
                                                     start = 300,
                                                     goals = {183},
                                                     hmap = hmap
                                                     )
        startTime = time.perf_counter()
        searcher = SearcherMPP(problem)
        solutionPath = searcher.search()
        endTime = time.perf_counter()
        elapsedTime = (endTime - startTime)
        timeAlgorithm1.append(elapsedTime)
        #problem.setSolution(solutionPath)
        #problem.show()
        if solutionPath:
            print('Solution path: ', solutionPath)
            print(f'Tempo di ricerca : {elapsedTime} secondi.')
        else:
            print('Nessuna soluzione trovata.')
        #heuristic
        startTime = time.perf_counter()
        searcher = SearcherMPP(problemHeuristic)
        solutionPath = searcher.search()
        endTime = time.perf_counter()
        elapsedTime = (endTime - startTime)
        timeAlgorithm2.append(elapsedTime)
        #problem.setSolution(solutionPath)
        #problem.show()
        if solutionPath:
            print('Solution path: ', solutionPath)
            print(f'Tempo di ricerca con euristica : {elapsedTime} secondi.')
        else:
            print('Nessuna soluzione trovata.')
        
        #attempt 6 
        problem = Search_problem_from_explicit_graph("Find railway path",
                                                     nodes = nodes,
                                                     arcs = arcs,
                                                     start = 302,
                                                     goals = {183}
                                                     )
        problemHeuristic = Search_problem_from_explicit_graph("Find railway path",
                                                     nodes = nodes,
                                                     arcs = arcs,
                                                     start = 302,
                                                     goals = {183},
                                                     hmap = hmap
                                                     )
        startTime = time.perf_counter()
        searcher = SearcherMPP(problem)
        solutionPath = searcher.search()
        endTime = time.perf_counter()
        elapsedTime = (endTime - startTime)
        timeAlgorithm1.append(elapsedTime)
        #problem.setSolution(solutionPath)
        #problem.show()
        if solutionPath:
            print('Solution path: ', solutionPath)
            print(f'Tempo di ricerca : {elapsedTime} secondi.')
        else:
            print('Nessuna soluzione trovata.')
        #heuristic
        startTime = time.perf_counter()
        searcher = SearcherMPP(problemHeuristic)
        solutionPath = searcher.search()
        endTime = time.perf_counter()
        elapsedTime = (endTime - startTime)
        timeAlgorithm2.append(elapsedTime)
        #problem.setSolution(solutionPath)
        #problem.show()
        if solutionPath:
            print('Solution path: ', solutionPath)
            print(f'Tempo di ricerca con euristica : {elapsedTime} secondi.')
        else:
            print('Nessuna soluzione trovata.')
        
        plt.plot(problemSize, timeAlgorithm1, label="Senza euristica")
        plt.plot(problemSize, timeAlgorithm2, label="Con euristica")
        plt.xlabel("Dimensione soluzione")
        plt.ylabel("Tempo di Esecuzione (s)")
        plt.legend()
        plt.title("Confronto del Tempo di Esecuzione tra non euristica ed euristica")
        plt.show()
        

    """
    Metodo che esegue il clustering degli alloggi.
    """    
    def runClustering(housingCluster: Dataset, housing: Dataset) -> None:
        dataset = Data_from_file(f'../dataset/{housingCluster.getNameDataset()}.csv',
                         prob_test = 0,
                         has_header= True,
                         target_index = 100)
        km = K_means_learner(dataset)
        nCluster = km.elbow_rule(15)
        facts = []
        optimalK = K_means_learner(dataset, nCluster)
        print(f'Il numero ottimale di Clusters generati è: {nCluster}')
        optimalK.learn()
        clusterAssignments = [optimalK.class_of_eg(eg) for eg in dataset.train]
        for i in range(len(dataset.train)):
            facts.append(f"prop('{housing.getData().iloc[i, 0]}', 'cluster', '{clusterAssignments[i]}').\n")
        with open('../knowledgeBase/housingFacts.pl', 'a') as file:
            file.writelines(facts)
        print('Facts of clustering saved.')
        


    """
    Metodo che esegue il programma destinato all'utente con le varie
    attività eseguibili da quest'ultimo.
    """
    def runUser():
        global exit
        results = None
        results_price = None
        common_nights = None
        results3 = None
        print("Benvenuto all'interfaccia di interrogazione della Knowledge Base!")
        kb = KB("../knowledgeBase/")
        kb.runQueryMode()
        while True:
            exit = False
            print("1. Ricerca alloggio")
            print("2. Ricerca percorso")
            print("3. Predici classe di prezzo")
            print("4. Esci")

            choice = input("Scelta: ")
            if choice == '1':
                    results = search_by_capacity(kb)
                    results_price = search_by_budget(kb)
                    common_nights = search_by_minimum_nights(kb)
                    results3 = search_by_roomtype(kb)
                    common_numbers = find_common_numbers(results, results_price, common_nights, results3)
                    if common_numbers:
                        run_queries_for_common_numbers(kb, common_numbers)
                    else:
                        exit = True
            elif choice == '2':
                print("Ricerca percorso.")    
                stations = kb.ask('station(X).')
                valuesID = []
                for item in stations:
                    id = item['X']
                    valuesID.append(id)
                    print(id, end = ' ')
                    nameStation = kb.ask(f"prop(station({item['X']}), 'name', N).")
                    print(nameStation[0]['N'])
                valid = False
                while not valid:
                    try:
                        start = int(input('Seleziona una delle stazioni sovraelencate come stazione di partenza: '))
                        goal = int(input('Seleziona una delle stazioni sovraelencate come stazione di destinazione: '))
                        if start not in valuesID:
                            print('Stazione di partenza non valida.')
                        elif goal not in valuesID:
                            print('Stazione di destinazione non valida.')
                        else:
                            valid = True
                    except:
                        print('Inserisci un valore valido.')
                searchPath(start, goal, kb)
            elif choice == '3':
                modelcomplete()
            elif choice == '4':
                print("Arrivederci!")
                break
            else:
                print("Scelta non valida. Scegli una delle opzioni indicate")


def search_by_capacity(kb):
    global exit
    while not exit:
        capacita = input("Per quante persone desideri cercare un alloggio (o inserisci 0 per tornare al menu principale)?: ")

        if capacita == '0':
            exit = True
            break
        try:
            capacita = int(capacita)
            if capacita > 0:
                query = f"prop(X, 'accommodates', {capacita})."
                results = kb.ask(query)
                if not results:
                    print("Nessun alloggio trovato per la capacità specificata.")
                else:
                    return results
            else:
                print("Inserisci un numero valido maggiore di zero.")
        except ValueError:
            print("Inserisci un numero valido.")


def search_by_budget(kb):
    global exit
    while not exit:
        budget_max = input("Qual è il tuo budget massimo? Inserisci l'importo desiderato: ")

        if budget_max == '0':
            exit = True
            break
        try:
            budget_max = int(budget_max)
            if budget_max > 0:
                query = f"prop(X, 'price', P), P =< {budget_max}."
                results_price = kb.ask(query)
                if not results_price:
                    print(f"Nessun alloggio trovato nel tuo budget massimo di {budget_max}.")
                else:
                    return results_price
            else:
                print("Inserisci un importo valido maggiore o uguale a zero.")
        except ValueError:
            print("Inserisci un importo valido.")



def search_by_minimum_nights(kb):
    global nights
    global exit
    while not exit:
        nights = input("Per quanti giorni desideri prenotare? Inserisci l'importo desiderato: ")

        if nights == '0':
            exit = True
            break

        try:
            nights = int(nights)
            if nights >= 0:
                query = f"prop(X, 'minNights', M), M =< {nights}."
                results_min_nights = kb.ask(query)
                numbers1 = {item['X'] for item in results_min_nights}

                query2 = f"prop(X, 'maxNights', N), N >= {nights}."
                results_max_nights = kb.ask(query2)
                numbers2 = {item['X'] for item in results_max_nights}

                common_nights = numbers1.intersection(numbers2)

                if not common_nights:
                    print('Non è stato trovato nessun alloggio per il numero di notti indicato.')
                else:
                    return common_nights  # Esci dal ciclo while se l'input è valido
            else:
                print("Inserisci un numero valido maggiore o uguale a zero.")
        except ValueError:
            print("Inserisci un numero valido.")




def search_by_roomtype(kb):
    global exit  # Dichiarare exit come globale all'inizio della funzione
    while not exit:
        opzioni = ["entire_home/apt", "hotel_room", "private_room", "shared_room"]
        for i, opzione in enumerate(opzioni, start=1):
            print(f"{i}. {opzione}")

        scelta_opzione = input("Scegli un numero (1-4) (o inserisci 0 per tornare al menu principale): ")

        if scelta_opzione == '0':
            exit = True  # Impostare exit su True per uscire dal ciclo
            break

        try:
            scelta_opzione = int(scelta_opzione)
            if 1 <= scelta_opzione <= 4:
                selected_option = opzioni[scelta_opzione - 1]
                query = f"prop(X, 'roomType', '{selected_option}')."
                results3 = kb.ask(query)
                if not results3:
                    print(f"Nessun alloggio trovato con questo tipo di stanza: {selected_option}.")
                else:
                    return results3
            else:
                print("Scelta non valida. Scegli un numero tra 1 e 4.")
        except ValueError:
            print("Inserisci un numero valido.")

def find_common_numbers(results,results_price,common_nights, results3):
    global exit
    while not exit:
    # Estrai i numeri dopo 'X' da ciascuna lista
        numbers1 = {item['X'] for item in results}
        numbers_price = {item['X'] for item in results_price}
        numbers3 = {item['X'] for item in results3}

    # Trova l'intersezione tra le tre liste di numeri
        common_numbers = numbers1.intersection(numbers_price,common_nights, numbers3)

    # Stampa i numeri comuni e il numero totale
        if common_numbers:
            return common_numbers
        else:
            print("Non è stato trovato nessun alloggio che soddisfa le caratteristiche richieste.")
            exit = True

def run_queries_for_common_numbers(kb, common_numbers):
    global nights
    global exit
    if not exit:
        show = True
        index = 0  # Inizializza l'indice all'ID iniziale
        common_numbers_list = list(common_numbers)  # Converti il set in una lista ordinata
        while index < len(common_numbers_list):
            current_number = common_numbers_list[index]
            if show:
            # Esegui le query per l'ID corrente
                query_bed = f"prop('{current_number}', 'beds', X)."
                query_price = f"prop('{current_number}', 'price', X)."
                query_neighbourhood = f"prop('{current_number}', 'neighbourhood', X)."
                query_nights = f"prop('{current_number}', 'maxNights', X)."
                query_sharedbath = f"sharedBath('{current_number}')."
                query_hasWifi = f"hasWifi('{current_number}')."
                query_hasheating = f"hasheating('{current_number}')."
                query_hasKitchen = f"hasKitchen('{current_number}')."
                query_hasAlarm = f"hasAlarm('{current_number}')."
                query_allowPets = f"allowPets('{current_number}')."
                query_hasTV = f"hasTV('{current_number}')."
                query_hasRefrigerator = f"hasRefrigerator('{current_number}')."
                query_hasElevator = f"hasElevator('{current_number}')."
                query_hasAirConditioning = f"hasAirConditioning('{current_number}')."
                query_hasParking = f"hasParking('{current_number}')."
                result_shared = kb.ask(query_sharedbath)
                result_sharedBath =kb.ask(query_sharedbath)
                result_hasWifi = kb.ask(query_hasWifi)
                result_hasheating = kb.ask(query_hasheating)
                result_hasKitchen = kb.ask(query_hasKitchen)
                result_hasAlarm = kb.ask(query_hasAlarm)
                result_allowPets = kb.ask(query_allowPets)
                result_hasTV = kb.ask(query_hasTV)
                result_hasRefrigerator = kb.ask(query_hasRefrigerator)
                result_hasElevator = kb.ask(query_hasElevator)
                result_hasAirConditioning = kb.ask(query_hasAirConditioning)
                result_hasParking = kb.ask(query_hasParking)
                result_bed = kb.ask(query_bed)
                result_price = kb.ask(query_price)
                result_neighbourhood = kb.ask(query_neighbourhood)
                result_nights = kb.ask(query_nights)
                # Stampa solo i valori dai risultati
                print("\nID", current_number, end = ' - ')
                print("Prezzo", result_price[0]['X'], end = ' - ')
                print("Quartiere", result_neighbourhood[0]['X'], end = ' - ')
                print("Letti", result_bed[0]['X'], end = ' - ')
                print("NumeroMassimoNotti", result_nights[0]['X'])
                #print([item['X']for item in result_cluster])
                #print(result_cluster)
                print('Servizi forniti:', end = ' ')
                if bool(result_shared)== True:
                    print("Bagno Condiviso", end = '')
                if bool(result_hasWifi)== True:
                    print(", Wifi", end = '')
                if bool(result_hasheating)== True:
                    print(", Riscaldamento", end = '')
                if bool(result_hasKitchen)== True:
                    print(", Cucina", end = '')
                if bool(result_hasAlarm)== True:
                    print(", Non si può fumare in camera", end = '')
                if bool(result_allowPets)== True:
                    print(", Animali consentiti", end = '')
                if bool(result_hasTV)== True:
                    print(", TV", end = '')
                if bool(result_hasRefrigerator)== True:
                    print(", Frigorifero", end = '')
                if bool(result_hasElevator)== True:
                    print(", Ascensore", end = '')
                if bool(result_hasAirConditioning)== True:
                    print(", Aria condizionata", end = '')
                if bool(result_hasParking)== True:
                    print(", Parcheggio privato")
                # Chiedi all'utente se vuole passare all'ID successivo
                show = False    #le informazioni dell'alloggio non vengono ristampate nuovamente
            if index < len(common_numbers_list) - 1:
                next_input = input("Premi 'Y' per passare all'ID successivo,'A'per verificare la disponibilità,'C' per mostrare come arrivare all'alloggio,'S' per mostrare alloggi simili, 'E' per uscire: ").strip().lower()
                next_input = next_input.lower()
                if next_input == 'y':
                    index += 1
                    show = True
                elif next_input == 'a':
                    try:
                        input_availabilty = input("Qual'è la data di partenza? (GG/MM/AAAA)")
                        gg, mm, aaaa = input_availabilty.split('/')  
                        result_availability = kb.ask(f"journey('{current_number}', date({gg},{mm},{aaaa}), {nights}).")
                        if bool (result_availability) == True:
                            print("L'alloggio è disponibile per le date richieste")
                        else:
                            print("L'alloggio non è disponibile per le date richieste")
                    except:
                        print('La data inserita non è nel formato crretto.')
                elif next_input == 'c':
                    start = 117 #partenza dall'aereoporto principale della città
                    results = kb.ask(f"distance('{current_number}', station(S), D).")
                    stations = []
                    distance = []
                    print(len(results))
                    for item in results:
                        stations.append(item['S'])
                        distance.append(item['D'])
                    distance = np.array(distance)
                    stations = np.array(stations)
                    minIndex = np.argmin(distance)
                    goal = int(stations[minIndex])
                    searchPath(start, goal, kb)
                elif next_input == 's':
                    results = kb.ask(f"prop('{current_number}', 'cluster', X).")
                    result_cluster = results[0]['X']
                    result_simili = kb.ask(f"prop(X,'cluster', '{result_cluster}').")
                    if result_simili:
                        common_numbers_list = []
                        for item in result_simili:
                            common_numbers_list.append(item['X'])
                        index = 0
                        show = True
                    else:
                        print("Non è stato possibile individuare degli alloggi a quello corrente.")
                elif next_input == 'e':
                    break
                else:
                    print("Input non valido. Continua con l'ID corrente.")


"""
Funzione che applica la ricerca del percorso migliore tra due stazioni ferroviarie
"""
def searchPath(startNode: int, goal: int, kb: KB) -> None:
    #creazione grafo di ricerca
    stations = kb.ask('station(X).')
    nodes = []
    arcs = []
    for item in stations:
        nodes.append(item['X'])
    results = kb.ask('connection(Station1, Station2, _).')
    for item in results:
        match1 = re.search(r'\d+', item['Station2'])
        match2 = re.search(r'\d+', item['Station1'])
        station1 = int(match1.group())
        station2 = int(match2.group())
        distance = kb.ask(f'distance(station({station1}), station({station2}), D).')
        arcs.append(Arc(station1, station2, distance[0]['D']))
    #definizione euristica
    hmap = {}   #euristica
    for item in nodes:
            results = kb.ask(f'distance(station({goal}), station({item}), D).')
            heuristic = results[0]['D']
            hmap[item] = heuristic
    problem = Search_problem_from_explicit_graph("Find railway path", 
                                                          nodes = nodes,
                                                          arcs = arcs,
                                                          start = startNode,
                                                          goals = {goal},
                                                          hmap = hmap
                                                          )
    searcher = SearcherMPP(problem)
    solutionPath = searcher.search()
    problem.setSolution(solutionPath)
    problem.show()
    firstNode = None
    nodesSolution = list(reversed(list(solutionPath.nodes())))
    for node in nodesSolution:
        secondNode = node
        name = kb.ask(f"prop(station({node}), 'name', N)")
        print(name[0]['N'], end = ' ')
        if firstNode is not None:
            line = kb.ask(f"connection(station({firstNode}), station({secondNode}), line(X))")
            print(f"(Line: {line[0]['X']})")
        firstNode = secondNode


"""
Metodo che va a fare delle predizioni con un modello addestrato precedentemente.
"""
def modelcomplete():
    with open('../models/modelPrediction.pickle', 'rb') as model_file:
        model = pickle.load(model_file)
    columns =['Accommodates', 'Bedrooms', 'Baths']
    columns2 = [ 'Shared', 'Wifi', 'Heating', 'Kitchen', 'CarbonMonoxideAlarm',
               'PetsAllowed', 'TV', 'Refrigerator', 'Elevator', 'AirConditioning', 'Parking',
               'inTuristicNeighbourhood', 'inLuxuryNeighbourhood']

    quartieri = ['Neighbourhood_barking_and_dagenham', 'Neighbourhood_barnet', 'Neighbourhood_bexley', 'Neighbourhood_brent',
                 'Neighbourhood_bromley', 'Neighbourhood_camden', 'Neighbourhood_city_of_london', 'Neighbourhood_croydon',
                 'Neighbourhood_ealing', 'Neighbourhood_enfield', 'Neighbourhood_greenwich', 'Neighbourhood_hackney',
                 'Neighbourhood_hammersmith_and_fulham', 'Neighbourhood_haringey', 'Neighbourhood_harrow', 'Neighbourhood_havering',
                 'Neighbourhood_hillingdon', 'Neighbourhood_hounslow', 'Neighbourhood_islington', 'Neighbourhood_kensington_and_chelsea',
                 'Neighbourhood_kingston_upon_thames', 'Neighbourhood_lambeth', 'Neighbourhood_lewisham', 'Neighbourhood_merton',
                 'Neighbourhood_newham', 'Neighbourhood_redbridge', 'Neighbourhood_richmond_upon_thames', 'Neighbourhood_southwark',
                 'Neighbourhood_sutton', 'Neighbourhood_tower_hamlets', 'Neighbourhood_waltham_forest', 'Neighbourhood_wandsworth',
                 'Neighbourhood_westminster']

    room_types = ['RoomType_entire_home/apt', 'RoomType_hotel_room', 'RoomType_private_room', 'RoomType_shared_room']

    new_data = {}

    for col in columns:
        valido = False
        while not valido:
            try:
                value = int(input(f"Inserisci il valore per '{col}' (Inserire un valore maggiore di 0): "))
                if value <= 0:
                    raise ValueError("Il valore deve essere maggiore di 0.")
                new_data[col] = value
                valido = True  # Esci dal ciclo se l'input è valido
            except ValueError as e:
                print(f"Input non valido: {e}")
    # Applica lo StandardScaler alle colonne specifiche
    scalingColumns = ['Accommodates', 'Bedrooms', 'Baths']
    scaler = StandardScaler()
    scaled_values = scaler.fit_transform([[new_data[col] for col in scalingColumns]])
    for col, scaled_value in zip(scalingColumns, scaled_values[0]):
        new_data[col] = scaled_value

    for col in columns2:
        valido = False
        while not valido:
            try:
                value = int(input(f"Inserisci il valore per '{col}' (Inserire 1 per sì, 0 per no): "))
                if value < 0 or value > 1:
                    raise ValueError("Il valore deve essere 0 o 1.")
                new_data[col] = value
                valido = True  # Esci dal ciclo se l'input è valido
            except ValueError as e:
                print(f"Input non valido: {e}")

    for i, quartiere in enumerate(quartieri, start=1):
        print(f"{i}. Quartiere '{quartiere}'")
    valido = False
    while not valido:
        try:
            choice_quartiere = int(input("Seleziona un quartiere (inserisci il numero): "))
            if choice_quartiere < 1 or choice_quartiere > 33:
                raise ValueError("Il valore deve essere tra 1 e 33.")

            for i, quartiere in enumerate(quartieri, start=1):
                if i == choice_quartiere:
                    new_data[quartiere] = 1
                else:
                    new_data[quartiere] = 0

            valido = True
        except ValueError as e:
            print(f"Input non valido: {e}")

    for i, room_type in enumerate(room_types, start=1):
        print(f"{i}. Room Type '{room_type}'")
    valido = False
    while not valido:
        try:
            choice_room_type = int(input("Seleziona un Room Type (inserisci il numero): "))
            if choice_room_type < 1 or choice_room_type > 4:
                raise ValueError("Il valore deve essere tra 1 e 4.")

            for i, room_type in enumerate(room_types, start=1):
                if i == choice_room_type:
                    new_data[room_type] = 1
                else:
                    new_data[room_type] = 0

            valido = True
        except ValueError as e:
            print(f"Input non valido: {e}")

    df = pd.DataFrame(data=[new_data], columns=columns + columns2 + quartieri + room_types)

    predizioni = model.predict(df)
    if predizioni == 0:
        print("Predizione classe:economic")
    elif predizioni == 1:
        print("Predizione classe:medium")
    elif predizioni == 2:
        print("Predizione classe:premium")
