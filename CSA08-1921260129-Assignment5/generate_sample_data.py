import csv
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
STATIONS = ["Adyar", "Guindy", "T Nagar", "Velachery", "Anna Nagar", "Tambaram", "Perungudi", "Mylapore", "Ambattur", "Porur", "Chromepet", "Sholinganallur"]
random.seed(42)
start = date(2026, 10, 1)
for index, station in enumerate(STATIONS):
    path = RAW / f"station_{index + 1:02d}.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["station", "date", "hour", "pm25", "pm10", "no2", "temperature", "temp_unit"])
        rows = []
        for day_num in range(30):
            d = start + timedelta(days=day_num)
            for hour in range(24):
                base = 25 + index * 2.2 + 9 * (hour in range(7, 11)) + 6 * (hour in range(18, 22)) + random.uniform(-7, 9)
                pm25 = round(max(2, base + 4 * (day_num % 5)), 2)
                pm10 = round(pm25 * random.uniform(1.55, 2.1), 2)
                no2 = round(9 + index * 1.1 + random.uniform(0, 35) + 4 * (hour in range(7, 10)), 2)
                temp_c = round(25 + 4 * (hour in range(12, 16)) + random.uniform(-2.5, 2.5), 2)
                unit = "F" if index in (10, 11) else "C"
                temp_value = round(temp_c * 9 / 5 + 32, 2) if unit == "F" else temp_c
                rows.append([station, d.isoformat(), hour, pm25, pm10, no2, temp_value, unit])
        # Deliberate source-quality problems for pipeline validation.
        if index == 0:
            rows[5][3] = "NA"
            rows[18][4] = ""
            rows[42][5] = -12
            rows[63][3] = 1500
            rows[85][0] = "  adyar "
            rows.append(rows[100].copy())
        if index == 1:
            rows[10][6] = "NA"
            rows[30][3] = -4
        if index == 2:
            rows[20][1] = "2026/10/01"  # invalid date format
        for row in rows:
            writer.writerow(row)
