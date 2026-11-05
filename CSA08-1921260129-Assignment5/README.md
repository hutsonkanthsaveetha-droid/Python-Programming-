# Python Programming - Assignment 5 (CO5)

**Student:** J. Hutson Kanth  
**Register Number:** 1921260129  
**Assignment:** Data Acquisition, Cleaning, Analysis and AI Applications  
**GitHub repository:** `CSA08-1921260129-Assignment5`   
**Python used for the included runs:** 3.13.5

## Libraries

- Python standard library: `csv`, `sqlite3`, `statistics`, `logging`, `pathlib`, `datetime`, `collections`, `time`, `timeit`, `cProfile`, `pstats`, `re`, `unittest`.
- `pandas==2.2.3`
- `matplotlib==3.10.8`

Install the two third-party libraries with `python -m pip install -r requirements.txt`.

## Folder map

- `TaskA1` to `TaskA5`: Part A designs, storage model, cleaning/normalisation, chart design, debugging/profiling plan, sentiment, summariser and chatbot design.
- `TaskB1`: Full CSV cleaning pipeline, completed TODO program, SQLite creation/query, normalisation and four charts.
- `TaskB2`: Adversarial CSV/encoding/delimiter/empty-file tests and SQL injection demonstration.
- `TaskB3`: Reproducible 1/12/120-station year-scale benchmark, correctness comparison and cProfile output.
- `TaskB4`: 51-complaint sentiment evaluation, extractive summary, chatbot query and station/day index test.
- `data/raw`: Twelve synthetic station CSV files for October 2026. `generate_sample_data.py` recreates them using a fixed random seed.
- `tests`: Automated regression tests.

The air-quality readings are simulated teaching data, not official measurements from a city monitoring network. Included terminal PNGs are generated from recorded program output; replace them with captures from your own computer if your instructor specifically requires local screenshots.

## Run each task

Run commands from this project root (the directory containing this README):

| Task | Command | Result/evidence |
|---|---|---|
| A1 | Read `TaskA1/design.md` | CSV schema, SQLite tables, example questions and CSV-vs-SQL analysis |
| A2 | Read `TaskA2/design.md` | Missing/impossible/duplicate/unit rules, min-max and z-score design |
| A3 | Read `TaskA3/design.md` | Four chart choices and daily SQL summary design |
| A4 | `python -m TaskA4.debugging_profile` | Debugging demo and cProfile summary |
| A5 | `python -m TaskA5.ai_app` | Sentiment, extractive summary and example chatbot functions |
| B1 | `python -m TaskB1.cleaning_pipeline` | Cleaned CSV, SQLite DB, daily summary and four charts in `TaskB1/outputs` |
| B1 TODO | `python -m TaskB1.complete_code` | Matches the assignment's three-row and min-max expected output |
| B1 alternative | `python -m TaskB1.alternative_benchmark` | CSV streaming vs pandas timings/memory at 1K, 100K and 1M rows |
| B2 | `python -m TaskB2.adversarial_checks` and `python -m TaskB2.complete_code` | Adversarial files, SQL injection checks and completed executemany/parameterised-query TODO |
| B3 | `python -m TaskB3.benchmark` | 1/12/120-station benchmark, agreement check and cProfile output |
| B4 | `python -m TaskB4.decision` and `python -m TaskB4.complete_code` | 51-complaint agreement, both summary methods, index timing, chatbot and completed sentiment TODO (run B1 first) |
| Tests | `python -m unittest discover -s tests -v` | Regression-test results |

To recreate raw sample input files, run `python generate_sample_data.py` before B1.

## Current included run summary

- B1 parsed 8,639 valid-key records; 6 numeric cells were imputed and 2 rows were rejected (one duplicate and one invalid date).
- B1 generated the SQLite database, daily summary, normalised PM2.5 file and labelled line/bar/scatter charts.
- B2 confirms that the parameterised SQL query treats the injection string as data, while unsafe concatenation changes the query logic.
- B3 produced 8,760, 105,120 and 1,051,200 rows; Python, pandas and SQLite summaries agree at all three sizes.
- B4 lexicon agreement was 46/51 (90.2%) on the included reference-labelled sample. The first-five summary covered 13/15 top terms; frequency selection covered 9/15 on this sample. This is a small demonstration set, not a city-wide accuracy claim.

## Submission reminders

The assignment requires the actual GitHub link on the report cover and README, and at least one progressive commit per task. Create an empty GitHub repository named `CSA08-1921260129-Assignment5`. Review the generated programs and data, then use `PUBLISH_ASSIGNMENT5.bat` to create one commit per task and push. The link placeholder must be replaced with the actual repository URL before submission.

Benchmark results are specific to the Python 3.13.5 environment used for the included run.