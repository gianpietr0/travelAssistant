"""
File contenente la definizione e l'implementazione della classe ModelPrediction,
la quale si occupa della gestione del modello di predizione per l'apprendimento supervisionato.
"""

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import f1_score, precision_score, recall_score
import pandas as pd
import joblib

class ModelPrediciton:
    """
    Metodo costruttore della classe.
    
    :param data: dati di input del modello di previsione.
    :param target: dati che rappresentano il target (obiettivo) della previsione.
    """
    def __init__(self, data: pd.DataFrame, target: pd.DataFrame) -> None:
        self.data = data
        self.target = target
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(data, target,
                                                                                test_size = 0.20,
                                                                                random_state = 23,
                                                                                stratify = target)
        self.best_model = None
    

    """
    Metodo che effettua l'addestramento di un modello di previsione e trova il modello migliore
    in base alla metrica di MSE.
    """
    def trainModel(self) -> None:
        models = {
            'Decision_Tree' : (DecisionTreeClassifier(),
                              {'max_depth': [None, 10, 20, 30]}),
            'Random_Forest' : (RandomForestClassifier(),
                               {'n_estimators': [10, 50, 100]}),
            #'SVM' : (SVC(),
             #        {'C': [0.1, 1, 10],
            #          'kernel': ['linear', 'rbf']}),
            'Gradient_Boosting' : (GradientBoostingClassifier(),
                                   {'n_estimators': [10, 50, 100]}),
            'K-Nearest_Neighbors': (KNeighborsClassifier(),
                                    {'n_neighbors': [3, 5, 7]}),
            'Neural_Network' : (MLPClassifier(early_stopping = True), {
                                'hidden_layer_sizes': [(50,), (100, 50), (100, 100)],
                                'activation': ['relu', 'tanh'],
                                'alpha': [0.0001, 0.001, 0.01],
                                'max_iter': [300]}),
            'Gaussian_Naive_Bayes' : (GaussianNB(), {})
            }
        bestModels = {}
        #cerchiamo la configurazione ottimale per ogni modello considerato
        for modelName, (model, paramGrid) in models.items():
            print(f'Trying model {modelName}...', end = ' ')
            gridSearch = GridSearchCV(model, paramGrid,
                                      cv = 10,
                                      scoring = 'f1_weighted')

            gridSearch.fit(self.X_train, self.y_train)
            print('Done.')
            bestModels[modelName] = gridSearch.best_estimator_
        #valutiamo i miglori modelli addestrati
        for modelName, model in bestModels.items():
            prediction = model.predict(self.X_test)
            precision = precision_score(self.y_test, prediction, average = 'weighted')
            recall = recall_score(self.y_test, prediction, average = 'weighted')
            f1 = f1_score(self.y_test, prediction, average = 'weighted')
            print(f'Risultati modello {modelName}:')
            print(f'Precision: {precision:.5f}')
            print(f'Recall: {recall:.5f}')
            print(f'F1: {f1:.5f}')
        bestModelName = max(bestModels, key = lambda x : f1_score(self.y_test, bestModels[x].predict(self.X_test), average = 'weighted'))
        bestModel = bestModels[bestModelName]
        print(f'Il miglor modello è {bestModelName}')
        #saving the best model
        print('Saving best model...', end = ' ')
        joblib.dump(bestModel, f'../models/{bestModelName}.pkl')
        print('Done.')



"""
Codice modelli di regressione:
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import Lasso, Ridge, LinearRegression, BayesianRidge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor

models = {
    'Linear Regression': (LinearRegression(), {}),
    'Lasso Regression': (Lasso(), {
        'alpha' : [0.1, 0.5, 1.0]
    }),
    'Ridge Regression': (Ridge(), {
        'alpha': [0.1, 0.5, 1.0]
    }),
    'K-Nearest Neighbors': (KNeighborsRegressor(), {
        'n_neighbors': [3, 5, 7],
        'weights': ['uniform', 'distance']
    }),
    'Neural Network': (MLPRegressor(max_iter = 1000, early_stopping = True), {
        'hidden_layer_sizes': [(50,), (100, 50), (100, 100)],
        'activation' : ['relu', 'tanh'],
        'alpha' : [0.0001, 0.001, 0.01]
    }),
    'Decision Tree': (DecisionTreeRegressor(), {
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }),
    'Random Forest': (RandomForestRegressor(), {
        'n_estimators' : [10, 20, 30],
        'max_depth' : [None, 10, 20],
        'min_samples_split' : [2, 5, 10],
        'min_samples_leaf' : [1, 2, 4]
    }),
    #'Support Vector Regression' : (SVR(), {
    #    'C': [0.1, 1, 10],
    #    'kernel' : ['linear', 'rbf']
    #}),
    'Gradient Boosting': (GradientBoostingRegressor(), {
        'n_estimators': [10, 20, 30],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 4, 5]
    }),
    'Bayesian Regression': (BayesianRidge(), {})
}
for name, (model, param_grid) in models.items():
    print(f'Trying with model {name}...', end = ' ')
    if param_grid:
        grid_search = GridSearchCV(model, param_grid, scoring = 'neg_mean_squared_error', cv = 10)
        grid_search.fit(self.X_train, self.y_train)
        model = grid_search.best_estimator_
    model.fit(self.X_train, self.y_train)
    predictions = model.predict(self.X_test)
    print('Done.')
    mse = mean_squared_error(self.y_test, predictions)
    r2 = r2_score(self.y_test, predictions)
    print(f'Risultati ottenuti con {name}:\nMSE: {mse}\nR2: {r2}')
    if mse < self.best_score:
        self.best_score = mse
        self.best_model = model
        self.best_model_name = name
        print(f'Found new best model: {name}')
"""
