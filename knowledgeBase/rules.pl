% File contenente la definizione delle regole del dominio

% importazione degli altri file prolog
:-include('housingFacts.pl').
:-include('turismFacts.pl').
:-include('calendar.pl').
:- discontiguous prop/3.


% regola che indica se un alloggio si trova in un quartiere turistico

isInTuristNeigh(H, N):- housing(H), turisticNeighbourhood(N), prop(H, 'neighbourhood', N).

% regola che indica se un alloggio si trova in un quartiere lussuoso

isInLuxuryNeigh(H, N):- housing(H), luxuryNeighbourhood(N), prop(H, 'neighbourhood', N).

% regola che indica se un alloggio si trova vicino (a meno di 500 metri) da un attrazione turistica

isNearAttraction(H, T):- housing(H), attraction(T), distance(H, T, D), D < 2000.

% regola che indica se due punti di riferimento (alloggio e/o attrazione) si trova nello stesso quartiere

sameNeigh(X1, X2):- prop(X1, 'neighbourhood', N), prop(X2, 'neighbourhood', N).

% regola che calcola la distanza tra due punti di riferimento (alloggio e/o attrazione)

distance(H, T, D):- prop(H, 'latitude', Lat1), prop(H, 'longitude', Lon1),
    prop(T, 'latitude', Lat2), prop(T, 'longitude', Lon2), haversine(Lat1, Lon1, Lat2, Lon2, Distance),
    D is Distance.

% regola che applica la formula di haversine per calcolare la distanza

haversine(Lat1, Lon1, Lat2, Lon2, Distance):- DLat is Lat2 - Lat1, DLon is Lon2 - Lon1, A is sin(DLat / 2) ** 2 + cos(Lat1) * cos(Lat2) * sin(DLon / 2) ** 2,
    C is 2 * atan2(sqrt(A), sqrt(1 - A)),
    Radius is 6371000,  % Raggio medio della Terra in metri
    Distance is Radius * C.


% fatti circa il numero di giorni nei vari mesi
daysPerMonth(1, 31).
daysPerMonth(2, 28).
daysPerMonth(3, 31).
daysPerMonth(4, 30).
daysPerMonth(5, 31).
daysPerMonth(6, 30).
daysPerMonth(7, 31).
daysPerMonth(8, 31).
daysPerMonth(9, 30).
daysPerMonth(10, 31).
daysPerMonth(11, 30).
daysPerMonth(12, 31).


% regola che verifica la validità di una data
date(D, M, Y):- Y >= 2023, M >=1, M =< 12, daysPerMonth(M, X), D >= 1, D =< X.


% regole che consente di definire la data successiva
nextDay(date(D, M, Y), date(ND, NM, NY)) :- daysPerMonth(M, X), D < X , ND is D + 1, NM = M, NY = Y.
nextDay(date(D, M, Y), date(1, NM, NY)):- daysPerMonth(M, X), D = X, NM is M + 1, NY = Y.
nextDay(date(31, 12, Y), date(1, 1, NY)):- NY is Y + 1.

% regola che verifica se è possibile alloggiare in un certo alloggio per un certo periodo a partire da una determinata data in base alle disponibilità giornaliere
journey(ID, StartDate, Duration):- checkAvailability(ID, StartDate, Duration).

% regole che effettuano un controllo ricorsivo sulle disponibilità giornaliere diun certo alloggio
 checkAvailability(_, _, 0).
 checkAvailability(ID, Date, Duration):- available(ID, Date), nextDay(Date, NextDate), NewDuration is Duration - 1, checkAvailability(ID, NextDate, NewDuration).