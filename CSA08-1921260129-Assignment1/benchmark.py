from decimal import Decimal
from time import perf_counter
import sys

def total_float(items):
    total = 0.0
    for x in items:
        total += float(x)
    return total

def total_decimal(items):
    total = Decimal("0.00")
    for x in items:
        total += Decimal(x)
    return total

def measure(n):
    items = ["33.40"] * n
    print(f"\nPayments: {n:,}")
    for label, func in (("float", total_float), ("Decimal", total_decimal)):
        start = perf_counter()
        result = func(items)
        elapsed = perf_counter() - start
        print(f"{label:7} total={result} elapsed={elapsed:.6f}s")
    print("sys.getsizeof(float 0.0):", sys.getsizeof(0.0))
    print("sys.getsizeof(Decimal('0.00')):", sys.getsizeof(Decimal("0.00")))

if __name__ == "__main__":
    for size in (300, 6000, 150000):
        measure(size)
