import csv
import sqlite3
import statistics
import time
from pathlib import Path

from TaskA5.ai_app import label, summarize, answer_question, tokens, STOP_WORDS

ROOT = Path(__file__).resolve().parents[1]
INPUT = Path(__file__).resolve().parent / "complaints.csv"
OUT = Path(__file__).resolve().parent / "outputs"
DB = ROOT / "TaskB1" / "outputs" / "air_quality.db"
OUT.mkdir(exist_ok=True)


def sentiment_check():
    results = []
    texts = []
    with INPUT.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            predicted = label(row["complaint"])
            agreed = predicted == row["reference_label"]
            results.append((row["id"], row["reference_label"], predicted, int(agreed), row["complaint"]))
            texts.append(row["complaint"])
    with (OUT / "sentiment_results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["id", "reference_label", "predicted_label", "agreed", "complaint"]); w.writerows(results)
    agreement = sum(row[3] for row in results)
    combined = " ".join(texts)
    frequency_summary = summarize(combined, 5)
    first_k_summary = " ".join(texts[:5])
    from collections import Counter
    important_counts = Counter(w for w in tokens(combined) if w not in STOP_WORDS)
    important_terms = [w for w, _ in important_counts.most_common(15)]
    def coverage(text):
        present = set(tokens(text))
        found = sum(1 for word in important_terms if word in present)
        return found, len(important_terms), found / len(important_terms) if important_terms else 0.0
    freq_cov = coverage(frequency_summary)
    first_cov = coverage(first_k_summary)
    (OUT / "complaint_summary.txt").write_text(f"FREQUENCY SUMMARY\n{frequency_summary}\n\nFIRST-FIVE BASELINE\n{first_k_summary}\n", encoding="utf-8")
    with (OUT / "summary_comparison.txt").open("w", encoding="utf-8") as f:
        f.write(f"Important-term coverage (top 15 terms):\nFrequency summary: {freq_cov[0]}/{freq_cov[1]} ({freq_cov[2]*100:.1f}%)\n")
        f.write(f"First-five baseline: {first_cov[0]}/{first_cov[1]} ({first_cov[2]*100:.1f}%)\n")
        f.write("Frequency summary selection scans/scorers words (O(W)); taking a fixed first k sentences is O(1) with respect to corpus length after the first k records are available.\n")
    return len(results), agreement, agreement / len(results) * 100, freq_cov, first_cov


def index_check():
    if not DB.exists():
        raise FileNotFoundError("Run TaskB1/cleaning_pipeline.py first to build the SQLite database")
    con = sqlite3.connect(DB)
    station_id = con.execute("SELECT station_id FROM stations WHERE station_name=?", ("Adyar",)).fetchone()[0]
    sql = "SELECT AVG(pm25) FROM readings WHERE station_id=? AND day BETWEEN ? AND ?"
    params = (station_id, "2026-10-01", "2026-10-30")
    # Measure the unindexed plan, then create the requested index and measure again.
    con.execute("DROP INDEX IF EXISTS idx_readings_station_day")
    before_plan = con.execute("EXPLAIN QUERY PLAN " + sql, params).fetchall()
    def measure():
        samples = []
        for _ in range(7):
            start = time.perf_counter()
            for _ in range(500): con.execute(sql, params).fetchone()
            samples.append((time.perf_counter() - start) / 500)
        return statistics.median(samples)
    before = measure()
    con.execute("CREATE INDEX idx_readings_station_day ON readings(station_id, day)")
    con.commit()
    after_plan = con.execute("EXPLAIN QUERY PLAN " + sql, params).fetchall()
    after = measure()
    con.close()
    return before, after, before_plan, after_plan


def main():
    count, agreed, percent, freq_cov, first_cov = sentiment_check()
    before, after, before_plan, after_plan = index_check()
    answer = answer_question("What is the PM2.5 in Adyar today?", DB)
    summary = [f"Complaints evaluated: {count}", f"Agreement with reference reading: {agreed}/{count} ({percent:.1f}%)",
               f"Query average before index: {before * 1000:.4f} ms", f"Query average after index: {after * 1000:.4f} ms",
               f"Index speed-up: {before / after:.2f}x" if after else "Index speed-up: n/a",
               f"Before query plan: {before_plan}", f"After query plan: {after_plan}",
               f"Frequency-summary coverage: {freq_cov[0]}/{freq_cov[1]} ({freq_cov[2]*100:.1f}%)",
               f"First-five coverage: {first_cov[0]}/{first_cov[1]} ({first_cov[2]*100:.1f}%)", f"Chatbot: {answer}"]
    (OUT / "decision_results.txt").write_text("\n".join(summary), encoding="utf-8")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
