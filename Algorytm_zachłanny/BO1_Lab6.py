from math import inf
from copy import deepcopy


def G_TSP(G, w):
    edges = list()  # Zmienna pomocnicza reprezentująca listę krawędzi
    V = dict()  # Zmienna będąca słownikiem krawędzi odwiedzonych, które zostaną na końcu dodane do ścieżki

    path = []  # Zmienna reprezentująca ścieżkę
    suma = 0  # Zmienna reprezentująca sumą wartości wszystkich krawędzi ścieżki

    for k, v in G.items():  # dla każdego klucza k i każdej wartości v w grafie
        for i in range(len(v)):  # powtarzaj dodawanie krawędzi do zmiennej edges, aż i osiągnie wartość
            if (k, v[i]) not in edges:  # (jeśli nie ma takiej krawędzi)
                edges.append((k, v[i]))  # równą długości listy wierzchołków wierzchołka-klucza

    weight_edges = dict()  # przerobienie edges na słownik, w którym oprócz krawędzi, znajdują się także ich wagi
    for edge in edges:  # dla każdej krawędzi w edges, do słownika weight_edges dodaję krawędź jako klucz
        weight_edges[edge] = w[edge[0]][edge[1]]  # oraz wagę tej krawędzi jako wartość

    # Uporządkowanie w ciąg niemalejący
    new = sorted(weight_edges.items(),
                 key=lambda x: x[1])  # Sortuję tak, aby otrzymać listę krotek, uszeregowanych rosnąco według wag
    # w krotkach tych znajdują się krotki opisujące krawędź oraz ich wagi
    w_copy = deepcopy(w)  # Tworzę kopię tablicy wag przy pomocy deepcopy, gdyż standardowa implementacja powodowała
    # problemy z wartością inf
    num = 0  # pomocnicza zmienna, zwiększana w pętli
    while len(V.keys()) < len(G.keys()):  # Dopóki długość kluczy słownika krawędzi V będzie mniejsza od ilości
        # kluczy grafu

        if num > len(new) - 1:  # Zabezpiecznie przed wyjściem poza zakres - wyjście z pętli, gdy zostanie przekroczony
            break
        elem = new[num]  # Zmiennej elem przyporządkowuję pierwszą krotkę z listy krotek ((krawędź), waga)
        num += 1  # Zwiększam num o 1, aby w nstępnych powtórzeniach odwoływać się do innych elementów listy new
        x = elem[0][0]  # x to pierwszy węzeł tworzący krawędź z danej krotki
        y = elem[0][1]  # y to drugi węzeł tworzący krawędź z danej krotki

        w_copy[x][
            y] = inf  # Kopii tablicy wag, jako wagę krawędzi x-y, przypisuję wartość inf, co oznacza, że usuwam to
        # połączenie z tablicy (tak, żeby nie zmodyfikować oryginału)

        if x in V.keys() or y in V.values():  # Jeśli x już znajduje się w kluczach V albo y w wartościach V, to
            continue  # przejdź dalej

        # Jeśli wierzchołek końcowy krawędzi 'y' będzie w kluczach słownika V i wierzchołek począrkowy krawędzi 'x'
        # będzie w wartościach słownika V i Dopóki długość kluczy słownika krawędzi V będzie mniejsza od ilości
        # kluczy grafu pomniejszonej o jeden
        if y in V.keys() and x in V.values() and len(V.keys()) < (len(G.keys()) - 1):
            ans = True  # Zmienna pomocnicza ans = True
            helper = y  # Przypisuję do zmiennej helper watość y
            for i in range(len(V.keys())):  # Dla każdego i w zakresie długości kluczy V
                if helper not in V.keys():  # Jeśli helper nie jest w kluczach to ans = False
                    ans = False
                else:  # Inaczej, helper staje się wartością słownika V dla klucza helper
                    helper = V[helper]
            if ans:  # Jeśli odpowiedź ans ostatecznie jest prawdą to obliczenia są kontynuowane
                continue

        # Dodaję do słownika V krawędź o kluczu x i wartośći y
        V[x] = y

        # Dodaję wagę tej krawędzi do sumy
        suma += w[x][y]

    # pierwszy key to pierwszy klucz w kluczach słownika V
    key = list(V.keys())[0]
    for _ in range(len(V)):  # Powtarzam dopóki nie dojdę do końca V
        if key in path:  # Jeśli klucz już jest w ścieżce oznacza to, że wystąpił błąd
            raise Exception('Wystąpił błąd - nie ma takiego klucza w ścieżce')
        path.append(key)  # inaczej przyłączam klucz do ścieżki
        if key not in V.keys():  # Zabezpieczenie, jeśli klucza nie ma w kluczach V
            break  # Przerwij wykonywanie pętli
        else:
            key = V[key]  # inaczej, za klucz przyjmij wartość V dla danego klucza
    if len(path) < len(V.keys()) - 1:  # Wyjątek, gdy nie wszystkie elementy zostaną znalezione
        raise Exception('Niepełna ścieżka została znaleziona')
    # Zwrócenie ścieżki w postaci listy z wierzchołkami (sekwencja wierzchołków) oraz łącznej wartości drogi
    return path, suma


if __name__ == '__main__':
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
    #
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

    # V, suma = G_TSP(graph, a)
    # print(V, suma)

    # g3 = {
    #     0: [1, 2, 3, 4, 6],
    #     1: [0, 2, 3, 4, 5, 8],
    #     2: [0, 1, 4, 5, 6],
    #     3: [0, 1, 5, 6, 7],
    #     4: [0, 1, 2, 5],
    #     5: [1, 2, 3, 4, 6, 8],
    #     6: [2, 3, 5],
    #     7: [1, 2, 4, 6, 8, 9],
    #     8: [1, 4, 6, 9],
    #     9: [4, 6, 8],
    # }
    #
    # a3 = [[inf, 5, 6, 4, 1, 2, 3, 2, 7, 6],
    #       [5, inf, 2, 1, 7, 3, 1, 1, 1, 8],
    #       [6, 2, inf, 2, 1, 4, 1, 8, 6, 3],
    #       [4, 1, 2, inf, 2, 4, 4, 3, 3, 2],
    #       [1, 7, 1, 2, inf, 3, 1, 5, 3, 1],
    #       [2, 3, 4, 4, 3, inf, 1, 2, 5, 9],
    #       [3, 1, 1, 4, 1, 1, inf, 4, 6, 8],
    #       [2, 1, 8, 3, 5, 2, 4, inf, 1, 3],
    #       [7, 1, 6, 3, 3, 5, 6, 1, inf, 1],
    #       [6, 8, 3, 2, 1, 9, 8, 3, 1, inf]]

    # V, suma = G_TSP(g3, a3)
    # print(V, suma)

    graph4 = {
        0: [1, 2, 3, 4, 5, 6, 7],
        1: [3, 4, 6, 7, 8, 9],
        2: [0, 1, 3, 4, 5, 6, 7, 8, 9],
        3: [0, 1, 2, 4, 5, 6, 7, 8, 9],
        4: [1, 2, 5, 6, 8, 9],
        5: [0, 1, 2, 3, 4, 6, 7, 8, 9],
        6: [0, 1, 2, 4, 5, 7, 8, 9],
        7: [0, 1, 2, 3, 4, 5, 6, 8, 9],
        8: [1, 2, 3, 4, 5, 6, 7],
        9: [2, 3, 4, 5, 6, 7, 8]
    }

    a4 = [[inf, -1, 1, 1, 1, 1, 1, 1, inf],
          [inf, inf, 2, 2, 2, 2, 2, 2, 2, -2],
          [1, 2, inf, 3, 3, 3, 3, 3, 3, 3],
          [1, 2, 3, inf, 4, 4, 4, 4, 4, 4],
          [inf, 2, 3, 4, inf, 5, 5, 5, 5, 5],
          [1, 2, 3, 4, 5, inf, 6, 6, 6, 6],
          [1, 2, 3, 4, 5, 6, inf, 7, 7, 7],
          [1, 2, 3, 4, 5, 6, 7, inf, 8, 8],
          [inf, 2, 3, 4, 5, 6, 7, 8, inf, 9],
          [inf, inf, 3, 4, 5, 6, 7, 8, 9, inf]]

    path, suma = G_TSP(graph4, a4)
    print(f'Ścieżka: {path}')
    print(f'Suma: {suma}')

    # g = {
    #     0: [1, 2, 3, 4],
    #     1: [0, 3, 6],
    #     2: [0, 3, 4, 5],
    #     3: [0, 1, 2, 5, 6],
    #     4: [0, 2, 5],
    #     5: [1, 2, 3, 4, 6],
    #     6: [1, 3, 5, 9],
    #     7: [6],
    #     8: [6, 7],
    #     9: [8]
    # }
    #
    # a = [
    #     [inf, 2, 1, 4, 3, inf, inf, inf, inf, inf],
    #     [2, inf, inf, 3, inf, inf, 5, inf, inf, inf],
    #     [1, inf, inf, 7, 1, 2, inf, inf, inf, inf],
    #     [4, 3, 7, inf, inf, 4, 4, inf, inf, inf],
    #     [3, inf, 1, inf, inf, 3, inf, inf, inf, inf],
    #     [inf, inf, 2, 4, 3, inf, 3, inf, inf, inf],
    #     [inf, 5, inf, 4, inf, 3, inf, inf, inf, 0],
    #     [inf, inf, inf, inf, inf, inf, 4, inf, inf, inf],
    #     [inf, inf, inf, inf, inf, inf, 0, 4, inf, inf],
    #     [inf, inf, inf, inf, inf, inf, inf, inf, -1, inf]
    # ]
    #

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

    # path, suma = G_TSP(graph, a)
    # print(f'Ścieżka: {path}')
    # print(f'Suma: {suma}')

    # graph_z_ujemnym = {
    #     0: [1, 2, 3],
    #     1: [2],
    #     2: [4],
    #     3: [4],
    #     4: [6, 7],
    #     5: [7],
    #     6: [8],
    #     7: [9],
    #     8: [7],
    #     9: [5]
    # }
    #
    # a_z_ujemnym = [[inf, 4, 2, 1, inf, inf, inf, inf, inf, inf],
    #                [inf, inf, 5, inf, inf, inf, inf, inf, inf, inf],
    #                [inf, inf, inf, inf, 2, inf, inf, inf, inf, inf],
    #                [inf, inf, inf, inf, -1, inf, inf, inf, inf, inf],
    #                [inf, inf, inf, inf, inf, inf, 7, 2, inf, inf],
    #                [inf, inf, inf, inf, inf, inf, inf, -2, inf, inf],
    #                [inf, inf, inf, inf, inf, inf, inf, inf, 1, inf],
    #                [inf, inf, inf, inf, inf, inf, inf, inf, inf, 2],
    #                [inf, inf, inf, inf, inf, inf, inf, 5, inf, inf],
    #                [inf, inf, inf, inf, inf, -2, inf, inf, inf, inf]]
    #
    # path, suma = G_TSP(graph_z_ujemnym, a_z_ujemnym)
    # print(f'Ścieżka: {path}')
    # print(f'Suma: {suma}')
