import time
from io import StringIO


def build_plus(parts):
    text = ""
    for part in parts:
        text += part + ";"
    return text


def build_join(parts):
    return ";".join(parts) + ";" if parts else ""


def build_fstring(parts):
    return "".join(f"{part};" for part in parts)


def build_stringio(parts):
    buffer = StringIO()
    for part in parts:
        buffer.write(part)
        buffer.write(";")
    return buffer.getvalue()


def measure(size, repeats=3):
    parts = [f"Item{i}:Rs{i % 50}" for i in range(size)]
    methods = (("+=", build_plus), ("join", build_join), ("f-string + join", build_fstring))
    results = {}
    for label, function in methods:
        samples = []
        result = None
        for _ in range(repeats):
            start = time.perf_counter()
            result = function(parts)
            samples.append(time.perf_counter() - start)
        results[label] = (statistics_mean(samples), result)
    same = len({value[1] for value in results.values()}) == 1
    return same, {name: result[0] for name, result in results.items()}


def statistics_mean(values):
    return sum(values) / len(values)


def main():
    print("size,same_text,plus_avg_s,join_avg_s,fstring_avg_s")
    for size in (1_000, 10_000, 200_000):
        same, times = measure(size)
        print(f"{size},{same},{times['+=']:.6f},{times['join']:.6f},{times['f-string + join']:.6f}")
    sample = ["Call:10", "SMS:2", "Data:5"]
    print("sample:", build_join(sample))

if __name__ == "__main__":
    main()
