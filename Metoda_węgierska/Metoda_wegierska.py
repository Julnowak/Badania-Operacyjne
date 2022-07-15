import numpy as np
from math import inf


# Krok przygotowawczy

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
            if (mat[j][i] < minm):  # Jeśli element będzie mniejszy od najmniejszego to
                minm = mat[j][i]  # Ustawia ten element jako najmniejszy

        list_min.append(minm)  # dodaje do listy min z każdej kolumny
        fi += minm  # Dodaję najmniejszą wartość do fi przy każdej kolumnie

    for i in range(m):  # Dla każdej kolumny
        for j in range(n):  # Dla każdego wiersza
            mat[j][i] -= list_min[i]  # Od wartości elementu w macierzy odejmuję wartość z listy
    return mat, fi


def reduce_matrix(mat, n, m):
    print(f'\nMacierz początkowa:\n{mat}')

    mat1, fi1 = reduce_row(mat, n, m)  # Redukcja wierszy
    print(f'\nMacierz po redukcji wierszy:\n{mat1}')
    print(f'Fi po redukcji wierszy: {fi1}')

    mat2, fi2 = reduce_col(mat1, n, m)  # Redukcja kolumn
    print(f'\nMacierz po redukcji kolumn:\n{mat2}')

    return mat2, fi1 + fi2


# Krok 2 - poszukiwanie kompletnego przydziału
# szukanie elementów zerowych w macierzy:
# na początku szukam wiersza, który ma jak najmniej zer

# matrix_bool - macierz w której elementy o wartości 0 będą zaznaczone jako True
# a inne wartości jako False
# zero_place - pusta lista w której znajdą się współrzędne zer
def zero(matrix_bool, zero_place):
    size_row = [1000, -1]  # przykładowy rozmiar, ilość wierszy, podany dosyć duży, żeby działał dla dużych macierzy

    # iteracja w której znajdujemy wiersz, w którym jest najmniej zer
    for row in range(matrix_bool.shape[0]):
        if 0 < np.sum(matrix_bool[row] == True) < size_row[
            0]:  # szukam odpowiedniego wiersza, o najmniejszej liczbie zer
            size_row = [np.sum(matrix_bool[row] == True), row]
    #
    # zaznaczenie zer i wartości innych niż 0
    zero_index = np.where(matrix_bool[size_row[1]] == True)[0][0]  # oznaczenie zer w macierzy jako True
    zero_place.append((size_row[1], zero_index))  # dodanie do listy indeksu zer
    matrix_bool[size_row[1], :] = False  # oznaczenie pozostałych wartości w wierszach jako False
    matrix_bool[:, zero_index] = False  # oznaczenie wartości których nie ma w zero_index jako False

    return matrix_bool, zero_place


# Funkcja służaca do zaznaczenia zer niezależnych, zostaną zwrócone ich indeksy, które będą elementami zwróconej listy
def mark_matrix(macierz):
    zero_matrix = (macierz == 0)  # macierz z wartościami True False
    zero_matrix_copy = zero_matrix.copy()  # stworzenie kopii

    independent_zero = []  # lista do której będę umieszczał współrzędne zer niezależnych
    while True in zero_matrix_copy:  # wykonywanie wcześniejszej funkcji do momentu gdy są wartosci w macierzy
        zero(zero_matrix_copy, independent_zero)

    dependent_zero = list()  # Lista na zera zależne
    for i in range(zero_matrix.shape[0]):  # Dla każdego wiersza
        for j in range(zero_matrix.shape[1]):  # Dla każdej kolumny w macierzy z zerami
            if (i, j) not in independent_zero and zero_matrix[i][
                j] == True:  # Jeśli współrzędne (i, j) nie znajdują się
                dependent_zero.append(
                    (i, j))  # Na liście zer niezależnych i są zerami, to dodaję zero do listy zer zależnych
    return zero_matrix, independent_zero, dependent_zero


def min_lines(matrix, nzal, zal):
    M = matrix.copy()  # Tworzę kopię macierzy
    rows = list(range(matrix.shape[0]))  # Lista wierszy
    cols = []  # Lista kolumn

    for nzero in nzal:  # Dla każdego niezależnego zera w liście zer niezależnych
        if nzero[0] in rows:  # Jeśli pierwsza współrzędna zera niezależnego jest w wierszach
            rows.remove(nzero[0])  # Usuwam tą współrzędną z wiersza

    if rows:  # Jeśli lista wierszy nie jest pusta
        for zzero in zal:  # Dla każdego zera zależnego w zerach zależnych
            if zzero[0] in rows:  # Jeśli pierwsza współrzędna zera zależnego jest w wierszach
                if zzero[1] not in cols:
                    cols.append(zzero[1])  # Przyłączam drugą współrzędną zera zależnego do listy kolumn

    if cols:  # Jeśli lista kolumn nie jest pusta
        for nzero in nzal:  # Dla każdego zera niezależnego w zerach niezależnych
            if nzero[1] in cols:  # Jeśli druga współrzędna zera niezależnego jest w kolumnach
                rows.append(nzero[0])  # Przyłączam pierwszą współrzędną zera niezależnego do listy wierszy

    xr = []  # Lista na rzędy nieprzekreślone
    for i in range(matrix.shape[0]):  # Dla każdego wiersza
        for j in range(matrix.shape[1]):  # Dla każdej kolumny
            if i not in rows:  # Jeśli wiersz nie jest w wierszach nieprzekreślonych
                M[i][j] = 'x'  # przekreślam wiersz
                if i not in xr:  # Jeśli i nie jest w już w rzędach nieprzekreślonych to dodajemy
                    xr.append(i)
            if j in cols:  # Jeśli kolumna jest w kolumnach przekreślonych to przekreślam tą kolumnę
                M[i][j] = 'x'

    return M, matrix, xr, cols


def increasing(new_matrix, old_matrix, fi, rows, cols):
    mini = inf  # Ustawam zmienną mini na nieskończność (szukanie elementu minimalnego)
    for i in range(new_matrix.shape[0]):  # Dla każdego wiersza
        for j in range(new_matrix.shape[1]):  # Dla każdej kolumny
            if isinstance(new_matrix[i][j], str):  # Jeśli element jest przekreślony to idź dalej
                continue
            elif new_matrix[i][j] < mini:  # A jeśli element jest mniejszy od mini to
                mini = new_matrix[i][j]  # Ustaw ten element jako nową wartość mini

    for i in range(new_matrix.shape[0]):  # Dla każdego wiersza
        for j in range(new_matrix.shape[1]):  # Dla każdej kolumny
            if isinstance(new_matrix[i][j], str):  # Jeśli element jest przekreślony to idź dalej
                continue
            else:
                old_matrix[i][j] -= mini  # Inaczej, od elementu starej macierzy odejmij minimalną wartość
                # z nieprzekreślonych wartości

    if rows and cols:  # Jeśli listaw wierszy nieprzekreślonych i kolumn przekreślonych nie są puste
        for i in rows:  # to dla każdego indeksu wiersza w wierszach nieprzekreślonych
            for j in cols:  # i dla każdego indeksu kolumny w kolumnach przekreślonych
                old_matrix[i][j] += mini  # powiększ element starej macierzy o mini

    fi += mini  # Zwiększenie wartości fi o krotność elementu minimalnego

    return old_matrix, fi


def Metoda_wegierska(matrix):
    M, fi = reduce_matrix(matrix, matrix.shape[0], matrix.shape[1])  # Redukcja macierz
    print(f'Wartość fi po redukcji: {fi}\n')
    _, niezalezne, zalezne = mark_matrix(M)  # Szukanie zer zależnych i niezależnych
    M, matrix, xr, cols = min_lines(M, niezalezne, zalezne)  # Poszukiwanie minimalnej liczby linii wykreślających
    print(f'Macierz po wykreśleniu:\n{M}\n')
    f = True  # "Wieczna" pętla z warunkiem stopu
    while f:
        if len(xr) + len(cols) >= matrix.shape[
            0]:  # Jeśli liczba wykreśleń równa się maksymalnej liczbie zer niezależnych
            f = False  # przerywam pętle
        else:
            M, fi = increasing(M, matrix, fi, xr, cols)  # Jeśli nie to możnap poszerzyć liczbę zer niezależnych
            _, niezalezne, zalezne = mark_matrix(M)  # Szukanie zer zależnych i niezależnych
            M, matrix, xr, cols = min_lines(M, niezalezne,
                                            zalezne)  # Poszukiwanie minimalnej liczby linii wykreślających

    print(f'Macierz końcowa:\n{matrix}\n')
    print(f'Macierz wykreślona:\n{M}\n')
    print(f'Wartość funkcji kryterialnej: {fi}\n')
    print(f'Zbiór zer niezależnych: {niezalezne}\n')
    # Macierz optymalna
    new = np.zeros((matrix.shape[0], matrix.shape[1]))
    for i in niezalezne:
        new[i[0]][i[1]] = 1

    print(f'Macierz optymalna:\n{new}\n')


# matrix = np.array([[6, 3, 6, 3, 3, 1, 8, 3],
#                    [5, 3, 2, 2, 3, 5, 7, 3],
#                    [9, 7, 1, 7, 1, 9, 1, 3],
#                    [7, 1, 2, 8, 6, 2, 6, 1],
#                    [9, 2, 6, 7, 7, 8, 9, 8],
#                    [4, 9, 4, 9, 2, 2, 3, 2],
#                    [7, 6, 7, 3, 2, 9, 8, 2],
#                    [6, 8, 5, 9, 7, 4, 1, 1]
#                    ], dtype=object)


# matrix_example = np.array([[5, 2, 3, 2, 7],
#                            [6, 8, 4, 2, 5],
#                            [6, 4, 3, 7, 2],
#                            [6, 9, 0, 4, 0],
#                            [4, 1, 2, 4, 0]], dtype=object)

# # Dobra,nasza macierz
# matrix = np.array([[7, 1, 6, 3, 4, 8],
#                    [1, 8, 1, 3, 7, 4],
#                    [2, 6, 9, 3, 4, 8],
#                    [3, 7, 6, 1, 6, 4],
#                    [1, 3, 2, 6, 5, 3],
#                    [5, 5, 3, 5, 2, 1]], dtype=object)
#

# matrix = np.array([[1, 1, 1, 1, 1, 1],
#                    [1, 1, 1, 1, 1, 1],
#                    [1, 1, 1, 1, 1, 1],
#                    [1, 1, 1, 1, 1, 1],
#                    [1, 1, 1, 1, 1, 1],
#                    [1, 1, 1, 1, 1, 1]], dtype=object)

matrix = np.array([[1, 2, 3, 4, 5, 6],
                   [1, 2, 3, 4, 5, 6],
                   [1, 2, 3, 4, 5, 6],
                   [1, 2, 3, 4, 5, 6],
                   [1, 2, 3, 4, 5, 6],
                   [1, 2, 3, 4, 5, 6]], dtype=object)

if __name__ == '__main__':
    Metoda_wegierska(matrix)
