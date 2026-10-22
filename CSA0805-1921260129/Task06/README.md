# Task 6 — Functions

`rate_per_litre(fat, snf)` returns a rate; `payout(litres, fat, snf)` returns a payment; `ten_day_total(payments)` returns a total. A return value can be reused, tested and combined; `print()` only displays a value and returns `None`. Parameters and variables created inside a function are local. Constants can be read from module scope, but functions should not mutate global rate settings; pass revised values as parameters instead. Each function has a docstring. A long script can repeat logic and is harder to test; lambdas are suitable for small expressions but are less readable for validation and multi-step calculations. Function-call overhead is constant per call, so total work remains O(n); for thousands of entries it is normally small compared with I/O and Decimal operations.

Run the demonstration from the project root with `python -m Task06.functions_demo`.
