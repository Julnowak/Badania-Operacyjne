from math import inf  # Z biblioteki math importuję inf — wartość nieskończoną
from typing import Dict, List, Tuple  # Importuje typy danych


def DPA(G: Dict[int, List[int]], a: List[List], s: int) -> Tuple[List[Tuple[int, int]], int]:
    suma = 0  # suma — oznaczenie sumarycznej wagi krawędzi MST
    A = []  # A — zbiór krawędzi MST, wartość zwracana, wytyczająca ścieżkę
    alfa = dict()  # słownik z poprzednikami wierzchołka u w MST - do wartości u (klucz) przypisywany
    # jest jego poprzednik
    beta = dict()  # słownik z wagą krawędzi łączącej u z wierzchołkiem alfa[u] -
    # wartości u (klucz) przypisywana jest waga krawędzi łącząca go z odpowiednim wierzchołkiem
    V = [key for key in G.keys()]  # zbiór wierzchołków G (kluczy) w postaci listy

    for u in V:  # Dla każdego wierzchołka należącego do wierzchołków grafu
        beta[u] = inf  # ustawiam wartości dla wszystkich kluczy w słowniku b na inf
        alfa[u] = 0  # ustawiam wartości dla wszystkich kluczy w słowniku a na 0

    Q = V  # Przypisuję listę wierzchołków (kluczy) do zmiennej Q
    beta[s] = 0  # przypisuję 0, gdyż pierwszy wierzchołek nie ma poprzednika
    Q.remove(s)  # Usuwam wierzchołek z listy dostępnych wierzchołków (bo już tam byłam)

    u2 = s  # Ustawiam poprzednika na wartość przyjętego przeze mnie wierzchołka początkowego

    while Q:  # Dopóki lista wierzchołków nieodwiedzonych się nie zwolni, wykonuj
        for _ in Q:  # Dla każdego wierzchołka należącego do G
            for u in G[u2]:  # I dla każdego wierzchołka należącego do sąsiedztwa poprzedniego wierzchołka
                if a[u][u2] < beta[u]:  # Sprawdzam, czy wartość krawędzi jest mniejsza od inf, a jeśli tak
                    alfa[u] = u2  # Poprzedni wierzchołek (u2) dołącza do słownika poprzedników (kluczem jest u)
                    beta[u] = a[u][u2]  # Do słownika z wagami dopisuję wagę krawędzi (u i u2 określają współrzędne)
                else:
                    continue  # W innym wypadku kontynuuj
        # W tym miejscu zostały napotkane trudności, gdyż funkcja min() nie może zwrócić wartości z nieiteracyjnych typów
        # Dlatego też, zastosowałam prosty algorytm poszukiwania najmniejszej wartości
        minimum = inf  # Ustawiam wartość nieskończoność w pętli, aby nadpisywała się przy każdym cyklu
        for u in Q:  # Dla każdego wierzchołka w zbiorze pozostałych wierzchołków
            if minimum > beta[u]:  # Jeśli zmienna minimum jest większa od wartości krawędz dopisanej wierzchołkowi u
                u2 = u  # To należy wziąć wierzchołek u (obecny) i przypisać go poprzednikowi
                minimum = beta[u]  # A nowym minimum stanie się wartość krawędzi dla wierzchołka u
            else:
                continue  # W innym przypadku przejdź dalej
                # Pętla for sprawia, że minimum będzie się zmieniać aż do momentu, kiedy skończą nam się dostępne
                # wierzchołki, dla których możemy odczytać krawędzie

        Q.remove(u2)  # Usuwamy z pozostałych wierzchołków wierzchołek-poprzednik
        A.append((alfa[u2], u2))  # Do listy zwracanych krawędzi dołączam krotkę z poprzednikiem
        # poprzednika i poprzednikiem
        suma += a[alfa[u2]][u2]  # Do ogólnej sumy krawędzi dołączam wartość krawędzi poprzednika- poprzednika
        # z poprzednikiem

    return A, suma  # Zwracam listę krawędzi A (ostateczna droga) i wartość najkrótszej drogi w postaci krotki


if __name__ == '__main__':
    graph = {0: [1, 2, 3], 1: [0, 2, 4, 5, 6], 2: [0, 1, 3, 6], 3: [0, 2, 6, 7], 4: [1, 5, 8, 9], 5: [1, 4, 6, 9],
             6: [1, 2, 3, 5, 7, 9], 7: [3, 6, 8, 9], 8: [4, 7, 9], 9: [4, 5, 6, 7, 8]}

    a = [
        [inf, 4, 1, 4, inf, inf, inf, inf, inf, inf],
        [4, inf, 5, inf, 9, 9, 7, inf, inf, inf],
        [1, 5, inf, 3, inf, inf, 9, inf, inf, inf],
        [4, inf, 3, inf, inf, inf, 10, inf, inf, 18],
        [inf, 9, inf, inf, inf, 2, inf, 4, 6, inf],
        [inf, 9, inf, inf, 2, inf, 8, 2, inf, inf],
        [inf, 7, 9, 10, inf, 8, inf, 9, inf, 8],
        [inf, inf, inf, inf, 4, 2, 9, inf, 3, 9],
        [inf, inf, inf, inf, 6, inf, inf, 3, inf, 9],
        [inf, inf, inf, 18, inf, inf, 8, 9, 9, inf]
    ]
    # Dobry
    # graph = {
    #     0: [1, 2],
    #     1: [0, 3, 4, 5],
    #     2: [0, 5, 6],
    #     3: [1, 4],
    #     4: [1, 3, 9],
    #     5: [1, 2, 9],
    #     6: [2, 7, 8],
    #     7: [6],
    #     8: [6, 9],
    #     9: [4, 5, 8]
    # }

    # graph = {
    #     0: [1, 2, 3],
    #     1: [0],
    #     2: [0, 4],
    #     3: [1, 4, 5, 6],
    #     4: [2, 3],
    #     5: [3],
    #     6: [3],
    #     7: [8, 9],
    #     8: [7, 9],
    #     9: [7, 8]
    # }

    # Dobry
    # a = [[inf, 1, 3, inf, inf, inf, inf, inf, inf, inf],
    #      [1, inf, inf, 2, 1, 6, inf, inf, inf, inf],
    #      [3, inf, inf, inf, inf, 2, 1, inf, inf, inf],
    #      [inf, 2, inf, inf, 3, inf, inf, inf, inf, inf],
    #      [inf, 1, inf, 3, inf, inf, inf, inf, inf, 2],
    #      [inf, 6, 2, inf, inf, inf, inf, inf, inf, 5],
    #      [inf, inf, 1, inf, inf, inf, inf, 4, 3, inf],
    #      [inf, inf, inf, inf, inf, inf, 4, inf, inf, inf],
    #      [inf, inf, inf, inf, inf, inf, 3, inf, inf, 1],
    #      [inf, inf, inf, inf, 2, 5, inf, inf, 1, inf]]

    # a = [[inf, 1, 3, 2, inf, inf, inf, inf, inf, inf],
    #      [1, inf, inf, inf, inf, inf, inf, inf, inf, inf],
    #      [3, inf, inf, inf, 4, inf, inf, inf, inf, inf],
    #      [2, inf, inf, inf, 1, 4, 1, inf, inf, inf],
    #      [inf, inf, 4, 1, inf, inf, inf, inf, inf, inf],
    #      [inf, inf, inf, 4, inf, inf, inf, inf, inf, inf],
    #      [inf, inf, inf, 1, inf, inf, inf, inf, inf, inf],
    #      [inf, inf, inf, inf, inf, inf, inf, inf, 1, 2],
    #      [inf, inf, inf, inf, inf, inf, inf, 1, inf, 4],
    #      [inf, inf, inf, inf, inf, inf, inf, 2, 1, inf]]

    print(DPA(graph, a, 0))
