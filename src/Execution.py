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
        print(nodes)
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
        results2 = None
        results3 = None
        print("Benvenuto all'interfaccia di interrogazione della Knowledge Base!")
        kb = KB("../knowledgeBase/")
        kb.runQueryMode()
        while True:
            exit = False
            print("1. Ricerca alloggio")
            print("2. Esci")
            choice = input("Scelta: ")
            if choice == '1':
                results = search_by_capacity(kb)
                results_price = search_by_budget(kb)
                common_nights = search_by_minimum_nights(kb)
                results2 = search_by_neighbourhood(kb)
                results3 = search_by_roomtype(kb)
                common_numbers = find_common_numbers(results, results_price, common_nights, results2, results3)
                run_queries_for_common_numbers(kb, common_numbers)
            elif choice == '2':
                print("Arrivederci!")
                break
            else:
                print("Scelta non valida. Scegli tra 1 e 2.")


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
                    print(f"Numero di alloggi che possono ospitare almeno {capacita} persone: {len(results)}")
                return results
            else:
                print("Inserisci un numero valido maggiore di zero.")
        except ValueError:
            print("Inserisci un numero valido.")



def search_by_neighbourhood(kb):
    global exit
    while not exit:
        opzioni = ["islington", "kensington_and_chelsea", "wandsworth", "westminster", "hammersmith_and_fulham",
                   "greenwich", "tower_hamlets", "brent", "richmond_upon_thames", "lambeth", "haringey", "southwark",
                   "barnet", "enfield", "camden", "hackney", "ealing", "croydon", "merton", "hounslow", "harrow", "newham",
                   "lewisham", "waltham_forest", "hillingdon", "bromley", "barking_and_dagenham", "kingston_upon_thames",
                   "redbridge", "city_of_london", "sutton", "bexley", "havering"]

        for i, opzione in enumerate(opzioni, start=1):
            print(f"{i}. {opzione}")
        scelta_opzione = input("Scegli un numero (1-33) (o inserisci 0 per tornare al menu principale): ")

        if scelta_opzione == '0':
            exit = True
            break

        try:
            scelta_opzione = int(scelta_opzione)
            if 1 <= scelta_opzione <= 33:
                selected_option = opzioni[scelta_opzione - 1]
                query = f"prop(X, 'neighbourhood', '{selected_option}')."
                results2 = kb.ask(query)
                if not results2:
                    print(f"Nessun alloggio trovato nel quartiere {selected_option}.")
                else:
                    print(f"Numero di alloggi che si trovano in {selected_option}: {len(results2)}")
                # Aggiungere un break qui per uscire dal ciclo dopo una selezione valida
                return results2
            else:
                print("Scelta non valida. Scegli un numero tra 1 e 33.")
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
                    print(f"Numero di alloggi con un prezzo inferiore o uguale a {budget_max}: {len(results_price)}")
                return results_price

            else:
                print("Inserisci un importo valido maggiore o uguale a zero.")
        except ValueError:
            print("Inserisci un importo valido.")



def search_by_minimum_nights(kb):
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
                    print(f"Nessun alloggio trovato nel tuo pernottamento di {nights} giorni.")
                    return set()  # Restituisci un set vuoto se non ci sono risultati
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
                    print(f"Numero di alloggi che hanno questo tipo di stanza: {selected_option}: {len(results3)}")
                    return results3
            else:
                print("Scelta non valida. Scegli un numero tra 1 e 4.")
        except ValueError:
            print("Inserisci un numero valido.")

def find_common_numbers(results,results_price,common_nights, results2, results3):
    global exit
    if not exit:
    # Estrai i numeri dopo 'X' da ciascuna lista
        numbers1 = {item['X'] for item in results}
        numbers_price = {item['X'] for item in results_price}
        numbers2 = {item['X'] for item in results2}
        numbers3 = {item['X'] for item in results3}

    # Trova l'intersezione tra le tre liste di numeri
        common_numbers = numbers1.intersection(numbers2,numbers_price,common_nights, numbers3)

    # Stampa i numeri comuni e il numero totale
        if common_numbers:
            print(f"Numero totale di numeri trovati: {len(common_numbers)}")
            return common_numbers
        else:
            print("Nessun numero comune trovato tra le liste.")

def run_queries_for_common_numbers(kb, common_numbers):
    global exit
    if not exit:
        index = 0  # Inizializza l'indice all'ID iniziale
        common_numbers_list = list(common_numbers)  # Converti il set in una lista ordinata
        while index < len(common_numbers_list):
            current_number = common_numbers_list[index]

            # Esegui le query per l'ID corrente
            query_bed = f"prop('{current_number}', 'beds', X)."
            query_price = f"prop('{current_number}', 'price', X)."
            query_neighbourhood = f"prop('{current_number}', 'neighbourhood', X)."
            query_nights = f"prop('{current_number}', 'maxNights', X)."
            result_bed = kb.ask(query_bed)
            result_price = kb.ask(query_price)
            result_neighbourhood = kb.ask(query_neighbourhood)
            result_nights = kb.ask(query_nights)
            # Stampa solo i valori dai risultati
            print("Host id", current_number)
            print("Prezzo", [item['X'] for item in result_price])
            print("Quartiere", [item['X'] for item in result_neighbourhood])
            print("Letti", [item['X'] for item in result_bed])
            print("NumeroMassimoNotti", [item['X'] for item in result_nights])
            # Chiedi all'utente se vuole passare all'ID successivo
            if index < len(common_numbers_list) - 1:
                next_input = input("Premi 'Y' per passare all'ID successivo, 'E' per uscire: ").strip().lower()
                if next_input == 'y':
                    index += 1
                elif next_input == 'e':
                    break
                else:
                    print("Input non valido. Continua con l'ID corrente.")
