import csv
import sqlite3
from pathlib import Path
from TaskA5.ai_app import label

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "inputs"
OUT = Path(__file__).resolve().parent / "outputs"
REQUIRED = {"station", "date", "hour", "pm25"}


def inspect_file(path):
    path = Path(path)
    if path.stat().st_size == 0:
        return "EMPTY: no records"
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
        encoding = "utf-8"
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
        encoding = "latin-1 fallback"
    sample = text[:2048]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = ","
    rows = list(csv.DictReader(text.splitlines(), delimiter=delimiter))
    header = set(rows[0].keys()) if rows else set()
    missing = REQUIRED - header
    if missing:
        return f"INVALID HEADER: missing {sorted(missing)} | encoding={encoding} delimiter={repr(delimiter)}"
    return f"READABLE: rows={len(rows)} | encoding={encoding} delimiter={repr(delimiter)}"


def sql_injection_demo():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE stations(station TEXT, pm25 REAL)")
    con.executemany("INSERT INTO stations VALUES (?, ?)", [("Adyar", 48), ("Guindy", 95), ("Velachery", 58)])
    payload = "Adyar' OR '1'='1"
    unsafe = con.execute(f"SELECT station, pm25 FROM stations WHERE station = '{payload}'").fetchall()
    safe = con.execute("SELECT station, pm25 FROM stations WHERE station = ?", (payload,)).fetchall()
    con.close()
    return unsafe, safe


def main():
    OUT.mkdir(exist_ok=True)
    lines = []
    for path in sorted(FIXTURES.iterdir()):
        lines.append(f"{path.name}: {inspect_file(path)}")
    unsafe, safe = sql_injection_demo()
    lines.append(f"Unsafe concatenated query rows: {unsafe}")
    lines.append(f"Safe parameterised query rows: {safe}")
    adversarial = ["Great, another day of toxic air.", "Not bad, not good either.",
                   "The service is good but the air is dirty.", "I do not dislike the improvement."]
    for item in adversarial:
        lines.append(f"Sentiment={label(item):8} | {item}")
    (OUT / "adversarial_results.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
