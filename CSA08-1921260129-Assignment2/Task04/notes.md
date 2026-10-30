# Q4 - Building Long Text

The program builds identical statements using repeated `+=`, a list plus `join`, and per-line f-strings followed by `join`. It measures 1,000, 10,000 and 200,000 records three times and stores raw timings in `data/q4_raw_timings.csv`. Timings are machine- and runtime-dependent; rerun on the submission PC.

Strings are immutable, so concatenation can copy accumulated content repeatedly and have O(T^2) worst-case character-copy cost for total output T. `join` assembles the final string in O(T) time and requires O(T) output plus O(n) references. `io.StringIO` or direct file writing can stream output and reduce the need to retain every fragment; file output uses buffering and O(buffer) working memory. CPython may optimise some `+=` loops, which is why measurements are included.
