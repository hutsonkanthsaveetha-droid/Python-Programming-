from decimal import Decimal

payments = ["33.40"] * 1000 + ["0.10"] * 3

def total_float(items):
    """Sum string amounts after converting to binary float."""
    total = 0.0
    for amount in items:
        total += float(amount)
    return total

def total_decimal(items):
    """Sum decimal strings exactly in base ten."""
    total = Decimal("0.00")
    for amount in items:
        total += Decimal(amount)
    return total

def total_paise(items):
    """Convert amounts to integer paise and sum."""
    return sum(int(Decimal(amount) * 100) for amount in items)

print("float  :", total_float(payments))
print("Decimal:", total_decimal(payments))
print("paise  :", total_paise(payments), "paise = Rs", Decimal(total_paise(payments)) / 100)
print(0.1 + 0.2 == 0.3, Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
print("Decimal(float('0.1')):", Decimal(float("0.1")))
