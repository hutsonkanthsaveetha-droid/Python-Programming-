# Python Programming - Assignment 5 (CO5)
## Data Acquisition, Cleaning, Analysis and AI Applications

**Student:** J. Hutson Kanth  
**Register Number:** 1921260129  
**Course:** Python Programming (CSA08)  
**Python version for included execution:** 3.13.5  
**GitHub repository:** `CSA08-1921260129-Assignment5`  
**Total marks:** 50

## Objective and case study

The project demonstrates how raw station CSV files and citizen complaints can be acquired, inspected, cleaned, normalised, stored in SQLite, queried, visualised and interpreted. Twelve simulated Chennai air-quality stations provide hourly PM2.5, PM10, NO2 and temperature observations. The data intentionally includes blank and `NA` values, negative and impossible values, duplicate rows, a malformed date, inconsistent station text and Fahrenheit temperatures at two stations. A separate set contains 51 sample complaints.

**Data note:** All supplied measurements and complaints are synthetic teaching data created by `generate_sample_data.py`; they are not official measurements or real citizen submissions.

# PART A - Data and Program Design (25 marks)

## A1 - Design the data acquisition (7 marks)

The board can send one station/day CSV with one row per hour and columns `station,date,hour,pm25,pm10,no2,temperature,temp_unit`. Expected issues are missing columns/values, `NA` text, negative sensor values, out-of-range readings, duplicate station-date-hour keys, inconsistent casing/whitespace, malformed date/hour values, alternate encodings/delimiters and Fahrenheit temperatures.

**SQLite design:** `stations(station_id INTEGER PRIMARY KEY, station_name TEXT UNIQUE NOT NULL)` stores station metadata. `readings(station_id INTEGER REFERENCES stations, day TEXT, hour INTEGER, pm25 REAL, pm10 REAL, no2 REAL, temperature_c REAL, PRIMARY KEY(station_id, day, hour))` stores hourly observations. The composite key prevents duplicate measurements for the same station and hour. Station names map to `stations`; date, hour, pollutant values and converted temperature map to `readings`.

**Typical queries:**
1. Adyar's October mean PM2.5: filter one station and date range, then `AVG(pm25)`.
2. Compare station averages: group by station and order by mean PM2.5.
3. Identify the worst hours: group all readings by hour and order by mean PM2.5.

CSV is portable and convenient for one-time exchange; reading and parsing every file for each question costs O(n). pandas can make analysis concise but reads the data into memory (O(n)). SQLite has a one-time ingestion cost and persistent disk storage; indexed selection is approximately O(log n) plus matching rows and repeated queries do not need to reparse CSV files.

**Algorithm A1 - Import station files (SIMATS-style):**
- **Input:** Folder containing station CSV files.
- **Output:** Station table, reading table and rejected-row log.
- **BEGIN**
- Create the station and reading tables with primary and foreign keys.
- FOR each CSV file DO
  - Open using UTF-8 and a context manager; validate required headers.
  - FOR each row DO
    - Normalize station name; parse ISO date and hour.
    - Convert Fahrenheit to Celsius; validate numeric ranges and duplicate key.
    - Insert the station if new and insert the reading with parameter placeholders.
    - Write invalid or duplicate records to the rejected-row log.
  - END FOR
- END FOR
- Commit the transaction and close the database.
- **END**

## A2 - Design the cleaning and normalisation (5 marks)

| Problem | Rule | Reason |
|---|---|---|
| Blank / NA | Treat as missing; fill from station median, then global median if required | Median is robust to pollution spikes |
| Negative or impossible pollutant | Mark missing if PM2.5 outside 0-999, PM10 outside 0-2000 or NO2 outside 0-1000 | Fault values must not become observations |
| Fahrenheit | Convert `(F - 32) * 5 / 9` before temperature validation | Store one standard unit |
| Duplicate station/date/hour | Keep the first and log later copies | One station has one hourly record |
| Bad date/hour | Reject with file, line and reason | A malformed key cannot be grouped safely |

Min-max normalisation is `x' = (x - min) / (max - min)` and is suitable for a bounded 0-1 scale. If max equals min, return zero to avoid division by zero. Z-score standardisation is `z = (x - mean) / population_std_dev`; it expresses distance from the mean and is useful when comparing deviations. If standard deviation is zero, return zero. Dates use `YYYY-MM-DD`, station names are trimmed and title-cased, hours are integers 0-23, measurements are numeric and temperature is stored in Celsius.

Dropping missing values takes O(n) time and streaming O(1) extra space but can bias daily means if missingness is systematic. Forward fill is O(n). Median by sorting costs O(n log n) time and O(n) storage. This project uses station medians and records imputed/rejected counts.

## A3 - Design analysis and visualisation (5 marks)

| Question | Chart | Reason |
|---|---|---|
| PM2.5 trend over a month | Line | Shows chronological movement and peaks |
| Compare stations | Bar | Makes station ranking clear |
| Temperature vs PM2.5 | Scatter | Shows association and outliers without claiming causation |
| Hours with worst air | Bar by hour | Identifies recurring high-exposure periods |

The daily summary table contains station, date, minimum PM2.5, maximum PM2.5, mean PM2.5 and valid-reading count. SQL produces it with `MIN`, `MAX`, `AVG`, `COUNT` and `GROUP BY station_id, day`. A Python loop with a dictionary of running min/max/sum/count is also O(n) time and O(g) space for g station-day groups; the database performs aggregation near stored data.

## A4 - Debugging and profiling plan (4 marks)

- Use short print samples at parsing boundaries during development.
- Use assertions for internal invariants (hour range, non-negative cleaned values, unique keys); do not use assertions in place of input validation.
- Use `logging` levels: DEBUG for details, INFO for counts, WARNING for repairs and rejected rows. Set the level to WARNING in production.
- Use `pdb` or `breakpoint()` to inspect local variables and step through the first bad record.
- Use `time.perf_counter()` around a full stage, `timeit` for repeated functions and `cProfile` for cumulative function time and call counts.

The included debugging demo cleaned 10,000 values in about 0.0022 seconds for one `perf_counter` measurement; ten `timeit` runs took about 0.0153 seconds in this environment. The profile output is included. Thousands of print calls can add terminal I/O and formatting overhead; logging can be disabled by changing its level, and a debugger is used only at selected breakpoints.

## A5 - AI application for complaints (4 marks)

The lexicon assigns +1 to positive words and -1 to negative words; a preceding negator flips the next word's sign. The total maps to positive, negative or neutral. The extractive summariser counts important words after stop-word removal, scores each sentence by those word counts, and returns the top k original sentences. The rule-based chatbot detects `PM2.5` and a station name in a question, then uses a parameterised SQLite query for the latest available date.

Limitations include sarcasm, mixed opinions, double negation, out-of-vocabulary words, fixed question wording, lack of conversation context and non-live latest data. A trained Naive Bayes model requires labelled data and feature extraction; a language model may capture context better but costs more memory and compute. Any model must be evaluated on representative, multilingual complaints before production use.

# PART B - Implementation and Experimental Investigation (25 marks)

## B1 - Implement and validate the cleaning pipeline (7 marks)

The source folder contains twelve station files with 30 days × 24 hours per station. The full pipeline parsed 8,639 valid-key rows, produced 8,639 cleaned rows, imputed 6 numeric cells and rejected 2 records (a duplicate key and an invalid date). The cleaning script converts Fahrenheit before validation, applies station medians, writes a rejected-row file and loads SQLite with `executemany`.

The completed assignment TODO program matches the expected output exactly:

```text
[('Adyar', '2026-10-01', 48.0), ('Guindy', '2026-10-01', 95.0), ('Guindy', '2026-10-03', 121.0)]
[0.0, 0.644, 1.0]
```

The SQL output gives Adyar's October mean PM2.5 as 36.50. The highest station means are Sholinganallur 60.70, Chromepet 58.34 and Porur 56.27. The highest average PM2.5 hours are 09:00 (55.43), 08:00 (55.05), 07:00 (54.96), 10:00 (54.76) and 19:00 (52.55). The daily summary CSV and SQLite database are included.

**Chart interpretation:** The monthly trend chart shows day-to-day variation in the simulated network average. The station bar chart ranks Sholinganallur highest in this sample. The temperature scatter plot shows spread rather than a simple causal relationship. The hourly bar chart highlights morning hours as the highest average period in the generated data.

**CSV streaming versus pandas measurements:**

| Rows | CSV streaming time | CSV peak bytes | pandas time | pandas DataFrame bytes |
|---:|---:|---:|---:|---:|
| 1,000 | 0.0077 s | 45,253 | 0.0107 s | 119,132 |
| 100,000 | 0.8898 s | 49,038 | 0.0892 s | 11,900,132 |
| 1,000,000 | 9.7882 s | 48,958 | 0.9942 s | 119,000,132 |

The standard-library loop streams records and keeps only per-station totals/counts, so its additional memory remains near constant. pandas is much faster for the larger vectorised operation but holds the full DataFrame. The measurements are environment-specific.

## B2 - Engineer adversarial data (5 marks)

| Test | Observed response |
|---|---|
| Missing PM2.5 column | Header rejected with missing-column message |
| Semicolon delimiter | Sniffer detects `;` and reads the row |
| Latin-1 file | UTF-8 decode fails; Latin-1 fallback reads it |
| Empty file | Reported as empty without a crash |

Unsafe SQL concatenation with `Adyar' OR '1'='1` returns all demo rows. The parameterised query `WHERE station = ?` returns no match because the complete input is treated as one value. The lexicon returns neutral for sarcasm, double negation and mixed opinions in the adversarial examples; these are documented limitations, not hidden errors.

## B3 - Loops vs libraries vs SQL (8 marks)

The benchmark generator produces 8,760 readings per station (365 × 24 hours). All three approaches agreed within 1e-9 at every size.

| Stations | Rows | Python loop | pandas groupby | SQLite load | SQLite GROUP BY query |
|---:|---:|---:|---:|---:|---:|
| 1 | 8,760 | 0.0260 s | 0.0551 s | 0.0283 s | 0.0045 s |
| 12 | 105,120 | 0.3125 s | 0.3766 s | 0.5729 s | 0.0957 s |
| 120 | 1,051,200 | 2.6126 s | 1.3510 s | 3.2221 s | 0.8419 s |

SQLite load and query times are separated because the database load is a one-time or incremental ingestion cost, while the stored database supports repeat queries. At the largest size pandas was faster than the plain loop. The cProfile output contains 631,329 calls in 0.570 seconds for the 12-station profiling case; `python_group` consumed 0.570 cumulative seconds, and `csv.DictReader.__next__` consumed 0.413 cumulative seconds. This points to row parsing as the largest cost in that profile.

A running sum/count dictionary is O(n) time and O(stations × days) space. Retaining all values before calling `statistics.mean` is O(n) time and O(n) memory. The running aggregate is preferable if only means are needed.

## B4 - Final engineering decision (5 marks)

The complaint set contains 51 reference-labelled messages. The lexicon agreed with 46 labels (90.2%) on this prepared sample. This is not a city-wide accuracy estimate. The extractive summary is saved in `complaint_summary.txt` and the chatbot returned the latest available Adyar sample: 44.2 µg/m³ on 2026-10-30.

The query averaged 0.1284 ms before the explicit `(station_id, day)` index and 0.1381 ms after in the recorded run. The query plan already used SQLite's primary-key autoindex on `(station_id, day, hour)`, so the second index overlaps it and did not improve this query; it may add storage and write overhead. The measurement should be interpreted cautiously because it is a small, cache-sensitive query.

At the proposed scale, 100 new stations reporting every 15 minutes produce 100 × 96 = 9,600 readings/day (about 3.50 million/year). The practical design is incremental ingestion; schema, unit and range validation; deduplication by station/time; audit logs for repairs/rejections; SQLite for the current scale with indexed queries and backups; SQL for scheduled aggregation; pandas for exploratory analysis; and a trained, locally evaluated model with human escalation for 50,000 monthly complaints if the lexicon proves inadequate.

