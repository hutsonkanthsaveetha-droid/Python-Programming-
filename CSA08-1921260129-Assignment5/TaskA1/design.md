# A1 - Data acquisition and storage design

## Source CSV structure
The board can send one station/day CSV containing `station,date,hour,pm25,pm10,no2,temperature,temp_unit`; a row represents one hourly observation. For a compact downloadable fixture, the supplied sample groups one month per station in a single CSV, and the same folder reader processes multiple daily files. Expected defects include blank values, `NA` strings, negative sensor output, values outside physical/assignment limits, duplicate station-date-hour records, mixed station spelling/case, malformed dates/hours, inconsistent delimiters/encodings, and temperatures reported in Fahrenheit rather than Celsius.

## SQLite design
`stations(station_id INTEGER PRIMARY KEY, station_name TEXT UNIQUE NOT NULL)` stores one row per station. `readings(station_id INTEGER NOT NULL REFERENCES stations, day TEXT NOT NULL, hour INTEGER NOT NULL, pm25 REAL NOT NULL, pm10 REAL NOT NULL, no2 REAL NOT NULL, temperature_c REAL NOT NULL, PRIMARY KEY(station_id,day,hour))` stores hourly readings. The composite key prevents duplicate hourly observations. ISO dates (`YYYY-MM-DD`) sort chronologically. CSV station names map to `stations`; the remaining readings map to `readings`; Fahrenheit temperatures are converted before insertion.

## Example board questions
1. Adyar's October mean PM2.5: `SELECT AVG(pm25) ... WHERE station_name=? AND day BETWEEN ? AND ?`.
2. Rank stations by monthly mean: `GROUP BY station_name ORDER BY AVG(pm25) DESC`.
3. Find worst hours: `GROUP BY hour ORDER BY AVG(pm25) DESC`.

CSV is convenient for a one-time full scan and portable exchange. Re-reading all CSV files costs O(n) per question and requires parsing each time. SQLite has a one-time load cost, persistent storage and indexes; an indexed lookup is approximately O(log n) plus matching rows, and repeated queries avoid reparsing files. A pandas DataFrame loaded for every question also scans O(n) and consumes O(n) RAM; SQLite keeps the main data on disk.

## Acquisition pseudocode (SIMATS-style)
**Algorithm A1: ImportStationFiles**
- **Input:** Folder containing station CSV files.
- **Output:** Station and hourly-reading tables; rejected-row log.
- **BEGIN**
- Create SQLite station and reading tables with primary and foreign keys.
- FOR each CSV file in the folder DO
  - Open the file using UTF-8 encoding and a context manager.
  - Validate the required header columns.
  - FOR each row DO
    - Normalize station name and parse date/hour.
    - Validate fields; convert Fahrenheit to Celsius.
    - Insert station if it is new; insert reading with parameter placeholders.
    - Record invalid or duplicate rows in the rejected-row log.
  - END FOR
- END FOR
- Commit the transaction and close the database.
- **END**

## Alternative: CSV + pandas per question
Read all files with `pandas.read_csv`, concatenate, filter and aggregate for each query. Time is O(n) per query; DataFrame memory is O(n). This is flexible for exploration but inefficient for repeated operational queries compared with a persistent indexed database.
