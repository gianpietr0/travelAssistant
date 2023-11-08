# Progetto Ingegneria della conoscenza A.A. 2022-2023 :TravelAssistant

**Gruppo di lavoro:**

•	*Gianpietro Fontana, 736570, g.fontana10@studenti.uniba.it*

•	*Simone Lastilla, 717851, s.lastilla3@studenti.uniba.it*


# FASE INIZIALE


**Installare Python 3.11.5**

*https://www.python.org/downloads/release/python-3115/*

**Installare SWIProlog 8.4.2 (installare la versione a 64 bit)**

*https://www.swi-prolog.org/download/stable/bin/swipl-8.4.2-1.x64.exe.envelope*

**Clonare il repository dal prompt dei comandi:**

*git clone https://github.com/gianpietr0/travelAssistant.git*

**Creare l'ambiente virtuale:**

*cd travelAssistant*

*python -m venv travelAssistant*

**Installare le dipendenze:**

*pip install -r requirements.txt*

# Come eseguire il codice

**Scaricare dataset dai link forniti**
Per via della dimensione eccessiva per poter essere caricati su GitHub, i dataset fondamentali per l'esecuzione corretta e completa del programma sono stati caricati su una cartella condivisa su Google Drive.
Il link alla cartella è il seguente:
https://drive.google.com/drive/folders/10fW_FWgJq8uC7DeoUbCVih-eD200hcrZ?usp=sharing

**Bisogna innanzitutto recarsi nella cartella src :**

*cd src*


**Affinchè si possa utilizzare il lato utente c'è bisogno di avviare il lato admin:**

*python -u Main.py admin*


**(Durante il lato admin si avvierà il preprocessing del dataset, la creazione dei fatti della KB, apprendimento supervisionato e non, creazione e salvataggio del miglior modello di predizione ed esecuzione dei clustering. E' fondamentale pertanto che sia
eseguita prima la parte admin perchè costruisce le basi per poter utilizzare correttamente la parte user. Inoltre, nella parte admin vengono testati algoritmi con e senza euristica.)** 

<br>

**Lato Utente:**

*python -u Main.py user*


<br>

**Il lato utente permette l'utilizzo dei modelli e fatti che sono stati costruiti nel lato admin tramite interazione con interfaccia a riga di comando.**

*L'interfaccia prevede varie funzionalità come:*

*-Ricerca alloggio*

*-Ricerca percorso*

*Predizione classe di prezzo*

<br>
<br>

**Nella ricerca dell'alloggio verranno tenuti in considerazione vari fattori:**

-*numero ospiti*

-*budget*

-*numero notti*

-*tipo di stanza* 

<br>

<br>

**La ricerca del percorso permette di trovare il percorso da compiere per spostarsi da una stazione ad un'altra.**

<br>

<br>

**La predizione della classe di prezzo utilizza un modello costruito nel lato admin che consente di classificare la categoria  appartenente all'alloggio tramite l'inserimento da parte dell'utente delle varie caratteristiche dell'abitazione.**

**Questa funzione permette ad un ipotetico venditore di poter comprendere sia il tipo di alloggio che ha a disposizione e sia la lista dei vari competitor in quella zona.**


