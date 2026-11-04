import csv
import random
import time
from pathlib import Path
from Task01.rainfall import moving_average_naive, moving_average_running


def measure(function, data, repeats=3):
    values = []
    for _ in range(repeats):
        start = time.perf_counter()
        function(data)
        values.append(time.perf_counter() - start)
    return min(values)


def main():
    output = Path(__file__).parent / 'outputs' / 'rainfall_benchmark.csv'
    output.parent.mkdir(exist_ok=True)
    rows = []
    for size in (365, 36_500, 365_000):
        rng = random.Random(700 + size)
        data = [round(rng.uniform(0, 40), 1) for _ in range(size)]
        naive = measure(moving_average_naive, data)
        running = measure(moving_average_running, data)
        windows = max(0, size - 6)
        naive_additions = 7 * windows
        running_additions = 7 + max(0, size - 7)
        running_subtractions = max(0, size - 7)
        rows.append((size, windows, naive_additions, running_additions, running_subtractions, naive, running))
        print(f'n={size:>7} windows={windows:>7} naive_additions={naive_additions:>9} '
              f'rolling_additions={running_additions:>7} rolling_subtractions={running_subtractions:>7} '
              f'naive={naive:.6f}s running={running:.6f}s')
    with open(output, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['n_days','windows','naive_additions','running_additions','running_subtractions','naive_seconds','running_seconds'])
        w.writerows(rows)


if __name__ == '__main__':
    main()
