from decimal import Decimal
from pathlib import Path


def total_with_read(filename):
    text = Path(filename).read_text(encoding='utf-8')
    total = Decimal('0.00')
    for line in text.splitlines():
        parts = line.split(',')
        if len(parts) == 3:
            try:
                total += Decimal(parts[2])
            except (InvalidOperation, ValueError):
                continue
    return total


if __name__ == '__main__':
    print(total_with_read('input/mess_oct.csv'))
