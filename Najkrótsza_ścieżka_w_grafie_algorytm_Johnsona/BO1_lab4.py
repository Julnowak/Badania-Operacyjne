# Algorytm Johnsona

from math import inf  # Z biblioteki math importuję inf — wartość nieskończoną
from typing import Dict, List, Tuple  # Importuje typy danych


# DIJKSTRA
def Dijkstra(G, w, s):
    V = [key for key in G.keys()]  # Lista wierzchołków-kluczy

    d = dict()  # słownik odległości od źródła dla wszystkich wierzchołków grafu
    poprzednik = dict()  # słownik z poprzednikami wierzchołka v - do wartości u (klucz) przypisywany jego poprzednik
    Q = dict()  # Zbiór wierzchołków pozostałych

    for v in V:  # dla każdego wierzchołka v w zbiorze wierzchołków-kluczy
        d[v] = inf  # ustawiam wartości dla wszystkich kluczy w słowniku d na inf
        poprzednik[v] = None  # ustawiam wartości dla wszystkich kluczy w słowniku na None
        Q[v] = v  # Przypisuję listę wierzchołków (kluczy) do zmiennej Q

    Q.pop(s)  # Usuwam s z pozostałych wierzchołków
    d[s] = 0  # przypisuję 0, bo wierzchołek początkowy nie ma odległości od siebie
    u2 = s  # Ustawiam poprzednika na wartość przyjętego przeze mnie wierzchołka początkowego

    while Q:  # Dopóki lista wierzchołków nieodwiedzonych się nie zwolni, wykonuj
        for _ in Q.values():  # Dla każdego wierzchołka należącego do G
            for u in G[u2]:  # I dla każdego wierzchołka należącego do sąsiedztwa poprzedniego wierzchołka
                if d[u2] + w[u2][u] < d[u]:  # relaksacja
                    d[u] = d[u2] + w[u2][u]
                    poprzednik[u] = u2
        minimum = inf  # Zdejmowanie wierzchołka najbliżej źródła, który nie został jeszcze rozważony
        for u in Q.values():  # Dla każdej wartości w pozostałych wierzchołkach
            if d[u] < minimum:  # Znajduję najmniejszą drogę dla wierzchołka u
                u2 = u
                minimum = d[u]
        if u2 in Q:  # Jeśli poprzednik jest w Q, to go usuwam, w innym przypadku przerywam pętle
            Q.pop(u2)  # Zapobiega to powstawaniu błędów przy kompilacji
        else:
            break

    # Zwrócenie drogi (odległości od wierzchołka początkowego) i poprzedników
    return d, poprzednik


# BELLMANA-FORDA
def Bellman_Ford(G, w, s):
    V = [key for key in G.keys()]  # Zbiór wszystkich wierzchołków-kluczy
    poprzednik = dict()  # Zbiór poprzedników danych wierzchołków
    d = dict()  # Odległość od początkowego punktu

    for v in V:  # Dla każdego wierzcołka w wierzchołkach
        d[v] = inf  # Do wszystkich odległości od początku przypisz inf
        poprzednik[v] = None  # Poprzednik pierwszego wierzchołka nie istnieje

    d[s] = 0  # Odległość od pierwszego wierzchołka jest równa 0

    for i in range(len(V) + 1):  # Dla i do o 1 mniejszej ilości wierzchołków
        for u in V:  # Dla pewnej krawędz i (u,v) w zbiorrze krawędzi
            for v in G[u]:
                if d[v] > d[u] + w[u][v]:  # Jeśli odległość wierzchołka v jest większa od odległości
                    # wierzchołka u + waga krawędzi (u,v)
                    if i == len(V):  # Jeśli dodatkowo i będzie równe ilości wierzchołków - 1
                        raise Exception('Został znaleziony cykl ujemny')  # Wyrzuć wyjątek

                    d[v] = d[u] + w[u][
                        v]  # W innym wypadku przypisz do odległości v odległość wierzchołka u + waga krawędzi (u,v)
                    poprzednik[v] = u  # A poprzednik ustaw na wierzchołek u

    # Zwrócenie drogi (odległości od wierzchołka początkowego)
    # Poprzednik nie jest tu potrzebny, a więc go nie zwracam
    return d


def Johnson(G, w, first, last):
    V = [key for key in G.keys()]  # Zbiór wszystkich wierzchołków-kluczy
    q = V[
            -1] + 1  # Tworzę nowy wierzchołek, którego nazywam np. '10', w tym celu wzięłam ostatni klucz i dodałam do niego 1
    G[q] = V  # Do wierzchołka '10' dopisuję listę sąsiadów, którymi są wszystkie wierzchołki

    # Zapisuję istnienie nowego wierzchołka w tablicy warości innych wierzchołków
    for wierzcholek in w:  # Do tablicy wag, dla każdego wierzchołka dopisuję inf
        wierzcholek.append(inf)  # jako wagę dla połączenia z wierzchołkiem np. '10'

    # Do tablicy wartości dołączam wierzchołek 10, z wartościami połączenia 0
    # z innymi wierzchołkami, a sam ze sobą - inf
    w.append(([0] * (len(V))) + [inf])

    # Używam algorytmu Bellmana-Forda, startując od dodanego wierzchołka dodanego
    min_dystans = Bellman_Ford(G, w, q)
    # Odnajduję i zwracam minimalną odległość d[v] dla każdego wierzchołka v od q
    # Jeżeli został wykryty ujemny cykl, zwracam informację i przerywam działanie algorytmu.

    # Przewagowanie grafu, aby zlikwidować ujemne wartości, nie zmieniając wartości najkrótszych ścieżek
    # Każdej krawędzi zostaje przypisana nowa waga
    for u in range(len(w)):
        for v in range(len(w)):
            if w[u][v] != inf:
                w[u][v] += min_dystans[u] - min_dystans[v]

    # Usuwam dodany wcześniej wierzchołek q z listy sąsiedztwa i tablicy wartości
    G.pop(q)
    w.pop(-1)
    # Usuwam wagi połączeń dla każdego z wierzchołków z ostatniego miejsca
    for wierzcholek in w:
        wierzcholek.pop(-1)

    # Tworzę słownik, który będzie przechowywał wyniki algorytmu Dijkstry dla każdego wierzchołka
    D = dict()
    for k in V:  # Dla każdego wierzchołka
        # Przypisuję krotkę do danego wierzchołka-klucza
        D[k] = Dijkstra(G, w, k)
        for e in D[k][0].keys():  # Dla każdego wierzchołka dla danego klucza
            D[k][0][e] += min_dystans[e] - min_dystans[k]  # Przewagowanie
    minDist = [last]  # Biorę ostatni wierzchołek
    s = last  # Przypisuję do zmiennej s
    while s != first:  # Dopóki s nie dotrze do pierwszego wierzchołka
        s = D[first][1][s]  # Dokładaj kolejne wierzchołki
        minDist.append(s)

    length = D[first][0][last]  # Długość ścieżki można odczytać biorąc jedną z wartości D
    return length, minDist[::-1]  # Zwracam długość ścieżki i opisane wierzchołki


if __name__ == '__main__':
    # Dobry
    graph = {
        0: [1, 2],
        1: [0, 3, 4, 5],
        2: [0, 5, 6],
        3: [1, 4],
        4: [1, 3, 9],
        5: [1, 2, 9],
        6: [2, 7, 8],
        7: [6],
        8: [6, 9],
        9: [4, 5, 8]
    }

    a = [[inf, 1, 3, inf, inf, inf, inf, inf, inf, inf],
         [1, inf, inf, 2, 1, 6, inf, inf, inf, inf],
         [3, inf, inf, inf, inf, 2, 1, inf, inf, inf],
         [inf, 2, inf, inf, 3, inf, inf, inf, inf, inf],
         [inf, 1, inf, 3, inf, inf, inf, inf, inf, 2],
         [inf, 6, 2, inf, inf, inf, inf, inf, inf, 5],
         [inf, inf, 1, inf, inf, inf, inf, 4, 3, inf],
         [inf, inf, inf, inf, inf, inf, 4, inf, inf, inf],
         [inf, inf, inf, inf, inf, inf, 3, inf, inf, 1],
         [inf, inf, inf, inf, 2, 5, inf, inf, 1, inf]]

    print(Dijkstra(graph, a, 0))
    print(Bellman_Ford(graph, a, 0))

    l, wr = Johnson(graph, a, 0, 8)
    print(f'Najkrótsza znaleziona ścieżka ma długość: {l}')
    print(f'Ścieżka ta przechodzi przez wierzchołki: {wr}\n')

    graph_z_ujemnym = {
        0: [1, 2, 3],
        1: [2],
        2: [4],
        3: [4],
        4: [6, 7],
        5: [7],
        6: [8],
        7: [9],
        8: [7],
        9: [5]
    }

    a_z_ujemnym = [[inf, 4, 2, 1, inf, inf, inf, inf, inf, inf],
                   [inf, inf, 5, inf, inf, inf, inf, inf, inf, inf],
                   [inf, inf, inf, inf, 2, inf, inf, inf, inf, inf],
                   [inf, inf, inf, inf, -1, inf, inf, inf, inf, inf],
                   [inf, inf, inf, inf, inf, inf, 7, 2, inf, inf],
                   [inf, inf, inf, inf, inf, inf, inf, -2, inf, inf],
                   [inf, inf, inf, inf, inf, inf, inf, inf, 1, inf],
                   [inf, inf, inf, inf, inf, inf, inf, inf, inf, 2],
                   [inf, inf, inf, inf, inf, inf, inf, 5, inf, inf],
                   [inf, inf, inf, inf, inf, -2, inf, inf, inf, inf]]

    # l,wr = Johnson(graph_z_ujemnym, a_z_ujemnym, 0, 8)
    # print(f'Najkrótsza znaleziona ścieżka ma długość: {l}')
    # print(f'Ścieżka ta przechodzi przez wierzchołki: {wr}\n')

    graph1 = {
        0: [1, 2, 3],
        1: [2],
        2: [4],
        3: [4],
        4: [6, 7],
        5: [7, 8],
        6: [8],
        7: [9],
        8: [7, 2],
        9: [5]
    }

    a1 = [[inf, 4, 2, 1, inf, inf, inf, inf, inf, inf],
          [inf, inf, 5, inf, inf, inf, inf, inf, inf, inf],
          [inf, inf, inf, inf, 2, inf, inf, inf, inf, inf],
          [inf, inf, inf, inf, 4, inf, inf, inf, inf, inf],
          [inf, inf, inf, inf, inf, inf, 7, 2, inf, inf],
          [inf, inf, inf, inf, inf, inf, inf, -2, 3, inf],
          [inf, inf, inf, inf, inf, inf, inf, inf, 1, inf],
          [inf, inf, inf, inf, inf, inf, inf, inf, inf, 2],
          [inf, inf, 3, inf, inf, inf, inf, 5, inf, inf],
          [inf, inf, inf, inf, inf, 6, inf, inf, inf, inf]]

    l, wr = Johnson(graph1, a1, 0, 8)
    print(f'Najkrótsza znaleziona ścieżka ma długość: {l}')
    print(f'Ścieżka ta przechodzi przez wierzchołki: {wr}\n')

    graph = {
        0: [1, 2, 3],
        1: [0],
        2: [0, 4],
        3: [1, 4, 5, 6],
        4: [2, 3],
        5: [3],
        6: [3],
        7: [8, 9],
        8: [7, 9],
        9: [7, 8]
    }

    a = [[inf, 1, 3, 2, inf, inf, inf, inf, inf, inf],
         [1, inf, inf, inf, inf, inf, inf, inf, inf, inf],
         [3, inf, inf, inf, 4, inf, inf, inf, inf, inf],
         [2, inf, inf, inf, 1, 4, 1, inf, inf, inf],
         [inf, inf, 4, 1, inf, inf, inf, inf, inf, inf],
         [inf, inf, inf, 4, inf, inf, inf, inf, inf, inf],
         [inf, inf, inf, 1, inf, inf, inf, inf, inf, inf],
         [inf, inf, inf, inf, inf, inf, inf, inf, 1, 2],
         [inf, inf, inf, inf, inf, inf, inf, 1, inf, 4],
         [inf, inf, inf, inf, inf, inf, inf, 2, 1, inf]]

    graph2 = {
        0: [1, 2],
        1: [3],
        2: [3, 4],
        3: [8],
        4: [5, 8],
        5: [6],
        6: [7, 9],
        7: [3, 8],
        8: [5],
        9: [7]
    }

    a2 = [[inf, -1, 2, inf, inf, inf, inf, inf, inf, inf],
          [inf, inf, inf, 3, inf, inf, inf, inf, inf, inf],
          [inf, inf, inf, -2, 4, inf, inf, inf, inf, inf],
          [inf, inf, inf, inf, inf, inf, inf, inf, 4, inf],
          [inf, inf, inf, inf, inf, 2, inf, inf, -1, inf],
          [inf, inf, inf, inf, inf, inf, -1, inf, inf, inf],
          [inf, inf, inf, inf, inf, inf, inf, 2, inf, 5],
          [inf, inf, inf, -1, inf, inf, inf, inf, 2, inf],
          [inf, inf, inf, inf, inf, 3, inf, inf, inf, inf],
          [inf, inf, inf, inf, inf, inf, inf, -3, inf, inf]]

    l, wr = Johnson(graph2, a2, 0, 8)
    print(f'Najkrótsza znaleziona ścieżka ma długość: {l}')
    print(f'Ścieżka ta przechodzi przez wierzchołki: {wr}\n')

    A_invert = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [-3, 3, 0, 0, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [2, -2, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, -3, 3, 0, 0, -2, -1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 2, -2, 0, 0, 1, 1, 0, 0],
                [-3, 0, 3, 0, 0, 0, 0, 0, -2, 0, -1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, -3, 0, 3, 0, 0, 0, 0, 0, -2, 0, -1, 0],
                [9, -9, -9, 9, 6, 3, -6, -3, 6, -6, 3, -3, 4, 2, 2, 1],
                [-6, 6, 6, -6, -3, -3, 3, 3, -4, 4, -2, 2, -2, -2, -1, -1],
                [2, 0, -2, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 2, 0, -2, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                [-6, 6, 6, -6, -4, -2, 4, 2, -3, 3, -3, 3, -2, -1, -2, -1],
                [4, -4, -4, 4, 2, 2, -2, -2, 2, -2, 2, -2, 1, 1, 1, 1]]
    # l, wr = Johnson(graph, a, 0, 6)
    # print(f'Najkrótsza znaleziona ścieżka ma długość: {l}')
    # print(f'Ścieżka ta przechodzi przez wierzchołki: {wr}\n')
