def normalise(text):
    return "".join(text.strip().upper().split()).replace("-", "")


def is_valid(reg):
    if len(reg) not in (9, 10):
        return False
    state = reg[:2]
    district = reg[2:4]
    series = reg[4:-4]
    number = reg[-4:]
    return (
        len(state) == 2 and state.isalpha()
        and len(district) == 2 and district.isdigit()
        and len(series) in (1, 2) and series.isalpha()
        and len(number) == 4 and number.isdigit()
    )


def format_receipt(reg):
    if not is_valid(reg):
        raise ValueError("Invalid vehicle registration number")
    return f"{reg[:2]} {reg[2:4]} {reg[4:-4]} {reg[-4:]}"


SAMPLES = [
    "tn 09 ab 1234",
    "KA-01-M-0007",
    "Tn09Ab1234",
    "TN9AB1234",
    "TN 22 1234 AB",
    "MH-12-XY-9876",
]


def main():
    for raw in SAMPLES:
        reg = normalise(raw)
        status = "valid" if is_valid(reg) else "INVALID"
        receipt = f" | receipt: {format_receipt(reg)}" if is_valid(reg) else ""
        print(f"{raw:17} -> {reg:11} {status}{receipt}")
    nine = "TN09A1234"
    ten = "TN09AB1234"
    print("9-char s[-4:] and s[4:-4]:", nine[-4:], nine[4:-4])
    print("10-char s[-4:] and s[4:-4]:", ten[-4:], ten[4:-4])

if __name__ == "__main__":
    main()
