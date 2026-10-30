# Python Programming - Assignment 2 (CO2)

**Student:** J. Hutson Kanth  
**Register number:** 1921260129  
**Repository:** `CSA08-1921260129-Assignment2`  
**Python version used for these runs:** Python 3.13.5

## Libraries
All programs use the Python standard library bundled with CPython 3.13.5 (including `time`, `sys`, `functools`, `dataclasses`, `io`, `unittest` and `csv`). No third-party runtime packages are required; `requirements.txt` records this runtime and module list.

## Run each task
Run commands from this project root:

| Task | Command | Result |
|---|---|---|
| Q1 | `python Task01/subsidy.py` and `python Task01/alternative_matchcase.py` | Compares separate `if`, `if-elif-else` and guarded `match-case` decisions at boundary values. |
| Q2 | `python Task02/otp_attempts.py` | Demonstrates while/for OTP attempts, blank input, break/continue/pass and loop-else. |
| Q3 | `python Task03/vehicle_number.py` | Normalises, validates and formats vehicle registration strings without regex. |
| Q4 | `python Task04/string_building.py` | Compares `+=`, `join` and f-string statement construction. |
| Q5 | `python Task05/functions_scope.py` | Demonstrates mutable defaults, parameters, return values and scope. |
| Q6 | `python Task06/temple_steps.py` | Compares naive recursion, memoisation and iterative DP for temple steps. |
| Q7 | `python Task07/redesign_validation.py` | Measures original recursion against the iterative redesign. |

Run automated tests:

```bash
python -m unittest discover -s tests -v
```

## Evidence and report
- `report.docx` and `report.pdf` contain the written Q1-Q7 analysis.
- `evidence/` contains terminal-style captures, the Q7 flowchart and a Q4 timing graph.
- `data/` contains the raw Q4 timings, Q6 function-call counts/timings and Q7 comparison results.
- Each Task folder contains its source, notes, output text and output image.

The recorded timings are from the Python 3.13.5 environment used to build this package. Execution times vary by machine.
