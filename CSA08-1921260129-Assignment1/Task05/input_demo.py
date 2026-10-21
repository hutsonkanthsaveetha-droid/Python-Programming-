def read_number(prompt):
    """Read a numeric value, retrying after invalid text."""
    while True:
        text = input(prompt).strip()
        try:
            return float(text)
        except ValueError:
            print("Invalid number. Use a decimal point, e.g. 8.5.")

if __name__ == "__main__":
    litres = read_number("Litres: ")
    fat = read_number("Fat %: ")
    print(f"Litres: {litres:8.2f}  Fat: {fat:5.2f}%")
