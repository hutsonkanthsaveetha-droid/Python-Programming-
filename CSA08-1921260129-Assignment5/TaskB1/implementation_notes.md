# B1 - Cleaning pipeline implementation and results

For a compact package, the supplied source groups each station's month into one CSV file; the same columns apply to the daily files received by the board, and the pipeline scans every CSV in the folder. The source dataset contains 12 station CSV files with 30 days × 24 hours per station (8,640 nominal records) and deliberate quality defects: blank/`NA`, negative and >999 PM2.5, an invalid date, duplicate station/date/hour, non-normal station text and Fahrenheit temperatures at two stations. The pipeline validates schema and keys, normalises station/date/hour, converts Fahrenheit before plausibility checks, marks missing/impossible readings and fills them with a station-specific median. It writes rejected rows separately, then inserts cleaned readings with one `executemany` call.

The supplied TODO program uses `csv.DictReader` and skips missing, `NA`, negative and >999 values. It matches the brief's expected sample exactly: three tuples and min-max values `[0.0, 0.644, 1.0]`.

The full pipeline run parsed 8,639 valid-key rows, retained 8,639 after median filling, logged 2 rejected records (one duplicate and one malformed date) and imputed 6 numeric cells. It wrote the SQLite database, normalized CSV, daily summary and four labelled charts. Query outputs are stored in `outputs/sql_results.txt`.

## Measured csv versus pandas cleaning alternative

Measurements from this environment (`pandas` DataFrame storage is measured using `memory_usage(deep=True)`; standard-library peak is `tracemalloc` peak for streaming aggregation):

| Rows | CSV streaming time | CSV peak bytes | pandas time | pandas DataFrame bytes |
|---:|---:|---:|---:|---:|
| 1,000 | 0.0077 s | 45,253 | 0.0107 s | 119,132 |
| 100,000 | 0.8898 s | 49,038 | 0.0892 s | 11,900,132 |
| 1,000,000 | 9.7882 s | 48,958 | 0.9942 s | 119,000,132 |

The streaming loop uses almost constant additional memory because it retains only aggregates, while pandas stores the full DataFrame and is faster for this vectorised grouping. The trade-off is memory versus development speed and analytical flexibility.
