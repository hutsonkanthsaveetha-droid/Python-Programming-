from decimal import Decimal
from milkrate import payout, rate_per_litre, ten_day_total, validate_entry

def calculate_record(farmer_id, litres, fat, snf, shift):
    """Validate a record and return a result dictionary."""
    valid, message = validate_entry(farmer_id, litres, fat, snf, shift)
    if not valid:
        raise ValueError(message)
    rate = rate_per_litre(fat, snf)
    amount = payout(litres, fat, snf)
    return {"farmer_id": str(farmer_id), "rate": rate, "amount": amount}

def main():
    """Read records until the clerk enters Q, then show the total."""
    amounts = []
    while True:
        farmer_id = input("Farmer ID (Q to finish): ").strip()
        if farmer_id.lower() == "q":
            break
        try:
            litres = Decimal(input("Litres: ").strip())
            fat = Decimal(input("Fat %: ").strip())
            snf = Decimal(input("SNF %: ").strip())
            shift = input("Shift (morning/evening): ").strip()
            result = calculate_record(farmer_id, litres, fat, snf, shift)
        except (ValueError, ArithmeticError) as error:
            print("Entry rejected:", error)
            continue
        print(f"{result['farmer_id']:>10}  rate Rs {result['rate']:6.2f}  payment Rs {result['amount']:8.2f}")
        amounts.append(result["amount"])
    print(f"Ten-day total: Rs {ten_day_total(amounts):.2f}")

if __name__ == "__main__":
    main()
