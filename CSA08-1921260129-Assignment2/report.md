# PYTHON PROGRAMMING - ASSIGNMENT 2 (CO2)

## Design, Implementation, Measurement and Validation of Control Flow and String Operations

**Student:** J. Hutson Kanth  
**Register number:** 1921260129  
**Repository:** `CSA08-1921260129-Assignment2` (URL to be inserted after GitHub creation)  
**Python version:** 3.13.5  
**Date prepared:** 2026-10-30

## Objective

This assignment applies decisions, loops, string manipulation, functions, parameters, scope, recursion and performance analysis through seven programming problems. The required progression is predict, design, implement, measure, analyse, evaluate, diagnose, redesign and validate.

## Q1 - Decisions with Many Boundaries (6 marks)

The eight pre-run cases cover 100, 101, 200 and 201 units, plus ration-card and age-over-80 variations. The rule is: up to 100 units receives full subsidy; 101-200 receives partial subsidy only with a ration card; above 200 receives the senior exception only when a household member is over 80; otherwise no subsidy.

| Household | Units | Ration card | Member >80 | Predicted decision |

|---|---:|---|---|---|

| H1 | 50 | No | No | Full subsidy |

| H2 | 100 | Yes | No | Full subsidy |

| H3 | 101 | No | No | No subsidy |

| H4 | 101 | Yes | No | Partial subsidy |

| H5 | 200 | Yes | No | Partial subsidy |

| H6 | 200 | No | Yes | No subsidy |

| H7 | 201 | No | No | No subsidy |

| H8 | 201 | No | Yes | Senior exception subsidy |

Both implementations are included. The separate-if version checks non-overlapping ranges and returns a list; the if-elif-else version returns one decision. The deliberate overlapping example (`units <= 100` and `units <= 200 and ration_card`) returns two results for 80 units with a ration card, demonstrating the original defect. Independent `if` statements are not inherently wrong, but overlapping predicates can both execute. An if-elif-else chain makes the mutually exclusive policy explicit. Combined Boolean conditions are easiest here because the rules are short and bounded; nested if would add indentation without clarifying the policy.

Alternative: `Task01/alternative_matchcase.py` implements Python 3.10+ `match` with guards. A lookup list of k upper limits searched in order costs O(k) time and O(k) stored entries; the if-elif and match approaches take up to O(k) checks and O(1) auxiliary storage.

Observed output: the two correct implementations agree for all eight cases; the overlap example returns `[Full subsidy, Partial subsidy]`.

## Q2 - Loops that Count Attempts (4 marks)

The while version suits an attempt limit that can change during execution; the for version is clearer for a fixed three attempts. Blank OTP strings are skipped before incrementing the count, so they do not consume an attempt. A correct OTP exits with `break`; blank input uses `continue`; `pass` demonstrates a no-op placeholder; loop `else` reports the lock when all attempts finish without `break`. Updating the count before checking blank input wrongly consumes an attempt. Not updating it for wrong non-blank input can cause an infinite while loop.

The changed rule uses five counted attempts only when the security question is answered correctly; otherwise it remains three. Recursive alternative processes one input and calls itself with the remaining entries and attempt allowance: O(a) time and O(a) stack space. Both iterative loops use O(a) time and O(1) auxiliary space.

## Q3 - Vehicle Registration Validator (6 marks)

The normaliser strips surrounding whitespace, removes internal spaces and hyphens, and converts to uppercase. Validation uses slices: two letters, two digits, one or two letters, then four digits. No regular expression is used in the required implementation. Receipt output groups the validated number as `TN 09 AB 1234`.

| Input | Normalised | Expected / observed |

|---|---|---|

| `tn 09 ab 1234` | `TN09AB1234` | Valid |

| `KA-01-M-0007` | `KA01M0007` | Valid |

| `Tn09Ab1234` | `TN09AB1234` | Valid |

| `TN9AB1234` | `TN9AB1234` | Invalid: district is not two digits |

| `TN 22 1234 AB` | `TN221234AB` | Invalid: expected group order |

| `MH-12-XY-9876` | `MH12XY9876` | Valid |

Strings are immutable: `upper()` returns a new string, so the original text stays unchanged unless the returned value is assigned. For a 9-character string, `s[-4:]` is the final four characters and `s[4:-4]` is one series character; for a 10-character string, the middle slice is two characters. Alternative regex: `re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg)`. Both slicing and regex validation scan O(L) characters; regex is compact while slicing makes each field visible.

## Q4 - Building Long Text: + or join? (6 marks)

The same statement is built with repeated `+=`, `";".join(parts) + ";"`, and an f-string per part followed by `join`. Each method was run three times at 1,000, 10,000 and 200,000 lines. The CSV in `data/q4_raw_timings.csv` records every run and the average. Timings below are from this package execution environment and are not universal; rerun on the submission PC if local measurements are expected.

| Lines | Method | Run 1 (s) | Run 2 (s) | Run 3 (s) | Average (s) |

|---:|---|---:|---:|---:|---:|

| 1000 | += | 0.000066 | 0.000058 | 0.000058 | 0.000061 |

| 1000 | join | 0.000010 | 0.000010 | 0.000009 | 0.000010 |

| 1000 | f-string + join | 0.000065 | 0.000045 | 0.000045 | 0.000052 |

| 10000 | += | 0.000816 | 0.000580 | 0.000837 | 0.000744 |

| 10000 | join | 0.000123 | 0.000086 | 0.000086 | 0.000098 |

| 10000 | f-string + join | 0.000741 | 0.000455 | 0.000455 | 0.000550 |

| 200000 | += | 0.012288 | 0.012928 | 0.012395 | 0.012537 |

| 200000 | join | 0.004201 | 0.002952 | 0.002636 | 0.003263 |

| 200000 | f-string + join | 0.016584 | 0.015969 | 0.014376 | 0.015643 |

All three outputs are equal and have the same total length for a given input. Strings are immutable, so repeated concatenation can copy prior characters and has O(T²) worst-case character-copy cost for an output of T characters. `join` makes one final string in O(T) time and uses O(T) output space plus O(n) references. CPython can optimise some `+=` patterns, so the observed timing may be closer than the theoretical worst case. The included `build_stringio` alternative uses `io.StringIO.write` for each part; writing directly to a file uses the same pattern. Both perform O(T) total writing work; StringIO holds the buffer in memory, while file output can keep working memory around the file buffer.

## Q5 - Functions, Parameters and Scope (7 marks)

A mutable default such as `order=[]` is evaluated once when the function is defined and reused between calls. The corrected function uses `order=None` and creates a fresh list inside the function. Three sequential customer orders are independent. Positional parameters are supplied by order, keyword parameters by name, and defaults make optional values available. `calculate_bill` returns both total and GST as a tuple. Local variables exist inside a function; global names belong to module scope and require `global` for reassignment; nonlocal names belong to an enclosing function and are updated with `nonlocal`. Global mutation is usually avoided because it creates hidden state and complicates testing. The default tuple is inspected with the actual Python attribute `add_item_buggy.__defaults__`.

Alternative code is included: `add_item_explicit(item, order)` receives the caller-owned list, while `make_order_adder()` returns a closure that stores a private order. Appending one item is amortised O(1); storing m items for one customer uses O(m) space.

## Q6 - Recursion and Its Limits (8 marks)

Let W(0)=W(1)=1 and W(n)=W(n-1)+W(n-2). Hand results are n=1..6: 1, 2, 3, 5, 8, 13. Plain recursion has overlapping subproblems and an exponential call count; memoisation stores each result and reduces distinct function calls to n+1 for a fresh cache. The recursion limit is printed and the memoised call for 1,000 is attempted so any `RecursionError` is visible. The iterative version is also run at 1,000 and keeps only two preceding values.

| n | Naive answer | Naive calls | Naive time (s) | Memo answer | Memo calls | Memo time (s) |

|---:|---:|---:|---:|---:|---:|---:|

| 10 | 89 | 177 | 0.000012 | 89 | 11 | 0.000007 |

| 20 | 10946 | 21891 | 0.001312 | 10946 | 21 | 0.000006 |

| 25 | 121393 | 242785 | 0.015052 | 121393 | 26 | 0.000018 |

| 30 | 1346269 | 2692537 | 0.170525 | 1346269 | 31 | 0.000036 |

Complexity: plain recursion O(φⁿ) time and O(n) stack; memoised recursion O(n) time and O(n) cache plus recursion stack; iterative DP O(n) time and O(1) auxiliary space. Raising the recursion limit can expose stack and reliability risks; the iterative version is selected for deployment at n=1,000.

## Q7 - Diagnose, Redesign and Validate (13 marks)

Selected program: the plain recursive temple-step counter from Q6. Diagnosis: both recursive branches recompute the same subproblems; the number of calls grows exponentially with n. Objective: return exactly the same count while reducing the number of operations to a linear pass and supporting n=1,000 without recursion. The redesign stores only the previous and current values and advances them once per step.

Prediction: for a given n, the iterative design will return the same integer with n-1 updates, use O(1) auxiliary memory and avoid recursion depth errors. The flowchart is `evidence/task07_flowchart.png`; pseudocode is in `data/q7_redesign_pseudocode.txt`.

| n | Answer | Naive calls | Naive time (s) | Iterative steps | Iterative avg time (s) |

|---:|---:|---:|---:|---:|---:|

| 20 | 10946 | 21891 | 0.001406 | 19 | 0.00000130 |

| 25 | 121393 | 242785 | 0.016974 | 24 | 0.00000124 |

| 30 | 1346269 | 2692537 | 0.176151 | 29 | 0.00000139 |

The redesigned results match the original answers at each common test input. The iterative version scales to 1,000 steps and avoids recursive call overhead. The original recursive version remains valuable for showing the recurrence on small values, but it is not suitable for large inputs because of repeated work and stack use. Measurements are machine-dependent; the raw rows are stored in `data/q7_raw_comparison.csv`.

## Testing and validation

The package includes unit tests for subsidy boundaries, the overlapping-if example, vehicle formats, string builders, independent order lists and the temple recurrence. Execute them with `python -m unittest discover -s tests -v`. The included test run is recorded in `evidence/unit_tests.txt`. Every task has a source file, output text and a terminal-style output image.

## Conclusion

The tasks show how structured decisions prevent overlapping outcomes, loops manage bounded attempts, string operations validate structured identifiers, `join` builds large output efficiently, safe defaults prevent shared mutable state, memoisation avoids repeated recursion, and iterative dynamic programming gives a robust large-input solution. The measurements and complexity analysis support the final design choice.

## References and tool disclosure

- Python documentation: Built-in Types (text sequence / str), Compound Statements, Functions, and `functools.lru_cache` — https://docs.python.org/3/
- Python `time.perf_counter()` documentation — https://docs.python.org/3/library/time.html
- This project was prepared with AI assistance; the student must review, understand, execute and acknowledge assistance according to course rules.
- Timing data and output captures are generated by the included programs in the preparation environment. Repeat them on the submission machine if the assignment requires student-local evidence.