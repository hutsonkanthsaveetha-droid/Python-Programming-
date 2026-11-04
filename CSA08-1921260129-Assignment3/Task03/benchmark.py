import csv
import random
import time
from collections import Counter
from pathlib import Path
from Task03.complaints import frequencies_get, list_count_method, STOP_WORDS

VOCAB = ['seed', 'fertiliser', 'water', 'price', 'delayed', 'crop', 'paddy', 'banana', 'subsidy', 'payment',
         'quality', 'supply', 'field', 'loan', 'weather', 'harvest', 'support', 'market', 'soil', 'pest']


def generate(n, seed=33):
    rng = random.Random(seed + n)
    return [' '.join(rng.choices(VOCAB, k=8)) for _ in range(n)]


def timed(fn):
    start = time.perf_counter()
    result = fn()
    return time.perf_counter() - start, result


def main():
    rows = []
    for n in (1_000, 10_000, 100_000):
        texts = generate(n)
        t_dict, d = timed(lambda: frequencies_get(texts, STOP_WORDS))
        t_counter, c = timed(lambda: Counter(word for text in texts for word in text.split() if word not in STOP_WORDS))
        t_list, l = timed(lambda: list_count_method(texts, STOP_WORDS))
        rows.append((n, len(d), t_dict, t_counter, t_list, d == dict(c), d == l))
        print(f'n={n:>6} distinct={len(d):>2} dict={t_dict:.6f}s Counter={t_counter:.6f}s list.count={t_list:.6f}s equal={d == dict(c) == l}')
    out = Path(__file__).parent / 'outputs' / 'complaints_benchmark.csv'
    out.parent.mkdir(exist_ok=True)
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['complaints','distinct_words','dict_seconds','counter_seconds','list_count_seconds','dict_counter_equal','dict_list_equal'])
        w.writerows(rows)


if __name__ == '__main__':
    main()
