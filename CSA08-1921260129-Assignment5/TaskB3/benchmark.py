import cProfile
import csv
import io
import pstats
import sqlite3
import tempfile
import time
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent / "outputs"
OUT.mkdir(exist_ok=True)


def generate_csv(path, stations):
    start = date(2026, 1, 1)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["station", "date", "hour", "pm25"])
        for station_id in range(stations):
            station = f"S{station_id + 1:03d}"
            for day_no in range(365):
                day = (start + timedelta(days=day_no)).isoformat()
                for hour in range(24):
                    pm25 = round(8 + ((station_id * 7 + day_no * 3 + hour * 5) % 170) + (hour in range(7, 10)) * 8, 2)
                    writer.writerow([station, day, hour, pm25])


def python_group(path):
    sums, counts = defaultdict(float), defaultdict(int)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = (row["station"], row["date"])
            sums[key] += float(row["pm25"])
            counts[key] += 1
    return {key: sums[key] / counts[key] for key in sums}


def pandas_group(path):
    frame = pd.read_csv(path)
    result = frame.groupby(["station", "date"], sort=True)["pm25"].mean()
    return result.to_dict()


def sqlite_group(path):
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE readings(station TEXT, day TEXT, pm25 REAL)")
    load_start = time.perf_counter()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        batch = []
        for row in reader:
            batch.append((row["station"], row["date"], float(row["pm25"])))
            if len(batch) >= 10000:
                con.executemany("INSERT INTO readings VALUES (?, ?, ?)", batch)
                batch.clear()
        if batch:
            con.executemany("INSERT INTO readings VALUES (?, ?, ?)", batch)
    con.commit()
    load_time = time.perf_counter() - load_start
    query_start = time.perf_counter()
    result = con.execute("SELECT station, day, AVG(pm25) FROM readings GROUP BY station, day ORDER BY station, day").fetchall()
    query_time = time.perf_counter() - query_start
    con.close()
    return {(station, day): mean for station, day, mean in result}, load_time, query_time


def main():
    output = []
    profile_target = None
    for stations in (1, 12, 120):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / f"air_{stations}.csv"
            gen_start = time.perf_counter()
            generate_csv(path, stations)
            generation_time = time.perf_counter() - gen_start
            start = time.perf_counter(); py_result = python_group(path); py_time = time.perf_counter() - start
            start = time.perf_counter(); pd_result = pandas_group(path); pd_time = time.perf_counter() - start
            start = time.perf_counter(); sql_result, sql_load_time, sql_query_time = sqlite_group(path); sql_total = time.perf_counter() - start
            # Compare every result with a tolerance for floating-point summation order.
            keys = set(py_result) & set(pd_result) & set(sql_result)
            agree = len(keys) == len(py_result) == len(pd_result) == len(sql_result) and all(
                abs(py_result[k] - pd_result[k]) < 1e-9 and abs(py_result[k] - sql_result[k]) < 1e-9 for k in keys)
            output.append({"stations": stations, "rows": stations * 8760, "generation_s": generation_time,
                           "python_s": py_time, "pandas_s": pd_time, "sqlite_load_s": sql_load_time,
                           "sqlite_query_s": sql_query_time, "sqlite_total_s": sql_total, "groups": len(py_result), "all_agree": agree})
            if stations == 12:
                profile_target = path.read_bytes()
                profile_file = Path(tempfile.gettempdir()) / "assignment5_profile.csv"
                profile_file.write_bytes(profile_target)
    with (OUT / "benchmark_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(output[0]))
        writer.writeheader(); writer.writerows(output)
    # Profile a 12-station input. Keep the CSV only in the temporary location.
    profiler = cProfile.Profile(); profiler.enable(); python_group(profile_file); profiler.disable()
    with (OUT / "cprofile.txt").open("w", encoding="utf-8") as f:
        stats = pstats.Stats(profiler, stream=f).sort_stats("cumulative")
        stats.print_stats(15)
    profile_file.unlink(missing_ok=True)
    for row in output:
        print(row)
    print(f"Profile saved: {OUT / 'cprofile.txt'}")


if __name__ == "__main__":
    main()
