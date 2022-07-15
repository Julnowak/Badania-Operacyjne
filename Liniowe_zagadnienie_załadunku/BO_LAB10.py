import numpy as np
from math import inf
# Import pomocniczych bibliotek

# Implementacja całkowitoliczbowego problemu liniowego
def CPD_method(b, a, num, q):
    # b - maksymalna pojemność
    # a - waga poszczególnych typów przedmiotów
    # num - ilość przedmiotów każdego typu
    # q - macierz kar

    szt = len(num)  # ilość sztuk
    X = np.zeros((b + 1, szt))  # Utworzenie macierzy dla x-ów (sztuk możliwych)
    f = np.zeros((b + 1, szt))  # Utworzenie macierzy na wartości funkcji minimalizującej - 3 wzory

    # program podzieliłam na etapy - można było zrealizować je krócej, ale z etapami program był bardziej czytelny

    # Pierwszy etap
    for y in range(b + 1):   # Dla każdej możliwej pojemności tk, od 0 do np.10
        lista = list(range(int(y / a[len(a) - 1]) + 1))  # Tworzę listą z x, które wyliczam według wzorów
                # w ten sposób otrzymam iksy, dla których będę szukać minimum
        x_mini = None   # Szukam x, dla którego wartość będze minimalna
        mini = inf      # Zmienna do szukania minimum
        for x in lista:     # Dla każdego x-a w liście
            try:                   # Wprowadzam zabezpieczenie przed wartościami None i zbyt dużymi indekasami
                if q[x][len(a) - 1] < mini:     # Jeśli wartość kary dla x-ego rzędu i ostatniej kolumny jest mniejsza
                                                # od minimum
                    mini = q[x][len(a) - 1]     # To wartość ta staje się nowym minimum
                    x_mini = x                  # A obecny z zostaje zapisany jako z najmniejszą wartością
            except:
                pass      # Pomiń
        X[y][0] = x_mini    # W każdym rzędzie, w pierwszej kolumnie wpisuję obliczone wartości x z minimalną wartością
        f[y][0] = mini      # Do macierzy f wpisuję wyliczoną najmniejszą wartość kary, dla każdego rzędu i pierwszej
                            # kolumny
    c = 0   # Deklaracja licznika pomocniczego od 0

    # Kolejne etapy (pomiędzy, nie pierwsze i nie ostatnie)
    for idx in range(len(a) - 2, 0, -1):    # Dla każdej wartości idx, nie pierwszej i nie ostatniej, malejącej o 1
        for y in range(b + 1):      # Dla każdej pojemności od 0 do np.10
            lista = list(range(int(y / a[idx]) + 1))  # Tworzę listą z x, które wyliczam według wzorów
            x_mini = None   # Szukam x, dla którego wartość będze minimalna
            mini = inf      # Zmienna do szukania minimum
            for x in lista:     # Dla każdego x-a w liście
                try:                # Wprowadzam zabezpieczenie przed wartościami None i zbyt dużymi indekasami
                    if q[x][idx] is None:   # Jeśli wartość nie jest None to przejdź dalej
                        pass
                    elif q[x][idx] + f[y - a[idx] * x][c] < mini:   # Jeśli wartość kary w miejscu macierzy [x, idx ]
                                    # plus wartość z poprzedniej kolumny dla indeksu rzędu opisanego wzorem oraz
                                    # indeksu c jest mniejsza od minimalnej wartości
                        mini = q[x][idx] + f[y - a[idx] * x][c] # To staje się ona minimalną wartoścą
                        x_mini = x  # A odpowiadający jej x staje się x-em minimalnym
                except:
                    pass       # Pomiń
            X[y][len(a) - idx - 1] = x_mini  # W kolejne kolumny, licząc od przodu, zostają wstawione wartośći x minimalnego
            f[y][len(a) - idx - 1] = mini  # W kolejne kolumny, licząc od przodu, zostają wstawione wartośći minimalne
        c += 1  # Licznik zwiększa się o 1

    # Ostatni etap
    # Tym razem opuszczam iterację - ni jest konieczna
    lista = list(range(b + 1))  # Wyznaczam listę wszytskich pojemności
    x_mini = None   # Szukam x, dla którego wartość będze minimalna
    mini = inf      # Zmienna do szukania minimum
    for x in lista:     # Dla każdej pojemności w liście
        try:                # Wprowadzam zabezpieczenie przed wartościami None i zbyt dużymi indekasami
            if q[x][0] == None:   # Jeśli wartość dla rzędu x i pierwszej kolumny z macierzy kar nie jest None to przejdź dalej
                pass
            elif q[x][0] + f[b - a[0] * x][len(a) - 2] < mini:   # Jeśli wartość kary w miejscu macierzy [x, 0 ]
                                    # plus wartość z poprzedniej kolumny dla indeksu rzędu opisanego wzorem dla
                                    # pierwszego a (wagi,kosztu) oraz
                                    # indeksu c jest mniejsza od minimalnej wartości i wartości ostatniej
                                    #jest mniejsza od wartości minimalnej
                mini = q[x][0] + f[b - a[0] * x][len(a) - 2] # To staje się ona minimalną wartoścą
                x_mini = x  # A odpowiadający jej x staje się x-em minimalnym
        except:
            pass    # Pomiń
    X[b][len(a) - 1] = x_mini  # Przypisuję minimalnego x do wiersza b i ostatniej kolumny macierzy X
    f[b][len(a) - 1] = mini  # Przypisuję wartość minimalną do wiersza b i ostatniej kolumny macierzy f

    return X, f    # Zwracam obie macierze

# Dobieranie strategii
def strategy(a, y, X, f):
    # y - maksymalna pojemność
    # a - waga poszczególnych typów przedmiotów
    # X - macierz z x-ami (ilością)
    # f - macierz z wartościami minimalnymi kar

    yik = y # yik przechowuje y - przyjmuje największą pojemność
    strat = '\n'    # Część początkowa ostatecznego stringa
    yi = len(a)     # Ilość zmiennych x
    for i in range(yi - 1, -1, -1):     # dla każdej zmiennej (bez pierwszej, do 0) zmniejszamy o -1
        idx = yi - i - 1    # Odpowiednio dobieram indeksy tak, aby wypisać z macierzy to, czego chcę
        strat += f'x{idx+1} --> {int(X[yik, i])}\nf{yi - idx}(y{idx}) = {f[yik, i]}\n\n'
        yik = int(yik - a[idx] * X[yik, i])   # Ponownie przeliczam wartości
    return strat    # Zwracam napis mówiący o strategii


# # Przykład z wykładu
# y = 7  # maksymalna pojemność
# a = np.array([1, 2, 3])  # t/szt
# b = np.array([6, 3, 2])  # szt
#
# q = np.array([[20, 9, 6],
#      [18, 6, 2],
#      [14, 3, 0],
#      [11, 0, None],
#      [7, None, None],
#      [2, None, None],
#      [0, None, None]],dtype=object)  # macierz kary

###########################
# y = 30  # maksymalna pojemność
# a = np.array([1, 2, 3, 4, 5, 6]) # t/szt
# b = np.array([6, 3, 2, 3, 5, 4])  # szt
#
# q = np.array([[20, 9, 6, 4,15,16],
#      [18, 6, 2, 2,13,12],
#      [14, 3, 0, 1,10,8],
#      [11, 0, None,0,7,4],
#      [7, None, None, None,2,0],
#      [2, None, None, None,0,None],
#      [0, None, None, None,None,None]],dtype=object) # macierz kary

y = 70

a = np.array([7, 4, 2, 3, 5, 7, 1, 7, 2, 2])

b = np.array([8, 1, 9, 3, 4, 4, 9, 5, 6, 7])

q = np.array([[40, 30, 27, 40, 44, 26, 84, 54, 30, 60],
              [35, 0, 24, 30, 33, 20, 72, 40, 28, 55],
              [30, None, 21, 20, 20, 13, 63, 32, 24, 45],
              [25, None, 18, 0, 7, 4, 51, 22, 20, 37],
              [20, None, 15, None, 0, 0, 46, 12, 12, 23],
              [15, None, 12, None, None, None, 32, 0, 4, 16],
              [10, None, 9, None, None, None, 22, None, 0, 8],
              [5, None, 6, None, None, None, 17, None, None, 0],
              [0, None, 3, None, None, None, 9, None, None, None],
              [None, None, 0, None, None, None, 0, None, None, None]])

if __name__ == '__main__':
    print(f'Ograniczenie zasobowe [t] : {y}\n')
    print(f'Wektor a [t/szt] : {a}\n')
    print(f'Wektor b [szt] : {b}\n')
    print(f'Macierz kar q : \n{q}\n')

    m, f = CPD_method(y, a, b, q)

    print(f"Macierz xi  \n{m}\n\nMacierz f(yi) \n{f}")
    print("\nOptymalna strategia\n", strategy(a, y, m, f))
