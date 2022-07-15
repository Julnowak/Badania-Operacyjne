from typing import List, Dict


def DFS(g: Dict[str, List[str]], s: str):
    visited = []  # visited- lista odwiedzonych wierzchołków

    track = dict()  # track- słownik do przypisywania numeracji odwiedzonym punktom
    num = 1  # num- numer określający kolejność, w której pojawił się dany wierzchołek

    acykliczny = True  # Określa, czy graf jest acykliczny, czy nie
    spojny = True  # Określa, czy graf jest spójny, czy nie

    S = [s]     # Tworzę strukturę "stosu" na bazie listy i dodaję pierwszy element- ten, od którego zaczynam
    while S:        # Wykonuję, dopóki stos nie będzie pusty
        r = S.pop(0)        # Zdejmuję wierzchołek z "góry" stosu
        if r not in visited:        # Jeśli wierzchołek nie jest w liście odwiedzonych wierzchołków
            visited.append(r)           # Wrzucam ten wierzchołek do listy odwiedzonych wierzchołków
            visited_count = 0           # Ustawiam licznik odwiedzeń dla danego wierzchołka
            helper = []                # Tworzę tymczasową listę pomocniczą 'helper'
            for u in g[r]:              # Dla każdego wierzchołka w wartościach grafu dla klucza r
                if u not in visited:        # Jeśli wierzchołka nie ma w odwiedzonych
                    helper.append(u)          # Wrzucam go do listy 'helper'
                else:                           # A jeśli już jest w odwiedzonych
                    visited_count += 1         # Omijam go i zwiększam licznik odwiedzeń o 1
                    if visited_count > 1:       # Jeśli jakiś wierzchołek zostanie odwiedzony więcej niż 1 raz
                        acykliczny = False          # To będziemy wiedzieć, że nasz graf nie jest acykliczny
                S = helper + S         # Na koniec do mojego stosu dodaję pomocniczą listę i tak powstaje nowy stos

    if len(visited) < len(g.keys()):    # Jeśli długość listy odwiedzonych wierzchołków będzie mniejsza
        spojny = False                  # od ilości kluczy grafu to graf nie będzie spójny
                                        # (bo pewne wierzchołki zostaną nieodwiedzone)

    for i in visited:         # Dodanie numerów przy ustalonej kolejności- dla lepszego zrozumienia tematu
        track[num] = i          # Ustalam klucze i wartości
        num += 1                # Zwiększam numerację

    return track, spojny, acykliczny        # Zwracam wierzchołki z numeracją, czy graf jst spójny i
                                            # czy graf jest acykliczny


graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E', 'F'],
    'C': ['A', 'F', 'G'],
    'D': ['B'],
    'E': ['B'],
    'F': ['B', 'C'],
    'G': ['C', 'H', 'I'],
    'H': ['G'],
    'I': ['G', 'J'],
    'J': ['I']
}

print(DFS(graph, 'A'))

graph_sa = {
    'A': ['B', 'C', 'D'],
    'B': ['A'],
    'C': ['A'],
    'D': ['A', 'E', 'F', 'G'],
    'E': ['D', 'H', 'I'],
    'F': ['D'],
    'G': ['D'],
    'H': ['E', 'J'],
    'I': ['E'],
    'J': ['H']
}

slownik, spojny, acykliczny = DFS(graph_sa, 'A')

print('---- Graf spójny acykliczny ----')
for k, v in slownik.items():
    print(f'Jako {k} został odwiedzony wierzchołek {v}.')
print(f'\nCzy graf jest spójny? {spojny}')
print(f'Czy graf jest acykliczny? {acykliczny}\n')


graph_sc = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B'],
    'D': ['B', 'E', 'F'],
    'E': ['D', 'F', 'H'],
    'F': ['D', 'E', 'G'],
    'G': ['F'],
    'H': ['E', 'I', 'J'],
    'I': ['H'],
    'J': ['H']
}

slownik, spojny, acykliczny = DFS(graph_sc, 'A')

print('---- Graf spójny z cyklami ----')
for k, v in slownik.items():
    print(f'Jako {k} został odwiedzony wierzchołek {v}.')
print(f'\nCzy graf jest spójny? {spojny}')
print(f'Czy graf jest acykliczny? {acykliczny}\n')

graph_nc = {
    'A': ['B', 'C', 'D'],
    'B': ['A'],
    'C': ['A', 'E'],
    'D': ['A', 'E', 'F', 'G'],
    'E': ['C', 'D'],
    'F': ['D'],
    'G': ['D'],
    'H': ['I', 'J'],
    'I': ['H', 'J'],
    'J': ['H', 'I']
}

slownik, spojny, acykliczny = DFS(graph_nc, 'A')

print('---- Graf niespójny z cyklami ----')
for k, v in slownik.items():
    print(f'Jako {k} został odwiedzony wierzchołek {v}.')
print(f'\nCzy graf jest spójny? {spojny}')
print(f'Czy graf jest acykliczny? {acykliczny}\n')
