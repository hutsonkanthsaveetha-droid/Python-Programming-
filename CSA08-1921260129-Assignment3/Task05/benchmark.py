import csv
import random
import sys
import time
from pathlib import Path
from Task05.sensor_cleaning import clean_loop, clean_comprehension, clean_map_filter


def timed(fn, repeats=3):
    values = []
    for _ in range(repeats):
        start = time.perf_counter(); fn(); values.append(time.perf_counter() - start)
    return min(values)


def main():
    rows = []
    for n in (10_000, 100_000, 1_000_000):
        rng = random.Random(500 + n)
        readings = [rng.uniform(-60, 60) for _ in range(n)]
        loop_time = timed(lambda: clean_loop(readings))
        comp_time = timed(lambda: clean_comprehension(readings))
        map_time = timed(lambda: clean_map_filter(readings))
        same = clean_loop(readings) == clean_comprehension(readings) == clean_map_filter(readings)
        rows.append((n, loop_time, comp_time, map_time, same))
        print(f'n={n:>9} loop={loop_time:.6f}s comprehension={comp_time:.6f}s map/filter={map_time:.6f}s equal={same}')
    sample = [float(x) for x in range(1000)]
    list_result = [x for x in sample if -50 <= x <= 50]
    generator_result = (x for x in sample if -50 <= x <= 50)
    print('memory shallow bytes: list=', sys.getsizeof(list_result), 'generator=', sys.getsizeof(generator_result))
    out = Path(__file__).parent / 'outputs' / 'sensor_benchmark.csv'; out.parent.mkdir(exist_ok=True)
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f); w.writerow(['n','loop_seconds','comprehension_seconds','map_filter_seconds','same_result']); w.writerows(rows)


if __name__ == '__main__':
    main()
