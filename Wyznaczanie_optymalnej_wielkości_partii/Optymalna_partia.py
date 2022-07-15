# + własny przykład
import numpy as np
from math import inf


# Import pomocniczych bibliotek


def WPP(g, h, q, ymin, ymax, beg, end):
    # g - koszt produkcji
    # h - koszt składowania po rozpatrywanym kresie
    # Ymax - pojemność maksymalna magazynu
    # Ymin - pojemność minimalna magazynu
    # beg - stan początkowy
    # stan końcowy

    # Wylicenie różnicy - dostępna pojemność
    b = ymax - ymin

    # Utworzenie macierzy X ze stanami
    X = np.zeros((b + 1, len(q)))

    # Utworzenie macierzy f z kosztami
    f = np.full((b + 1, len(q)), np.inf)


    # I etap
    # DLa każdej wartości y w rzędzie
    for y in range(f.shape[0]):  # Dla każdej możliwej pojemności tk, od 0 do np.10
        x = q[f.shape[1] - 1][0] - (ymin+y) + end  # wyliczam stan x zgodnie z wzorami
        if x < 0 or x > ymax:  # Stan niedozwolony
            X[y][0] = None
            f[y][0] = inf
        else:       # Jeśli stan jest dozwolony, to wpisuję go do macierzy X
            X[y][0] = x     # A także jego koszt dodaję do macierzy f
            f[y][0] = g[x] + ymin


    # II etap
    counter = f.shape[1] - 2    # ustawiam licznik na kolejną wartość
    for i in range(1, f.shape[1]- 1):  # Dla wszystkich "środkowych kolumn"
        for y in range(f.shape[0]):  # Dla każdego y
            pot = list(range(ymax + 2))  # Tworzę listę z wszystkimi możiwościami
            idx_down = max(q[counter][0] - y, 0)  # Wybieram próg górny
            # Wybieram próg dolny
            idx_up = min(ymax + q[counter][0] - (ymin + y), len(g) - 1)
            newlist = []    # Tworzę nową listę na dozwolone wartości stanów
            for m in pot:  # Dla każdej wartości m w liście wartości pot
                if idx_down <= m <= idx_up: # Wybieram takie my (x-y), które mieszczą się
                    newlist.append(m)    # pomiędzy wyznaczonymi progami

            mini = inf   # Zmienna pomocnicza ustawiona na inf - najmniejsza wartść
            x_mini = 0   # Zmienna pomocnicza do szukania najmniejszego x
            for x in newlist:   # Dla każdego dozwolonego x w newlist
                # Do macierzy kosztów f wpisujemy wartość wyliczoną ze wzoru
                f[y][i] = g[x][0] + h[y + x - q[counter][0]][0] + f[y + x - q[counter][0]][i - 1]
                if f[y][i] < mini:   # Jeśli wyliczona wartość jest mniejsza od najmniejszej
                    mini = f[y][i]   # To wartość ta staje się wartością minimalną
                    x_mini = x      # A najmniejszy stan x, odpowiadający temu kosztowi zostaje
                    # najmniejszym x-em

            # Wprowadzam warunki, które nie mogą wystąpić
            if idx_down > idx_up or idx_up < 0 or idx_down < 0 or idx_up > len(g)-1:
                X[y][i] = None   # Jeśli jednak wystąpią, stan ustawiany jest na None
                f[y][i] = inf   # a jego koszt na inf - jest niedozwolone
            else:
                X[y][i] = x_mini # Jeśli jednak nie zachodzą warunki wykluczające, to
                f[y][i] = mini # do macierzy stanów trafia x_mini, a do macierzy kosztów f
                # trafia wartość minimalna z wyliczonych kosztów
        counter -= 1   # Licznik zmniejszam o jeden

    # Etap mógłby zostać zrealizowany wraz z etapem 2, ale dla przejrzystości,
    # Został zrealizowany osobno

    # III etap
    # Dla każdego y w rzędzie (y to nasza możliwa pojemność)
    for y in range(f.shape[0]):
        if y == beg - ymin:  # Jeśli y to nasza określona pojemność końcowa
            pot = list(range(ymax + 2))  # Tworzę listę możliwości pot
            idx_down = max(q[counter][0] - y, 0)  # Ponownie tworzę próg dolny i górny
            idx_up = min(ymax + q[counter][0] - (ymin + y), len(g) - 1) #Na podstawie wzorów
            newlist = [] # Tworzę listę na dozwolone x-y
            for m in pot: # Dla każdego m w liście pot
                if idx_down <= m <= idx_up:  # Jeśli m mieści się pomięzy progami
                    newlist.append(m)   # To do listy dozwolonych x dołączmy m

            mini = inf  # Zmienna pomocnicza ustawiona na inf - najmniejsza wartść
            x_mini = 0  # Zmienna pomocnicza do szukania najmniejszego x
            for x in newlist: # Dla każdego dozwolonego x dla danego y wyliczam wartość kosztu ze wzorów
                f[y][f.shape[1]-1] = g[x] + h[y + x - q[counter][0]][0] + f[y + x - q[counter][0]][f.shape[1]-2]
                if f[y][f.shape[1]-1] < mini:  # Jeśli wartość ta jest mniejsza od mini
                    mini = f[y][f.shape[1]-1]   # Staje się najmniejszą wartością
                    x_mini = x  # A odpowiadający jej x staje się minimalnym x-em

            # Sprawdzam spełnienie warunków (wcześniej również można było to zrobić)
            if idx_down > idx_up or idx_up < 0 or idx_down < 0 or idx_up > len(g) - 1:
                X[y][f.shape[1]-1] = None  # Jeśli warunki są spełnione, to oznacza to
                f[y][f.shape[1]-1] = inf  # Że stan nie jest dozwolony, a więc koszt i stan
                # Są oznaczone jako inf i None
            else:  # W przeciwnym razie, przypisujemy głównym macierzom koszt i stan
                X[y][f.shape[1]-1] = x_mini
                f[y][f.shape[1]-1] = mini
        else:   # Jeśli nie mamy do czynienia z odpowiednim stanem końcowym, to rzędy inne
            X[y][f.shape[1] - 1] = None # Niż szukane zostają uznane za niedozwolone
            f[y][f.shape[1] - 1] = inf  # Pomaga to w utrzymaniu pewnego porządku w kodzie
    return X, f


# Dobieranie strategii
def strategy(q, ymin, beg, X, f):
    yik = beg   # Początkową wartością staje się wartość zdeklarowana na początku
    strat = ''  # Tworzę pusty string
    # Iteruję od końca
    for i in range(f.shape[1] - 1, -1, -1):
        idx = f.shape[1] - i - 1  # Wyszukuję odpowiedni index (odpowiednik counter)x
        # Dodaję odpowiednie wartoścido stringa opisującego strategię
        strat += f"x{idx + 1} --> {int(X[yik - ymin, i])}\n y{idx} --> {yik}\n f{len(q)-1 - idx + 1}(y{idx}) = {f[yik - ymin, i]}\n\n"
        yik = int(yik + int(X[yik - ymin, i]) - q[idx][0]) # Wyliczam kolejną wartość kosztu minimalnego

    strat += f"Koszt całkowity: {f[beg - ymin, f.shape[1]-1]}\n" # Na końcu podaję koszt całkowity
    return strat  # I zwracam optymalną strategią

# |y0 = 0, x0 = 4|
# |y1 = 1, x1 = 5|
# |y2 = 3, x2 = 0|
# |y3 = 0, x3 = 4|
# |y4 = 1, x4 = 5|
# |y5 = 3, x5 = 0|
# |y6 = 0|

# g = np.array([[0],
#               [15],
#               [18],
#               [19],
#               [20],
#               [24]])
#
# h = np.array([[i * 2] for i in range(6)])
#
# q = np.array([[3],
#               [3],
#               [3],
#               [3],
#               [3],
#               [3]])
#
# Ymax = 4  # Y - pojemność magazynu maksymalna
# Ymin = 0  # ymin- pojemność magazynu minimalna
#
# beg = 0
# end = 0

# g = np.array([[2],
#               [8],
#               [12],
#               [15],
#               [17],
#               [20]])
#
# h = np.array([[1],
#               [2],
#               [2],
#               [4]])
#
# q = np.array([[4],
#               [2],
#               [6],
#               [5]])
#
# Ymin = 2
# Ymax = 5
# beg = 4
# end = 3

#
# g = np.array([[1],
#              [3],
#              [5],
#              [15],
#              [20],
#              [22],
#              [25],
#              [30],
#              [39]])
#
# h = np.array([[1],
#              [2],
#              [6],
#              [10],
#              [14],
#              [20],
#              [27]])
#
# q = [[3],
#      [2],
#      [7],
#      [5],
#      [8],
#      [7],
#      [4],
#      [2],
#      [3],
#      [10],
#      [3],
#      [8]]
#
# Ymin = 2
# Ymax = 7
# beg = 7
# end = 2
# #\

q = [[8],
     [2],
     [10],
     [3]]

h = np.array([[1],
             [7],
             [3],
             [4],
             [6],
             [5],
             [2]])

g = np.array([[2],
     [4],
     [7],
     [14],
     [23],
     [33],
     [36],
     [47]])

Ymin = 2
Ymax = 6
beg = 5
end = 3


if __name__ == '__main__':
    X, f = WPP(g, h, q, Ymin, Ymax, beg, end)
    #
    print(f"Macierz xi  \n{X}\n\nMacierz f(yi) \n{f}")
    print("\nOptymalna strategia\n",strategy(q, Ymin, beg, X, f))
