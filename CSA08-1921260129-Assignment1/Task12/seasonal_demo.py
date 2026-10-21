from decimal import Decimal
from milkrate import rate_per_litre, payout, money

def seasonal_payment(litres, fat, snf, season, ten_day_litres=0):
    """Calculate payment using seasonal rates and a >500 L ten-day bonus."""
    season = season.strip().lower()
    if season in {"april-june", "apr-jun", "summer"}:
        base = Decimal("32.00")
        fat_value = Decimal("0.45")
    else:
        # Assumption: outside April–June, use original rate card.
        base = Decimal("30.00")
        fat_value = Decimal("0.40")
    standard_snf_value = Decimal("0.30")
    rate = rate_per_litre(fat, snf, base, fat_value, standard_snf_value)
    quantity = Decimal(str(litres))
    bonus = Decimal("0.50") if Decimal(str(ten_day_litres)) > 500 else Decimal("0.00")
    return rate, money(quantity * (rate + bonus)), bonus

if __name__ == "__main__":
    cases = [
        (100, "3.50", "8.50", "April-June", 600),
        (100, "3.50", "8.50", "July-March", 600),
        (100, "4.23", "8.67", "April-June", 501),
        (100, "4.23", "8.67", "April-June", 500),
    ]
    for litres, fat, snf, season, ten_day_litres in cases:
        rate, amount, bonus = seasonal_payment(litres, fat, snf, season, ten_day_litres)
        print(f"{season:12} fat={fat} snf={snf} ten_day={ten_day_litres:3} rate={rate:5.2f} bonus={bonus:.2f}/L payment={amount:.2f}")
