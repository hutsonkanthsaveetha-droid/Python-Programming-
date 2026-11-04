import copy
import sys


def change_first(values):
    values[0] = 99


def main():
    rows, cols = 3, 4
    bad = [[0] * cols] * rows
    bad[0][1] = 7
    good = [[0 for _ in range(cols)] for _ in range(rows)]
    good[0][1] = 7
    print('bad :', bad)
    print('good:', good)
    print('row identity:', bad[0] is bad[1], good[0] is good[1])
    print('row ids bad :', [id(row) for row in bad])
    print('row ids good:', [id(row) for row in good])

    stops = {(13.0827, 80.2707): 'Chennai Central', (13.0418, 80.2341): 'T. Nagar'}
    print('tuple key:', stops[(13.0418, 80.2341)])
    try:
        stops[[13.0418, 80.2341]] = 'Invalid key'
    except TypeError as error:
        print('list key error:', type(error).__name__)

    original = [[1, 2], [3, 4]]
    alias = original
    shallow_copy = copy.copy(original)
    slice_copy = original[:]
    deep_copy = copy.deepcopy(original)
    original[0][0] = 9
    original.append([5, 6])
    print('alias is original:', alias is original)
    print('shallow sees nested change:', shallow_copy[0][0])
    print('slice sees nested change:', slice_copy[0][0])
    print('deep copy unchanged:', deep_copy)
    values = [1, 2, 3]
    change_first(values)
    print('function changed caller list:', values)

    nested = ([1, 2], 'stop')
    nested[0].append(3)
    print('mutable item inside tuple:', nested)
    for (latitude, longitude), name in stops.items():
        print(f'{name}: {latitude:.4f}, {longitude:.4f}')

    values = list(range(1_000_000))
    tuple_values = tuple(values)
    print('container sizes for 1,000,000 references:')
    print('list bytes:', sys.getsizeof(values), '| tuple bytes:', sys.getsizeof(tuple_values))
    print('Note: sys.getsizeof reports shallow container size, not referenced objects.')


if __name__ == '__main__':
    main()
