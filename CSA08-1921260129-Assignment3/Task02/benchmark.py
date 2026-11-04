import csv
import sys
import time
from pathlib import Path


def elapsed(function, repeats=5):
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        function()
        samples.append(time.perf_counter() - start)
    return min(samples)


def main():
    n = 1_000_000
    base = range(n)
    list_create = elapsed(lambda: list(base))
    tuple_create = elapsed(lambda: tuple(base))
    values_list = list(base)
    values_tuple = tuple(values_list)
    indexes = [0, n // 4, n // 2, 3 * n // 4, n - 1] * 20_000
    list_index = elapsed(lambda: [values_list[i] for i in indexes])
    tuple_index = elapsed(lambda: [values_tuple[i] for i in indexes])
    out = Path(__file__).parent / 'outputs' / 'tuple_list_benchmark.csv'
    out.parent.mkdir(exist_ok=True)
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['n','list_create_seconds','tuple_create_seconds','list_index_seconds','tuple_index_seconds','list_shallow_bytes','tuple_shallow_bytes'])
        w.writerow([n, list_create, tuple_create, list_index, tuple_index, sys.getsizeof(values_list), sys.getsizeof(values_tuple)])
    print(f'n={n:,} list_create={list_create:.6f}s tuple_create={tuple_create:.6f}s')
    print(f'indexing 100,000 fixed indexes: list={list_index:.6f}s tuple={tuple_index:.6f}s')
    print('shallow bytes:', sys.getsizeof(values_list), sys.getsizeof(values_tuple))


if __name__ == '__main__':
    main()
