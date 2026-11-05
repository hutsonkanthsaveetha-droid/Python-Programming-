# A4 - Debugging and profiling plan

## Debugging
- Print a few rows at the file boundary to inspect parsing, but remove or disable frequent prints in production.
- Use `assert` for internal invariants such as `0 <= hour <= 23`, non-negative cleaned measurements and unique station/date/hour keys; assertions are development checks, not a substitute for input validation.
- Use `logging` at DEBUG for row-level diagnostics, INFO for accepted/rejected counts and WARNING for repaired records. Configure handlers/levels so verbose output can be disabled without editing processing logic.
- Use `pdb`/`breakpoint()` to pause at the first invalid conversion, inspect local variables and step through branches.

## Profiling
`time.perf_counter()` measures elapsed wall-clock time around a full cleaning stage. `timeit` repeats a small function to reduce noise. `cProfile` identifies cumulative function time and call counts; inspect the top cumulative-time functions before optimising. The accompanying `debugging_profile.py` demonstrates all three tools.

## Alternative: print-only debugging
Thousands of print calls perform formatting and terminal/file I/O and can dominate the measured runtime. Logging has configurable levels and handlers; set the level to WARNING/ERROR or disable the logger after debugging. A debugger pauses only at chosen breakpoints and is removed from normal execution. Time the production path with debugging output disabled to avoid measuring instrumentation overhead.
