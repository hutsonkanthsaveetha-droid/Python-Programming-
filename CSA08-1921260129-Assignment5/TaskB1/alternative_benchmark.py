import csv
import tempfile
import time
import tracemalloc
from pathlib import Path

import pandas as pd

OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)


def generate(path, count):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["station", "date", "pm25"])
        for i in range(count):
            writer.writerow([f"S{i % 12 + 1:02d}", f"2026-10-{i % 30 + 1:02d}", (i % 250) + 1])


def stdlib_mean(path):
    totals, counts = {}, {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["pm25"] in {"", "NA"}:
                continue
            value = float(row["pm25"])
            key = row["station"]
            totals[key] = totals.get(key, 0.0) + value
            counts[key] = counts.get(key, 0) + 1
    return {key: totals[key] / counts[key] for key in totals}


def main():
    results = []
    for count in (1000, 100000, 1000000):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "readings.csv"
            generate(path, count)
            tracemalloc.start()
            start = time.perf_counter(); stdlib_mean(path); stdlib_time = time.perf_counter() - start
            _, stdlib_peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
            start = time.perf_counter()
            frame = pd.read_csv(path)
            frame["pm25"] = pd.to_numeric(frame["pm25"], errors="coerce")
            frame = frame.dropna(subset=["pm25"])
            pandas_mean = frame.groupby("station")["pm25"].mean().to_dict()
            pandas_time = time.perf_counter() - start
            pandas_bytes = int(frame.memory_usage(index=True, deep=True).sum())
            results.append({"rows": count, "stdlib_time_s": stdlib_time, "stdlib_peak_tracemalloc_bytes": stdlib_peak,
                            "pandas_time_s": pandas_time, "pandas_frame_bytes": pandas_bytes,
                            "groups": len(pandas_mean)})
            del frame
    with (OUT / "pandas_vs_csv.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0]))
        writer.writeheader(); writer.writerows(results)
    for result in results:
        print(result)


if __name__ == "__main__":
    main()
