# Task 2 design

**Input:** one UTF-8 CSV per date; each line is `register_number,date,status`, where status is P or A.

**Data model:** dictionary keyed by register number; each value stores present and absent counts.

**Outputs:** `attendance_summary.csv` (all students and percentages), `below_75_percent.csv`, and `damaged_lines.csv` (file and line number included).

**Modes:** open source files with `r`, use UTF-8 and line iteration; open reports with `w` and `csv.writer`; use `a` when extending a persistent log. `read()` is unnecessary because iteration keeps memory bounded.

## Pseudocode

```text
START
  create empty attendance dictionary and damaged-line list
  FOR each CSV file returned by pathlib.glob:
    TRY open file in read mode with UTF-8
      FOR each line with its line number:
        parse register, date and status
        IF fields are invalid: append file name, line number and reason; CONTINUE
        initialise counts for register if absent
        increment present or absent count
    HANDLE file-level errors and continue to next file
  WRITE summary and below-threshold CSV reports
  WRITE damaged-line CSV
STOP
```

## Trace

For `192311003,2026-10-03,X`, the row has three fields but status X is invalid. No attendance counter changes; `(day02.csv, 2, invalid status 'X')` is added to the damaged-line log.
