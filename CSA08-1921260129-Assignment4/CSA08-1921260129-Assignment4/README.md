# CSA08 Assignment 4 – CO4

**Student:** J. Hutson Kanth  
**Register number:** 1921260129  
**Course:** Python Programming (CSA08)  
**Python version used for the included evidence:** Python 3.13.5  
**GitHub repository name:** `CSA08-1921260129-Assignment4`  

## Contents

- `Task01` – Diagnose and repair a mess-bill file processor; compare line-by-line and whole-file reading.
- `Task02` – Design a monthly attendance file processor with damaged-line reporting.
- `Task03` – Custom exceptions, specific error handling and the `except Exception: pass` misuse experiment.
- `Task04` – Reproduce and repair file-writing defects; preserve returns with append mode and an error log.
- `Task05` – Four organisations: one script, one imported module, three modules, and an `attendance` package.
- `Task06` – College-fest registration package with validation, duplicate removal, event reports and error logging.
- `report.docx` and `report.pdf` – Assignment report.
- `requirements.txt` – Third-party dependency list (none required).

## Run commands

Run these commands from this project folder using Python 3.12 or newer (tested with Python 3.13.5):

```bash
python Task01/repair_mess.py
python Task01/benchmark_memory.py
python Task02/attendance_processor.py
python Task03/attendance_errors.py
python Task03/misuse_demo.py
python Task04/forensics_demo.py
python Task04/library_returns.py
python Task05/single_script.py
python Task05/one_module/main.py
python Task05/three_modules/main.py
python Task05/package_demo.py
python Task06/run_fest.py
python -m unittest discover -s tests -v
```

## Libraries

Only Python standard-library modules are used (`csv`, `decimal`, `pathlib`, `os`, `tempfile`, `datetime`, `argparse`, `collections`, `unittest`, and related built-ins). No third-party packages are required.

## Evidence note

Each task folder contains the relevant sample inputs, generated outputs and selected output evidence. The included captures were generated in the Python 3.13.5 build environment. Execution times vary by computer.

