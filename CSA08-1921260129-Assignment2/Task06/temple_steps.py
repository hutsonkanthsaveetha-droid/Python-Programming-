from functools import lru_cache
import sys
import time

calls = 0

def ways_naive(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)

@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)


def ways_iterative(n):
    if n <= 1:
        return 1
    previous, current = 1, 1
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current


def call_count_naive(n):
    global calls
    calls = 0
    answer = ways_naive(n)
    return answer, calls


def call_count_memo(n):
    global calls
    calls = 0
    ways_memo.cache_clear()
    answer = ways_memo(n)
    return answer, calls


def main():
    print("Hand check:", [(n, ways_iterative(n)) for n in range(1, 7)])
    print("n,naive_answer,naive_calls,memo_answer,memo_calls")
    for n in (10, 20, 25, 30):
        naive_answer, naive_calls = call_count_naive(n)
        memo_answer, memo_calls = call_count_memo(n)
        print(f"{n},{naive_answer},{naive_calls},{memo_answer},{memo_calls}")
    print("recursion limit:", sys.getrecursionlimit())
    calls = 0
    try:
        print("naive(1000):", ways_naive(1000))
    except RecursionError as exc:
        print("naive(1000): RecursionError:", type(exc).__name__)
    ways_memo.cache_clear()
    calls = 0
    try:
        print("memo(1000):", ways_memo(1000))
    except RecursionError as exc:
        print("memo(1000): RecursionError:", type(exc).__name__)
    answer = ways_iterative(1000)
    print("iterative(1000): digits =", len(str(answer)), "last 12 digits =", str(answer)[-12:])

if __name__ == "__main__":
    main()
