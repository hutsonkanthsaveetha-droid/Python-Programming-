import time

naive_calls = 0

def ways_naive(n):
    global naive_calls
    naive_calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)


def call_count_naive(n):
    global naive_calls
    naive_calls = 0
    answer = ways_naive(n)
    return answer, naive_calls


def ways_iterative(n):
    if n <= 1:
        return 1
    previous, current = 1, 1
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current


def time_iterative(n, repeats=5):
    samples = []
    result = None
    for _ in range(repeats):
        start = time.perf_counter()
        result = ways_iterative(n)
        samples.append(time.perf_counter() - start)
    return result, sum(samples) / len(samples)


def main():
    print("Original Q6 naive recursion vs redesigned iterative DP")
    print("n,answer,naive_calls,naive_time_s,iterative_steps,iterative_avg_s")
    for n in (20, 25, 30):
        start = time.perf_counter()
        naive_answer, calls = call_count_naive(n)
        naive_time = time.perf_counter() - start
        iterative_answer, iterative_time = time_iterative(n)
        assert naive_answer == iterative_answer
        iterative_steps = max(0, n - 1)
        print(f"{n},{naive_answer},{calls},{naive_time:.6f},{iterative_steps},{iterative_time:.8f}")
    large_answer, large_time = time_iterative(1000)
    print("n=1000 iterative result digits:", len(str(large_answer)), "avg_s:", f"{large_time:.8f}")

if __name__ == "__main__":
    main()
