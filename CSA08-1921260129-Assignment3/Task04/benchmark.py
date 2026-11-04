import csv
import random
import time
from pathlib import Path


def time_contains(container, targets, repeats=3):
    values = []
    for _ in range(repeats):
        start = time.perf_counter()
        for target in targets:
            target in container
        values.append(time.perf_counter() - start)
    return min(values)


def nested_common(a, b):
    return {x for x in a for y in b if x == y}


def main():
    rows = []
    for n in (10_000, 100_000, 1_000_000):
        values = list(range(n))
        lookup = set(values)
        targets = [n - 1, n // 2, n // 3, -1] * 25
        t_list = time_contains(values, targets)
        t_set = time_contains(lookup, targets)
        rows.append((n, t_list, t_set, len(lookup)))
        print(f'n={n:>9} list membership={t_list:.6f}s set membership={t_set:.6f}s')
    rng = random.Random(42)
    a = set(rng.sample(range(20_000), 800))
    b = set(rng.sample(range(20_000), 900))
    t_nested = time_contains_nested = None
    start = time.perf_counter(); naive = nested_common(a, b); t_nested = time.perf_counter() - start
    start = time.perf_counter(); fast = a & b; t_intersection = time.perf_counter() - start
    print(f'nested common={t_nested:.6f}s set &: {t_intersection:.6f}s results_equal={naive == fast}')
    out = Path(__file__).parent / 'outputs' / 'set_benchmark.csv'
    out.parent.mkdir(exist_ok=True)
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['n','list_membership_seconds','set_membership_seconds','set_size']); w.writerows(rows)
    with open(Path(__file__).parent / 'outputs' / 'intersection_benchmark.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['left_size','right_size','nested_seconds','set_intersection_seconds','same_result']); w.writerow([len(a), len(b), t_nested, t_intersection, naive == fast])


if __name__ == '__main__':
    main()
