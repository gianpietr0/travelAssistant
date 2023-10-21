% File contenente la definizione delle regole del dominio

% importazione degli altri file prolog
:-include('housingFacts.pl').
:-include('turismFacts.pl').
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