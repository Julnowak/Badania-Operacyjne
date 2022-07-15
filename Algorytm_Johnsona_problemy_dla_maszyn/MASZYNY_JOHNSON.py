import numpy as np
from math import inf
from copy import deepcopy

# Algorytm Johnsona m=2


# Funkcja do znajdowania minimalnego elementu macierzy (przeznaczona głównie dla dwóch maszyn)
def find_min(matrix):
    mini = inf      # Minimalna wartość - początkowo ustawiona na inf
    for row in matrix:      # Dla każdego rzędu
        for x in row:       # Dla każdej wartości w rzędzie
            if x and x < mini:  # Jeśli element x w rzędzie nie jest None i jest mniejszy od wartości minimalnej
                mini = x    # To ustawiam ten element jako nową wartość minimalną i zwracam
    return mini


# Funkcja pomocnicza do wypisywania kolejności np. Z1 -> Z2 ->...
def print_kol(kol):
    text = ''   # Ustawiam pusty string
    for i in kol:       # Dla każdej wartości w liście kolejności
        if i != kol[0]:     # Jeśli nie jestem przy pierwsze wartości to będę dodawać strzałkę przed zadaniem
            text += ' -> '
        text += f'Z{i + 1}' # Dodaję zadanie z jego numerem
    print(text)     # Wypisuję


# Algorytm Johnsona dla 2 maszyn z przeróbką
def Two_machines(M1, base_m=None):  # przyjmuje jako parametr 2 wyliczone wiersze i macierz podstawową (dla liczby maszyn większej niż 2)
    if base_m is not None:  # Dla nich  wyppisuję macierz początkową
        print(f'\nMacierz początkowa:\n{base_m}')
    else:
        print(f'\nMacierz początkowa:\n{M1}')

    # Dla pierwszego wiersza macierzy dwuwierszowej
    res = {}
    for i in M1[0]: # Zliczam wystąpienia każdej wartości
        res[i] = (M1[0].count(i))

    keys = []
    for k, v in res.items():    # Jeśli wartość się powtórzy to wpisuję ją na listę keys
        if v > 1:
            keys.append(k)

    l = []
    for q in keys:  # Dla każdej wartości, która się powtórzyła
        l = [i for i, x in enumerate(M1[0]) if x == q]  # Wyszukuję tę wartość w macierzy dwuwierszowej i dodaję jej indeks
                                                        # do listy z indeksami

    if not l:   # Zabezpieczenie, gdy lista zostaje pusta - muszę dodać 1 element, żeby pętla for wykonała się raz
        l.append(None)

    # Tworzę dwie listy - na terminy oraz kolejności
    terminy = []
    kolejnosc = []
    for indeks in range(len(l)):    # Dla każdego indeksu elementu w liście l
        print(f'\nWERSJA {indeks + 1}')     # Wersja zmienia się, gdy mamy więcej niż 1 takich samych wartośći w I rzędzie
        M = deepcopy(M1)    # kopiuję macierz, żeby nie zmieniać oryginału
        Q = [None] * len(M[0])  # Optymalna kolejność - lista początkowa z None

        # indeksy pomocnicze - K to pierwszy element, S - ostatni
        K = 0
        S = len(M[0]) - 1

        minimum = find_min(M)   # szukam minimum w macierzy dwuwierszowej
        for i in range(len(M[0])):  # Dla każdego indeksu w liście indeksów pierwszego wierszamacierzy dwuelementowej M
            if minimum in M[0]:     # Jeśli minimum znajduje się w pierwszym wierszu
                if l[indeks] is not None and minimum == M[0][l[indeks]]:    # Jeśli w l nie ma None i minimum przyrównamy do wartości indeksu z l
                    idx = l[indeks]     # To przyjmuję jeden z indeksów z l
                else:
                    idx = list(M[0]).index(minimum) # Inaczej wyznaczam sobie ten indeks, wyszukując minimum w pierwszym wierszu
                Q[K] = idx  # Na poczętku kolejności ustawiam index w miejscu K
                K += 1      # K przesuwam do przodu (zwiększam o jeden)
                M[0][idx] = None    # Z pierwszego wiersza macierzy wykreślam wartość w miejscu indeksu
                M[1][idx] = None    # Z drugiego wiersza macierzy wykreślam wartość w miejscu indeksu
            elif minimum in M[1]:     # Jeśli minimum znajduje się w drugim wierszu
                idx = list(M[1]).index(minimum)    # Wyznaczam sobie indeks, wyszukując minimum w drugim wierszu
                Q[S] = idx  # Na końcu kolejności ustawiam index w miejscu S
                S -= 1      # S przesuwam do tyłu (zmniejszam o jeden)
                M[0][idx] = None    # Z pierwszego wiersza macierzy wykreślam wartość w miejscu indeksu
                M[1][idx] = None    # Z drugiego wiersza macierzy wykreślam wartość w miejscu indeksu

            if None in Q:   # Jeśli w Q będzie znajdować się jakieś None, czyli puste miejsca
                minimum = find_min(M)   # Wyszukuję nową wartość minimum i powtarzam pętle
            else:
                break   # W innym wypadku pętle przerywam

        print('\nKolejność zadań:')     # Wypisuję kolejność zadań
        print_kol(Q)

        # Podobnie jak wcześniej, tworzę kopię macierzy oryginalnej
        if base_m is not None:
            m = deepcopy(base_m)
            baza = base_m
        else:
            m = deepcopy(M1)
            baza = M1

        # Uszeregowanie

        t = []  # Macierz t będzie macierzą None'ów, w której znajdą się uszeregowanie
        for _ in range(len(m)):
            t.append([None] * len(m[0]))

        # Macierz czasów T będzie kopią macierzy None'ów t, w której znajdą się uszeregowanie
        T = deepcopy(t)
        counter = 0     # Licznik

        for idx in Q:   # Dla każdego indeksu w kolejności Q
            for i in range(len(m)):    # Dla każdej maszyny
                t[i][counter] = baza[i][idx]     # Szereguję według kolejności macierz wejściową i uzupełniam macierz t
            counter += 1        # Licznik zwiększa się w pętli

        print('\nUszeregowanie:')      # Wypisuję macierz uszeregowań
        print(np.array(t))

        for i in range(len(t)):     # Dla każdej maszyny
            for j in range(len(t[0])):      # Dla każdego zadania
                suma1 = 0
                suma2 = 0
                for k in range(j + 1):      # Wyliczenia sum przeprowadzam według wzorów podanych na wykładzie
                    suma1 += t[0][k]
                T[0][j] = suma1

                for n in range(i + 1):
                    suma2 += t[n][0]
                    T[n][0] = suma2
            # Ogólnie rzecz biorąc, powyższe wzory umożliwiły mi uzupełnienie pierwszego wiersza i pierwszej kolumny macierzy czasów T

        # Mając pierwszą kolumnę i pierwszy rząd mogę bez problemu obliczyć pozostałe wartości i uzupełnić macierz czasów
        # Robię to w dwóch poniższych pętlach, bez obliczania wyznaczonej kolumny i rzędu
        for i in range(1, len(t)):
            for j in range(1, len(t[0])):
                T[i][j] = max(T[i][j - 1], T[i - 1][j]) + t[i][j]

        print('\nTerminy zakończenia:')     # Wypisuję terminy zakończenia
        print(np.array(T))

        terminy.append(T)       # Zwracam listy terminów i kolejności
        kolejnosc.append(Q)

    return terminy, kolejnosc


# Właściwy algorytm CDS
def CDS(matrix):
    termin_opt = []     # Lista terminów optymalnych dla każdego r i wszystkich przypadków
    kolejnosc_opt = []      # Lista kolejności optymalnych dla każdego r i wszystkich przypadków

    for r in range(1, len(matrix)):     # Dla r w zakresie od 1 do maksymalnej liczby maszyn - 1
        print(f'\nDla r = {r}')         # Wypisuję r
        print('-------------------------------------')
        ran1 = list(range(r))       # Wyznaczam listę wszystkich r
        ran2 = [len(matrix) - 1 - x for x in ran1]    # Wyznaczam listę wszystkich r, tylko liczone są one od tyłu

        M1 = [0] * len(matrix[0])   # Tworzę pierwszy wiersz zer
        for i in ran1:      # Do których dodam odpowiednie wartości z macierzy wejściowej i utworzę pierwszy rząd
            M1 += matrix[i]     # Dla algorytmu dla 2 maszyn

        M2 = [0] * len(matrix[0])   # Tworzę drugi wiersz zer
        for x in ran2:      # Do których dodam odpowiednie wartości z macierzy wejściowej i utworzę drugi rząd
            M2 += matrix[x]     # Dla algorytmu dla 2 maszyn

        M = []      # M to moja macierz na bazie macierzy wejściowej, wyliczona ze wzorów, do której dołączę utworzone rzędy
        M.append(list(M1))
        M.append(list(M2))
        # W ten sposób otrzymuję macierz dla algorytmu 2 maszyn, który następnie wyliczam
        t, k = Two_machines(M, matrix)
        # Z algorytmu otrzymuję listę macierzy/ macierz czasów oraz macierz kolejnosci/kolejnosc macierzy

        # Otrzymane wartości dodaję do wcześniej utworzonych list
        termin_opt += t
        kolejnosc_opt += k

    # Tworzę kolejną listę, która posłuży do zoptymalizowania wyników
    lista = []
    for t in termin_opt:        # Dla każdej macierzy czasu t w wynikowych macierzach czassu
        lista.append(t[-1][-1])     # Sprawdzam ostatni element wiersza i kolumny, który jest końcowym czasem
    pos = lista.index(min(lista))       # Znajduję czas minimalny i zapamiętuję jego pozycję

    print('\n=============================\nOptymalna macierz czasów:')
    print(np.array(termin_opt[pos]))    # Na podstawie znalezionj pozycji wyznaczam optymalny czas oraz optymalną kolejność

    print('\nOptymalna kolejność zadań:')
    print_kol(np.array(kolejnosc_opt[pos]))

    print(f'\nMinimalny potrzebny czas: {min(lista)}')


# Przykłady
macierz = np.array([[9, 6, 8, 7, 12, 3],
                    [7, 3, 5, 10, 4, 7]], object)

example = np.array([[12, 7, 10, 4, 16],
                    [10, 12, 6, 15, 8],
                    [6, 18, 8, 13, 6],
                    [15, 9, 12, 7, 10]], object)

M = np.array([[34, 18, 74, 43, 8, 81, 84, 16, 68, 48],
              [49, 5, 22, 21, 86, 5, 44, 32, 12, 83],
              [47, 96, 31, 68, 59, 86, 73, 54, 5, 6],
              [95, 55, 52, 99, 9, 80, 88, 27, 34, 33],
              [11, 51, 74, 28, 19, 3, 67, 68, 54, 96],
              [85, 98, 81, 36, 88, 54, 15, 63, 1, 32]], object)

M2 = np.array([[92, 96, 14, 24, 47, 24, 10, 98, 15, 71],
               [89, 49, 79, 43, 5, 47, 9, 71, 4, 77],
               [78, 91, 6, 66, 90, 11, 98, 1, 27, 52],
               [15, 99, 5, 58, 28, 25, 66, 100, 95, 81],
               [46, 2, 71, 69, 72, 98, 94, 68, 19, 48],
               [28, 1, 86, 46, 37, 25, 100, 38, 67, 70]], object)

if __name__ == '__main__':
    CDS(M2)

