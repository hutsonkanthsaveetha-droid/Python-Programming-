import cProfile
import logging
import pstats
import time
import timeit

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def clean_values(values):
    cleaned = [float(v) for v in values if v not in ("", "NA", None)]
    assert all(v >= 0 for v in cleaned), "negative reading reached clean output"
    logging.info("cleaned %d values", len(cleaned))
    return cleaned


def main():
    values = [str(i % 200) for i in range(10000)]
    start = time.perf_counter()
    result = clean_values(values)
    elapsed = time.perf_counter() - start
    repeated = timeit.timeit(lambda: clean_values(values), number=10)
    profiler = cProfile.Profile()
    profiler.enable()
    clean_values(values)
    profiler.disable()
    profiler.dump_stats("TaskA4/cleaning_profile.prof")
    with open("TaskA4/profile_summary.txt", "w", encoding="utf-8") as f:
        pstats.Stats(profiler, stream=f).sort_stats("cumulative").print_stats(10)
    print(f"cleaned={len(result)} perf_counter={elapsed:.6f}s timeit_10_runs={repeated:.6f}s")
    print("For interactive debugging, add: breakpoint() or run python -m pdb <script.py>.")


if __name__ == "__main__":
    main()
