# Python Programming - Assignment 3 (CO3)

**Student:** J. Hutson Kanth  
**Register number:** 1921260129  
**Repository name:** `CSA08-1921260129-Assignment3`  
**Python version used for the included runs:** Python 3.13.5  
**Libraries:** Assignment programs use the Python standard library. `matplotlib==3.10.8` was used only to generate the evidence charts included in this package.

## Project contents

- `Task01` - lists, slicing, weekly rainfall, moving averages and benchmarks.
- `Task02` - tuples, mutability, aliasing and copying.
- `Task03` - dictionaries, complaint frequencies, grouping and comparisons.
- `Task04` - sets, elective clashes, Venn diagrams and membership benchmarks.
- `Task05` - list comprehensions, map/filter, generators and sensor cleaning.
- `Task06` - nested railway timetable and station index.
- `Task07` - contact merging from first principles.
- `tests` - automated checks for core functions.
- `evidence` - generated terminal-style output captures, charts and diagrams.
- `report.docx` and `report.pdf` - editable and submission-ready report drafts.
- `report.md` - Markdown copy of the report.
- `requirements.txt` - chart-generation dependency information.

## Result summary by task

| Task | Result |
|---|---|
| Q1 | Weekly totals, wet/dry day summary and both 7-day moving-average implementations are produced; benchmark sizes are 365, 36,500 and 365,000. |
| Q2 | Tuple-key lookup works; the repeated-row bug is shown and the list-comprehension grid creates independent rows. |
| Q3 | The expected top words are `seeds`, `price`, `received`; district and crop complaint groups are generated. |
| Q4 | The intersection, symmetric difference and neither-registration lists match the expected small case. |
| Q5 | Loop, comprehension and map/filter outputs are equal; sensor alarms and conversions are produced. |
| Q6 | Five-train timetable queries match the station-index result, including unknown-station and non-running-day tests. |
| Q7 | Contacts sharing canonical phone numbers are merged; same-name contacts with different numbers remain separate. |

## Run each task

Run these commands from the project root:

```bash
python -m Task01.rainfall
python -m Task01.benchmark
python -m Task02.tuples_mutability
python -m Task02.benchmark
python -m Task03.complaints
python -m Task03.benchmark
python -m Task04.electives
python -m Task04.benchmark
python -m Task05.sensor_cleaning
python -m Task05.benchmark
python -m Task06.timetable
python -m Task06.benchmark
python -m Task07.contact_merge
python -m Task07.benchmark
python -m unittest tests.test_assignment3
```

## Evidence note

The PNG files in `evidence/` are terminal-style captures generated from program runs in Python 3.13.5.