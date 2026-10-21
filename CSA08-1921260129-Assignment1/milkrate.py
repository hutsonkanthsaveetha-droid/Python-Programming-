"""Reusable payment calculations for the Ksheera milk co-operative.

Money is represented with Decimal to avoid binary floating-point errors.
The official rate is rounded to paise (two decimal places).
"""
from decimal import Decimal, ROUND_HALF_UP

BASE_RATE = Decimal("30.00")
REFERENCE_FAT = Decimal("3.5")
REFERENCE_SNF = Decimal("8.5")
FAT_STEP = Decimal("0.1")
SNF_STEP = Decimal("0.1")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
CENT = Decimal("0.01")

def money(value):
    """Return a monetary value rounded to the nearest paisa."""
    return Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)

def steps(reading, reference, step=Decimal("0.1")):
    """Count nearest 0.1-percentage-point steps from a reference reading."""
    reading = Decimal(str(reading))
    return int(((reading - reference) / step).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

def rate_per_litre(fat, snf, base_rate=BASE_RATE,
                   fat_step_value=FAT_STEP_VALUE,
                   snf_step_value=SNF_STEP_VALUE):
    """Return the per-litre rate rounded to two decimal places."""
    fat_steps = steps(fat, REFERENCE_FAT)
    snf_steps = steps(snf, REFERENCE_SNF)
    rate = (Decimal(str(base_rate))
            + Decimal(fat_steps) * Decimal(str(fat_step_value))
            + Decimal(snf_steps) * Decimal(str(snf_step_value)))
    return money(rate)

def payout(litres, fat, snf, base_rate=BASE_RATE,
           fat_step_value=FAT_STEP_VALUE,
           snf_step_value=SNF_STEP_VALUE):
    """Return one farmer's payment, rounded to the nearest paisa."""
    quantity = Decimal(str(litres))
    if quantity < 0:
        raise ValueError("Litres cannot be negative")
    return money(quantity * rate_per_litre(
        fat, snf, base_rate, fat_step_value, snf_step_value))

def ten_day_total(payments):
    """Sum already-calculated payment amounts and round the total to paise."""
    return money(sum((Decimal(str(p)) for p in payments), Decimal("0.00")))

def validate_entry(farmer_id, litres, fat, snf, shift):
    """Validate one entry; return (True, 'OK') or (False, reason)."""
    if not str(farmer_id).strip():
        return False, "Farmer ID is required"
    try:
        q, f, s = Decimal(str(litres)), Decimal(str(fat)), Decimal(str(snf))
    except (ValueError, TypeError, ArithmeticError):
        return False, "Litres, fat and SNF must be numeric"
    if not all(value.is_finite() for value in (q, f, s)):
        return False, "Litres, fat and SNF must be finite numbers"
    if q < 0:
        return False, "Litres cannot be negative"
    if not Decimal("2.0") <= f <= Decimal("7.0"):
        return False, "Fat must be between 2.0% and 7.0%"
    if not Decimal("6.0") <= s <= Decimal("10.0"):
        return False, "SNF must be between 6.0% and 10.0%"
    if str(shift).strip().lower() not in {"morning", "evening", "m", "e"}:
        return False, "Shift must be morning/evening (or M/E)"
    return True, "OK"

if __name__ == "__main__":
    for litres, fat, snf in [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]:
        rate = rate_per_litre(fat, snf)
        pay = payout(litres, fat, snf)
        print(f"{litres:5} L  fat {fat}  snf {snf}  rate {rate:6.2f}  pay {pay:8.2f}")
