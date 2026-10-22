# Task 1 — Problem analysis

Inputs: farmer ID (text identifier), quantity in litres (non-negative decimal), fat % (decimal, permitted 2.0–7.0), SNF % (decimal; assumed valid range 6.0–10.0 pending co-operative confirmation), and shift (Morning/Evening). Outputs: rate per litre, current payment, and accumulated ten-day total.

Constants: reference rate ₹30.00, reference fat 3.5%, reference SNF 8.5%, fat adjustment ₹0.40 per 0.1 percentage point, SNF adjustment ₹0.30 per 0.1 percentage point, and validation limits. These are named so a rate revision has one source of truth.

Types: farmer ID and shift are `str`; litres/fat/SNF are decimal measurements; step counts are `int`; validation results are `bool`; entries may be stored as tuples/dictionaries in a list; money uses `Decimal`.

Rules: reject nonnumeric input, negative litres, fat outside 2.0–7.0%, invalid shift, and (assumption) SNF outside 6.0–10.0%. Keep unrounded values until the specified billing stage and use a documented rounding rule. Assume one entry is one farmer's delivery for one shift and ten-day total is the sum of payment amounts.

Alternative: separate names such as `litres1`, `fat1`, `snf1` through `litres300` are hard to maintain and cannot be processed naturally in a loop. A list of records stores n entries in O(n) space and processes them in O(n) time; separate variables still require O(n) storage but cause code size and maintenance effort to grow with n. A record list scales because the same loop handles 300, 6,000 or 150,000 entries.
