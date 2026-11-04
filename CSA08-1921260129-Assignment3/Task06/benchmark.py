import csv
import random
import sys
import time
from pathlib import Path
from Task06.timetable import build_station_index, find_trains, query_index

STATIONS = ['Chennai', 'Katpadi', 'Jolarpettai', 'Bengaluru', 'Salem', 'Coimbatore', 'Erode', 'Trichy', 'Madurai', 'Villupuram', 'Tambaram', 'Arakkonam']
DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def generate(n, seed=606):
    rng = random.Random(seed + n)
    timetable = {}
    for i in range(n):
        stations = rng.sample(STATIONS, k=5)
        start_hour = rng.randrange(24)
        stops = []
        for j, station in enumerate(stations):
            minutes = (start_hour * 60 + j * 45) % 1440
            arrival = f'{minutes // 60:02d}:{minutes % 60:02d}'
            dep_minutes = (minutes + 3) % 1440
            departure = f'{dep_minutes // 60:02d}:{dep_minutes % 60:02d}'
            stops.append((station, arrival, departure))
        run_days = {day for day in DAYS if rng.random() < 0.75}
        timetable[str(10000 + i)] = {'name': f'Train {i}', 'stops': stops, 'days': run_days}
    return timetable


def timed(fn, repeats=5):
    values=[]
    for _ in range(repeats):
        start=time.perf_counter(); fn(); values.append(time.perf_counter()-start)
    return min(values)


def deep_size(obj, seen=None):
    if seen is None: seen=set()
    oid=id(obj)
    if oid in seen: return 0
    seen.add(oid)
    size=sys.getsizeof(obj)
    if isinstance(obj, dict):
        size += sum(deep_size(k, seen)+deep_size(v, seen) for k,v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(deep_size(x, seen) for x in obj)
    return size


def main():
    rows=[]
    for n in (100, 1_000, 10_000):
        data=generate(n); idx=build_station_index(data)
        direct=timed(lambda: find_trains(data, 'Chennai', 'Tue'))
        indexed=timed(lambda: query_index(idx, 'Chennai', 'Tue'))
        extra=deep_size(idx)
        rows.append((n, direct, indexed, extra, find_trains(data,'Chennai','Tue') == query_index(idx,'Chennai','Tue')))
        print(f'trains={n:>5} scan={direct:.6f}s indexed={indexed:.6f}s index_bytes={extra:,} equal={rows[-1][-1]}')
    out=Path(__file__).parent/'outputs'/'timetable_benchmark.csv'; out.parent.mkdir(exist_ok=True)
    with open(out,'w',newline='',encoding='utf-8') as f:
        w=csv.writer(f); w.writerow(['trains','scan_seconds','index_seconds','index_deep_bytes','same_results']); w.writerows(rows)


if __name__=='__main__': main()
