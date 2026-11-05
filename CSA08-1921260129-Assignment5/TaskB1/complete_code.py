import csv
import io

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Guindy,2026-10-04,1200
"""


def load_clean(text):
    rows = []
    reader = csv.DictReader(io.StringIO(text))
    for row in reader:
        value = (row.get("pm25") or "").strip().upper()
        if value in {"", "NA"}:
            continue
        try:
            pm25 = float(value)
        except ValueError:
            continue
        if pm25 < 0 or pm25 > 999:
            continue
        rows.append((row["station"], row["date"], pm25))
    return rows


def min_max(values):
    if not values:
        return []
    low, high = min(values), max(values)
    if low == high:
        return [0.0 for _ in values]
    return [round((value - low) / (high - low), 3) for value in values]


clean = load_clean(RAW)
print(clean)
print(min_max([pm for _, _, pm in clean]))
