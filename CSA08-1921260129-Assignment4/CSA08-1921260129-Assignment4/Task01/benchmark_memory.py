from pathlib import Path
from decimal import Decimal, InvalidOperation
from statistics import mean
from tempfile import TemporaryDirectory
import time


def streaming(path):
    total = Decimal('0.00')
    with open(path, encoding='utf-8') as source:
        for line in source:
            parts = line.rstrip('\n').split(',')
            if len(parts) == 3:
                try:
                    total += Decimal(parts[2])
                except InvalidOperation:
                    continue
    return total


def whole(path):
    text = Path(path).read_text(encoding='utf-8')
    total = Decimal('0.00')
    for line in text.splitlines():
        parts = line.split(',')
        if len(parts) == 3:
            try:
                total += Decimal(parts[2])
            except InvalidOperation:
                continue
    return total


if __name__ == '__main__':
    with TemporaryDirectory() as folder:
        path = Path(folder) / 'mess.csv'
        path.write_text(''.join(f'{i},Student{i},1250.50\n' for i in range(50000)), encoding='utf-8')
        for function in (streaming, whole):
            times = []
            result = None
            for _ in range(3):
                start = time.perf_counter()
                result = function(path)
                times.append(time.perf_counter() - start)
            print(f'{function.__name__}: total={result:.2f}; runs=' + ', '.join(f'{value:.6f}s' for value in times))
            print(f'{function.__name__}: average={mean(times):.6f}s')
