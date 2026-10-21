# Python Programming — Assignment 1

**Student:** J. Hutson Kanth  
**Register number:** 1921260129  
**Assignment:** Design, Implement and Validate a Payment Calculator for a Village Milk Co-operative  

## Project contents

- `milkrate.py` — calculation functions, rates, and validation.
- `Task01/` to `Task12/` — task explanations, code exercises, test cases, algorithm notes, and seasonal design.
- `Task09/test_calculator.py` — automated unit tests.
- `benchmark.py` — float versus Decimal timing experiment for 300, 6,000 and 150,000 payments.
- `report.md` — complete editable report draft.
- `GITHUB_SETUP.md` — Windows instructions for creating the required repository and making progressive commits.
- `report.docx` and `report.pdf` — formatted report copies.
- `evidence/` — generated terminal-style output captures and their raw text logs.

The output images were produced from actual runs of the included code in a Python 3.13.5 build environment. They are example output captures, **not screenshots taken from the student's own PC**. If the instructor specifically requires screenshots from a local Windows session, replace them when the PC is available.

## Run from this folder

```bat
python --version
python milkrate.py
python -m Task02.decimal_demo
python -m Task03.constants_demo
python Task04\expressions.py
python Task05\input_demo.py
python -m Task06.functions_demo
python -m Task07.test_import
python -m unittest Task09.test_calculator
python -m Task09.calculator
python benchmark.py
python -m Task12.seasonal_demo
```

If `python` is not recognised, try `py` in its place. All programs use the Python standard library; no third-party packages are needed.

## Submission checklist

1. Read and understand each task and be ready to explain the calculations and validation rules.
2. Confirm the valid SNF range, rounding policy, seasonal rates and bonus rule with the co-operative/lecturer; the report identifies assumptions where the assignment details are incomplete.
3. Review the benchmark table; timings depend on the machine and must be described as measurements from the environment that produced them.
4. Create a GitHub repository called `CSA08-1921260129-Assignment1`, upload these files and make meaningful progressive commits as requested by the instructor.
5. Add the real GitHub URL to the report cover page. No URL is filled in here because a repository has not been created or authenticated from this environment.
6. Follow the course's rules on permitted AI assistance and required acknowledgements.

## Design assumptions to verify

- SNF values are currently accepted from 6.0% to 10.0%.
- Fat and SNF readings are converted to nearest 0.1 percentage-point steps using `ROUND_HALF_UP`.
- Individual payment amounts are rounded to two decimals before being added to the ten-day total.
- For July–March, the demonstration uses the original rate card because no other rate card was provided.
- The seasonal bonus is ₹0.50 per litre when ten-day supply is strictly greater than 500 L; the demonstration applies it to the displayed current payment quantity. Confirm the business rule before operational use.

## References

- Python documentation, `decimal`: https://docs.python.org/3/library/decimal.html
- Python documentation, IDLE: https://docs.python.org/3/library/idle.html
- Turnitin, Similarity guidance: https://guides.turnitin.com/hc/en-us/articles/23713493434253-Understanding-the-similarity-score
