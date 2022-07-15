from math import inf
# Planowana implementacja PERT, rozpoczęto jednak od CPM

def CPM (data):
    path = []

    for a in data:
        poprzednik = a['poprzednik']
        if not poprzednik:
            es = 0
            ef = a['czas trwania'] + es
        elif poprzednik:
            ef_list = [d['ef'] for d in data if d['czynność'] in poprzednik]
            es = max(ef_list)
            ef = es + a['czas trwania']
        a['ef'] = ef
        print (a)
    for idx, ak in enumerate(reversed(data)):
        if idx == 0:
            ak['lf'] = ak['ef']
        else:
            items = [item for item in data if ak['czynność'] in item['poprzednik']]
            durations = []
            for ditem in items:
                durations.append(ditem['ls'])
            ak['lf'] = min(durations)
        ak['ls'] = ak['lf'] - ak['czas trwania']
        ak['slack'] = ak['lf'] - ak['ef']

    for i in data:
        if i['slack'] == 0:
            path.append(i['czynność'])

    return path, ef




if __name__ == '__main__':

    # # Dobry
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

    # data = [ ('a', 3, []),('b', 4, ['a']),('c', 2, ['a']),('d', 5, ['b']),('e', 1, ['c']),('f', 2, ['c']),
    #          ('g', 4, ['d', 'e']),('h', 3, ['f', 'g'])]

    data = [
        {
            'czynność': 'a',
            "czas trwania": 3,
            "poprzednik": []
        },
        {
            'czynność': 'b',
            "czas trwania": 4,
            "poprzednik": ['a']
        },
        {
            'czynność': 'c',
            "czas trwania": 2,
            "poprzednik": ['a']
        },
        {
            'czynność': 'd',
            "czas trwania": 5,
            "poprzednik": ['b']
        },
        {
            'czynność': 'e',
            "czas trwania": 1,
            "poprzednik": ['c']
        },
        {
            'czynność': 'f',
            "czas trwania": 2,
            "poprzednik": ['c']
        },
        {
            'czynność': 'g',
            "czas trwania": 4,
            "poprzednik": ['d', 'e']
        },
        {
            'czynność': 'h',
            "czas trwania": 3,
            "poprzednik": ['f', 'g']
        }
    ]

    path, time = CPM(data)
    print(f'Znaleziona ścieżka krytyczna: {path}')
    print(f'Czas trwania: {time}')