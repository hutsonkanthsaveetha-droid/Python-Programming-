# Q1 - Decisions with Many Boundaries

The policy is evaluated at 100, 101, 200 and 201 units. The sample set contains eight households and tests ration-card and age conditions. `separate_if_decision` uses three independent checks with non-overlapping ranges; `elif_decision` returns exactly one decision. `overlapping_if_example` deliberately shows why broad independent tests can append two decisions (80 units with a ration card).

Design choice: an `if-elif-else` chain is clearest because eligibility categories are mutually exclusive. Chained comparisons make boundaries explicit.

Alternative: `match units` can dispatch on a `case` with guards; a list of k ordered upper limits searched linearly costs O(k) time per decision and O(k) storage. `if-elif` and guarded `match` use O(1) auxiliary space and at most O(k) checks.
