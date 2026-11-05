# B3 - Loops, pandas and SQL

The benchmark generator creates 365 × 24 = 8,760 hourly readings per station. Each method computes the mean PM2.5 for every `(station, date)` group. All three result dictionaries agreed within a 1e-9 tolerance for every tested size.

| Stations | Rows | Python loop | pandas groupby | SQLite load | SQLite GROUP BY query | Groups |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 8,760 | 0.0260 s | 0.0551 s | 0.0283 s | 0.0045 s | 365 |
| 12 | 105,120 | 0.3125 s | 0.3766 s | 0.5729 s | 0.0957 s | 4,380 |
| 120 | 1,051,200 | 2.6126 s | 1.3510 s | 3.2221 s | 0.8419 s | 43,800 |

`benchmark_results.csv` is the authoritative run record and includes generation time, Python time, pandas time, SQLite load time, SQLite query time, total SQL time and correctness flag. SQLite load is separated because a persistent database pays ingestion cost once, while later queries reuse stored data. This distinction matters: a fresh in-memory SQL build is slower overall, but the repeated `GROUP BY` operation is much cheaper than loading and aggregating every time.

`cprofile.txt` profiles the plain-Python method on the 12-station case. The dominant work is reading/parsing rows and converting PM2.5 to float before dictionary aggregation. For a one-time quick analysis Python loops have low setup cost on small files; pandas becomes faster at the million-row scale. For a daily automated report, SQLite is preferable after ingestion because it persists data, supports parameterised repeat queries and avoids loading the full dataset into each analysis process.

A running-sum/count dictionary is O(n) time and O(stations × days) space. Storing all readings and then calling `statistics.mean` is O(n) time but O(n) space. Both are linear in readings; the running aggregate is smaller when only group means are needed.
