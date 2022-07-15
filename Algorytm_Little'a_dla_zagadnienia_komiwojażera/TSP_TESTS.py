
import numpy as np
from math import inf


# Redukcja wierszy
def reduce_row(mat, n, m):
    fi = 0  # Fi ustawiam na 0
    for i in range(n):  # Dla każdego wiersza
        min = np.min(mat[i])  # znajduję minimalną wartość w wiersz
        fi += min  # i dodaję ją do fi
        for j in range(m):  # Dla każdej kolumny
            mat[i][j] -= min  # Odejmuję wartość minimalną od każdego elementu w wierszu
    return mat, fi


# Redukcja kolumn
def reduce_col(mat, n, m):
    list_min = []  # lista min w kolumnach
    fi = 0  # sumaryczna redukcja
    for i in range(m):  # dla każdej kolumny
        minm = inf  # ustawienie inf jako min
        for j in range(n):  # dla każdego wiersza
            if mat[j][i] < minm:  # Jeśli element będzie mniejszy od najmniejszego to
                minm = mat[j][i]  # Ustawia ten element jako najmniejszy

        list_min.append(minm)  # dodaje do listy min z każdej kolumny
        fi += minm  # Dodaję najmniejszą wartość do fi przy każdej kolumnie

    for i in range(m):  # Dla każdej kolumny
        for j in range(n):  # Dla każdego wiersza
            try:
                mat[j][i] -= list_min[i]  # Od wartości elementu w macierzy odejmuję wartość z listy
            except:
                pass
    return mat, fi


def reduce_matrix(mat):
    n = mat.shape[0]    # Liczba wierszy
    m = mat.shape[1]    # Liczba kolumn

    print(f'\nMacierz początkowa:\n{mat}')

    mat1, fi1 = reduce_row(mat, n, m)  # Redukcja wierszy
    mat2, fi2 = reduce_col(mat1, n, m)  # Redukcja kolumn
    print(f'\nMacierz po redukcji kolumn:\n{mat2}')

    return mat2, fi1 + fi2    # Zwraca macierz po redukcji oraz sumę poredukcyjną


def choose_path(mat, lista, rozw, lr=None, lc=None):
    # lista i rozw to listy, przejść - rzeczywistych oraz tych "idealnych"
    # Jest to wynikiem zastosowania tablicy przeliczeń, niezbędnej do wprowadzenia przy rzeczywistej redukcji macierzy
    # lr oraz lc to listy z indeksami - również zostały wprowadzone w celach upiększenia ścieżki

    # W razie, gdyby tych list nie było, tworzę je
    if lr is None:
        lr = list(range(1, mat.shape[0] + 1))
    if lc is None:
        lc = list(range(1, mat.shape[1] + 1))

    n = mat.shape[0]    # Wyznaczam liczbę rzędów
    m = mat.shape[1]    # Wyznaczam liczbę kolumn

    d = dict()      # Tworzę słowniki przekodowań
    dk = dict()     # Słownik d to słownik rzeczywisty, dk to słownik wyidealizowany

    for i in range(n):  # Dla każdego rzędu
        for j in range(m): # Dla każdej kolumny
            if mat[i][j] == 0:   # Jeśli znajdę w macierzy zero to dla tej kolumny i tego wiersza znajduję najmniejsze wartosći
                ar = [mat[i][jj] for jj in range(len(mat[i][:])) if jj != j]  # Dokonuję tego poprzez stworzenie list
                mr = min(ar)    # oraz wyszukanie wartości minimlanych

                ac = [mat[ii][j] for ii in range(len(mat[:][j])) if ii != i]
                mc = min(ac) # Powtarzam to dwukrotnie

                d[(i, j)] = max(mr, mc)     # W słownikach zapisuję odpowiednie wierzchołki oraz wyliczoną dla nich wartość najmniejszą
                dk[(lr[i], lc[j])] = max(mr, mc) # Sprawdzanie wykazało, iż daje ona prawidłowe wyniki

    max_edge = None
    maxi = -inf     # Szukam wierzchołka o największej możliwej wartości w słowniku
    for k, v in d.items(): # iterując po wszystkich kluczach i wartościach
        if v > maxi:
            maxi = v        # Jeśli znajdę taką wartość to staj się ona wartością największą, a wierzchołek staje się
            max_edge = k       # wierzchołkiem, który zostanie dołączony do rozwiązań

    h = None    # Podobnie robię dla wartości do rozwiązania
    maxi = -inf
    for k, v in dk.items():
        if v > maxi:
            maxi = v
            h = k

    if n <= 2:   # Zabezpieczenie przed małymi macierzami - przy końcowym rezultacie, ostatecznie musimy dodać tylko jeden punkt
        rozw.append(list(dk.keys())[1])     # Gdyż mamy tylko jedną kolumnę i wierzchołek, który pozostał, jeśli rozważamy symetryczną macierz
    lista.append(max_edge)                  # z cyklem Hamiltona
    rozw.append(h)  # Przyłączam do rozwiązań końocwych

    return max_edge, h, lr, lc, lista, rozw   # Zwracam wszelkie potrzebne dane


def aktualizuj(mat, e, hh, koszt, lista, rozw, lr=None, lc=None):
    r = mat.shape[0]    # Ilość wierszy
    c = mat.shape[1]    # Ilość kolumn
    # Ponowne przeliczenie minimalnych wartości dla danego miejsca w macierzy (analogicznie jak wcześniej)
    ar = [mat[e[0]][jj] for jj in range(len(mat[e[0]][:])) if jj != e[0]]
    mr = min(ar)

    ac = [mat[ii][e[1]] for ii in range(len(mat[:][e[1]])) if ii != e[1]]
    mc = min(ac)
    h = max(mr, mc)
    print(f'Koszt niewybrania to: {koszt + h}')   # Przeliczenie kosztu prawej gałęzi

    # Tablice indeksowania
    if lr is None:
        lr = list(range(1, mat.shape[0] + 1))
    if lc is None:
        lc = list(range(1, mat.shape[1] + 1))

    # Fizyczne zmniejszenie rozmiaru tablicy
    mat = np.delete(mat, e[0], 0)
    mat = np.delete(mat, e[1], 1)

    li = []
    lk = []
    start = None
    end = None
    for (i, k) in rozw:
        li.append(i)
        lk.append(k)

    for i in li:
        if i not in lk:
            start = i

    for k in lk:
        if k not in li:
            end = k

    # Wyszukanie odpowiedniego wierzchołka, którego edycja ma zapobiec tworzeniu się podcykli
    # Usunięcie współrzędnych z tabel indeksowania
    lr.remove(hh[0])
    lc.remove(hh[1])

    # Wprowadzenie zakazu
    mat[lr.index(end)][lc.index(start)] = inf


    addon = 0
    new = mat
    for i in range(r - 1):
        for j in range(c - 1):
            # Jeśli we wszsytkich rzęach i kolumnach nie znajduje się 0 to należy zredukować macierz
            if 0 not in list(mat[:][j]) or 0 not in list(mat[i][:]):
                new, addon = reduce_matrix(mat)
    # Otrzymany koszt dodajemy do kosztu ogólnego
    nowy_koszt = koszt + addon
    print(f'LB: {nowy_koszt}')
    # Wybranie nowej ściezki i wypisanie
    newpk, newh, lr, lc, lista, rozw = choose_path(new, lista, rozw, lr, lc)
    return newpk, newh, new, lr, lc, lista, rozw, nowy_koszt


matrix = np.array([
    [inf, 3, 5, 1, 1, 6, 1],
    [1, inf, 3, 2, 2, 1, 4],
    [4, 2, inf, 5, 2, 3, 2],
    [1, 3, 5, inf, 1, 5, 3],
    [2, 6, 1, 3, inf, 2, 1],
    [5, 1, 2, 3, 5, inf, 2],
    [1, 2, 4, 1, 3, 2, inf]
])

M1 = np.array([[inf, 3, 4, 4, 1],
               [1, inf, 5, 3, 1],
               [1, 1, inf, 5, 1],
               [1, 1, 5, inf, 2],
               [1, 3, 2, 2, inf]])

M2 = np.array([[inf, 10, 8, 19, 12],
               [10, inf, 20, 6, 3],
               [8, 20, inf, 4, 2],
               [19, 6, 4, inf, 7],
               [12, 3, 2, 7, inf]])

# matrix = np.array([
#     [inf, 1, 5, 3, 1, 4, 2,3,7],
#     [2, inf, 3, 3, 3, 1, 4,1,2],
#     [4, 3, inf, 5, 2, 4, 2,2,6],
#     [6, 5, 5, inf, 1, 9, 6,1,2],
#     [5, 7, 1, 3, inf, 8, 7,2,4],
#     [4, 3, 7, 3, 9, inf, 2,6,2],
#     [1, 5, 6, 1, 3, 7, inf,8,5],
#     [7, 2, 6, 1, 6, 7, 3,inf,2],
#     [7, 2, 6, 1, 6, 1, 3,2,inf]
# ])

m2, LB2 = reduce_matrix(M2)
lista = []
rozw = []

e, h, mat, _, lista, rozw = choose_path(m2, lista, rozw)
print(mat)

npk, nh, mat, lr, lc, lista, rozw, nowy_koszt = aktualizuj(m2, e, h, LB2, lista, rozw)
for i in range(matrix.shape[0]-5):
    npk, nh, mat, lr, lc, lista, rozw, nowy_koszt = aktualizuj(mat, npk, nh, nowy_koszt, lista, rozw, lr, lc)
    print(mat)
print()
print(f'LB: {nowy_koszt}')
print(rozw)

li = []
lk = []
start = None
end = None
for (i, k) in rozw:
    li.append(i)
    lk.append(k)

for i in li:
    if i not in lk:
        start = i
        print(start)

for k in lk:
    if k not in li:
        end = k

