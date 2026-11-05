import csv
import logging
import sqlite3
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = Path(__file__).resolve().parent / "outputs"
OUT_DIR.mkdir(exist_ok=True)
DB_PATH = OUT_DIR / "air_quality.db"
CLEAN_CSV = OUT_DIR / "cleaned_readings.csv"
logging.basicConfig(filename=OUT_DIR / "cleaning.log", level=logging.INFO, format="%(levelname)s %(message)s")
REQUIRED = {"station", "date", "hour", "pm25", "pm10", "no2", "temperature", "temp_unit"}
LIMITS = {"pm25": (0, 999), "pm10": (0, 2000), "no2": (0, 1000), "temperature": (-50, 60)}


def number(value):
    if value is None or str(value).strip().upper() in {"", "NA", "N/A", "NULL"}:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def median_or_none(values):
    valid = [v for v in values if v is not None]
    return statistics.median(valid) if valid else None


def read_raw_files(folder):
    records, rejected, duplicate_keys = [], [], set()
    for path in sorted(Path(folder).glob("*.csv")):
        try:
            with path.open("r", newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                if not reader.fieldnames or not REQUIRED.issubset(set(reader.fieldnames)):
                    rejected.append((path.name, 1, "missing required column"))
                    continue
                for line_no, row in enumerate(reader, start=2):
                    try:
                        station = " ".join(row["station"].split()).title()
                        day = datetime.strptime(row["date"].strip(), "%Y-%m-%d").date().isoformat()
                        hour = int(row["hour"])
                        if not station or not 0 <= hour <= 23:
                            raise ValueError("invalid station or hour")
                        key = (station, day, hour)
                        if key in duplicate_keys:
                            rejected.append((path.name, line_no, "duplicate station/date/hour"))
                            continue
                        duplicate_keys.add(key)
                        values = {name: number(row[name]) for name in ("pm25", "pm10", "no2", "temperature")}
                        unit = (row["temp_unit"] or "C").strip().upper()
                        if values["temperature"] is not None and unit == "F":
                            values["temperature"] = (values["temperature"] - 32) * 5 / 9
                        elif unit not in {"C", "F"}:
                            values["temperature"] = None
                        for name, (low, high) in LIMITS.items():
                            value = values[name]
                            if value is not None and not low <= value <= high:
                                values[name] = None
                        records.append({"station": station, "date": day, "hour": hour, **values})
                    except (ValueError, AttributeError, KeyError) as exc:
                        rejected.append((path.name, line_no, str(exc)))
        except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as exc:
            rejected.append((path.name, 0, f"{type(exc).__name__}: {exc}"))
    return records, rejected


def clean_records(records):
    station_values = defaultdict(lambda: defaultdict(list))
    for record in records:
        for field in LIMITS:
            if record[field] is not None:
                station_values[record["station"]][field].append(record[field])
    medians = {station: {field: median_or_none(values.get(field, [])) for field in LIMITS}
               for station, values in station_values.items()}
    cleaned = []
    imputed = 0
    for record in records:
        item = dict(record)
        for field in LIMITS:
            if item[field] is None:
                item[field] = medians[item["station"]][field]
                imputed += 1
        if all(item[field] is not None for field in LIMITS):
            cleaned.append(item)
    return cleaned, imputed


def save_outputs(cleaned, rejected):
    fields = ["station", "date", "hour", "pm25", "pm10", "no2", "temperature"]
    with CLEAN_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows({"temperature": r["temperature"], **{k: r[k] for k in fields if k != "temperature"}} for r in cleaned)
    pm_values = [r["pm25"] for r in cleaned]
    low, high = min(pm_values), max(pm_values)
    mean = statistics.mean(pm_values)
    sd = statistics.pstdev(pm_values)
    with (OUT_DIR / "normalized_readings.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["station", "date", "hour", "pm25", "min_max", "z_score"])
        for r in cleaned:
            scaled = 0.0 if high == low else (r["pm25"] - low) / (high - low)
            zscore = 0.0 if sd == 0 else (r["pm25"] - mean) / sd
            writer.writerow([r["station"], r["date"], r["hour"], r["pm25"], round(scaled, 4), round(zscore, 4)])
    with (OUT_DIR / "rejected_rows.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "line", "reason"])
        writer.writerows(rejected)


def create_database(cleaned):
    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    con.executescript("""
        CREATE TABLE stations (station_id INTEGER PRIMARY KEY, station_name TEXT UNIQUE NOT NULL);
        CREATE TABLE readings (
            station_id INTEGER NOT NULL REFERENCES stations(station_id),
            day TEXT NOT NULL, hour INTEGER NOT NULL CHECK(hour BETWEEN 0 AND 23),
            pm25 REAL NOT NULL, pm10 REAL NOT NULL, no2 REAL NOT NULL, temperature_c REAL NOT NULL,
            PRIMARY KEY(station_id, day, hour)
        );
    """)
    con.executemany("INSERT INTO stations(station_name) VALUES (?)", [(s,) for s in sorted({r["station"] for r in cleaned})])
    id_map = dict(con.execute("SELECT station_name, station_id FROM stations").fetchall())
    con.executemany("INSERT INTO readings VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [(id_map[r["station"]], r["date"], r["hour"], r["pm25"], r["pm10"], r["no2"], r["temperature"]) for r in cleaned])
    con.commit()
    return con


def query_reports(con):
    adyar = con.execute("""SELECT AVG(r.pm25) FROM readings r JOIN stations s USING(station_id)
                          WHERE s.station_name=? AND r.day BETWEEN ? AND ?""", ("Adyar", "2026-10-01", "2026-10-31")).fetchone()[0]
    station_means = con.execute("""SELECT s.station_name, ROUND(AVG(r.pm25),2)
                                   FROM readings r JOIN stations s USING(station_id)
                                   GROUP BY s.station_name ORDER BY AVG(r.pm25) DESC""").fetchall()
    worst_hours = con.execute("""SELECT hour, ROUND(AVG(pm25),2) FROM readings
                                 GROUP BY hour ORDER BY AVG(pm25) DESC LIMIT 5""").fetchall()
    daily = con.execute("""SELECT s.station_name, r.day, MIN(r.pm25), MAX(r.pm25),
                           ROUND(AVG(r.pm25),2), COUNT(*)
                           FROM readings r JOIN stations s USING(station_id)
                           GROUP BY s.station_name, r.day ORDER BY s.station_name, r.day""").fetchall()
    with (OUT_DIR / "daily_summary.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["station", "date", "minimum", "maximum", "mean", "valid_readings"]); w.writerows(daily)
    with (OUT_DIR / "sql_results.txt").open("w", encoding="utf-8") as f:
        f.write(f"Adyar October mean PM2.5: {adyar:.2f}\n")
        f.write("Station averages (descending):\n")
        for row in station_means: f.write(f"{row[0]}: {row[1]}\n")
        f.write(f"Worst hours: {worst_hours}\n")
    return adyar, station_means, worst_hours


def make_charts(con):
    trend = pd.read_sql_query("""SELECT day, AVG(pm25) AS pm25 FROM readings GROUP BY day ORDER BY day""", con)
    stations = pd.read_sql_query("""SELECT s.station_name, AVG(r.pm25) AS pm25 FROM readings r
                                     JOIN stations s USING(station_id) GROUP BY s.station_name
                                     ORDER BY pm25 DESC""", con)
    scatter = pd.read_sql_query("SELECT temperature_c, pm25 FROM readings", con)
    hours = pd.read_sql_query("SELECT hour, AVG(pm25) AS pm25 FROM readings GROUP BY hour ORDER BY hour", con)
    charts = [
        (trend, "day", "pm25", "Daily PM2.5 Trend", "Date", "Mean PM2.5 (µg/m³)", "pm25_trend.png", "line"),
        (stations, "station_name", "pm25", "Station PM2.5 Comparison", "Station", "Mean PM2.5 (µg/m³)", "station_comparison.png", "bar"),
        (scatter, "temperature_c", "pm25", "Temperature and PM2.5", "Temperature (°C)", "PM2.5 (µg/m³)", "temperature_scatter.png", "scatter"),
        (hours, "hour", "pm25", "Average PM2.5 by Hour", "Hour of day", "Mean PM2.5 (µg/m³)", "hourly_air_quality.png", "bar"),
    ]
    for frame, x, y, title, xlabel, ylabel, filename, kind in charts:
        plt.figure(figsize=(9, 4.8))
        if kind == "line":
            plt.plot(frame[x], frame[y], marker="o", linewidth=1.5)
            if len(frame) > 10:
                plt.xticks(frame[x].iloc[::3], rotation=40, ha="right")
        elif kind == "bar" and x == "station_name":
            plt.barh(frame[x].astype(str), frame[y])
            plt.gca().invert_yaxis()
            xlabel, ylabel = ylabel, xlabel
        elif kind == "bar":
            plt.bar(frame[x].astype(str), frame[y])
        else:
            plt.scatter(frame[x], frame[y], alpha=0.15, s=9)
        plt.title(title); plt.xlabel(xlabel); plt.ylabel(ylabel); plt.grid(axis="y", alpha=0.25)
        plt.tight_layout(); plt.savefig(OUT_DIR / filename, dpi=150); plt.close()


def main():
    raw, rejected = read_raw_files(RAW_DIR)
    cleaned, imputed = clean_records(raw)
    save_outputs(cleaned, rejected)
    con = create_database(cleaned)
    queries = query_reports(con)
    make_charts(con)
    con.close()
    with (OUT_DIR / "before_after.txt").open("w", encoding="utf-8") as f:
        f.write("Before cleaning (raw source examples):\n")
        for path in sorted(RAW_DIR.glob("*.csv"))[:1]:
            with path.open("r", encoding="utf-8") as source:
                for _, line in zip(range(8), source): f.write(line)
        f.write("\nAfter cleaning (first 7 records):\n")
        for record in cleaned[:7]: f.write(str(record) + "\n")
    with (OUT_DIR / "pipeline_summary.txt").open("w", encoding="utf-8") as f:
        f.write(f"Raw parsed rows: {len(raw)}\nCleaned rows: {len(cleaned)}\nRejected rows: {len(rejected)}\nImputed numeric cells: {imputed}\n")
        f.write(f"Stations: {len({r['station'] for r in cleaned})}\n")
        f.write(f"Adyar mean PM2.5: {queries[0]:.2f}\n")
    print(f"Raw parsed rows: {len(raw)}")
    print(f"Cleaned rows: {len(cleaned)}")
    print(f"Rejected rows: {len(rejected)}")
    print(f"Imputed numeric cells: {imputed}")
    print(f"Adyar October mean PM2.5: {queries[0]:.2f}")
    print(f"SQLite database: {DB_PATH}")


if __name__ == "__main__":
    main()
