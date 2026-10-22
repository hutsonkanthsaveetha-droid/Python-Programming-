from milkrate import rate_per_litre, payout, ten_day_total

def show_payment(farmer_id, litres, fat, snf):
    """Print a labelled payment record and return its amount."""
    rate = rate_per_litre(fat, snf)
    amount = payout(litres, fat, snf)
    print(f"{farmer_id:>8}  {litres:7} L  rate Rs {rate:6.2f}  amount Rs {amount:8.2f}")
    return amount

if __name__ == "__main__":
    amounts = [
        show_payment("F001", 10, 3.5, 8.5),
        show_payment("F002", 8.5, 4.2, 8.7),
    ]
    print("Total:", ten_day_total(amounts))
