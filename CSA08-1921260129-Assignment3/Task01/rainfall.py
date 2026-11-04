import csv
import random
from pathlib import Path


def generate_readings(days=365, seed=3103):
    rng = random.Random(seed)
    return [round(rng.uniform(0, 42), 1) if rng.random() > 0.18 else 0.0 for _ in range(days)]


def weekly_totals(readings, days_per_week=7):
    return [round(sum(readings[i:i + days_per_week]), 1) for i in range(0, len(readings), days_per_week)]


def moving_average_naive(readings, window=7):
    if window <= 0:
        raise ValueError('window must be positive')
    return [sum(readings[i:i + window]) / window for i in range(len(readings) - window + 1)]


def moving_average_running(readings, window=7):
    if window <= 0:
        raise ValueError('window must be positive')
    if len(readings) < window:
        return []
    current = sum(readings[:window])
    result = [current / window]
    for i in range(window, len(readings)):
        current += readings[i] - readings[i - window]
        result.append(current / window)
    return result


def save_readings(readings, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['day', 'rainfall_mm'])
        writer.writerows((day, value) for day, value in enumerate(readings, start=1))


def main():
    readings = generate_readings()
    save_readings(readings, Path(__file__).parent / 'inputs' / 'rainfall_365.csv')
    weeks = weekly_totals(readings)
    averages = moving_average_running(readings)
    complete_count = len(readings) // 7
    comparable = weeks[:complete_count] if complete_count else weeks
    wet = max(range(len(comparable)), key=comparable.__getitem__)
    dry = min(range(len(comparable)), key=comparable.__getitem__)
    dry_days = [day for day, value in enumerate(readings, start=1) if value == 0]
    print('Days:', len(readings), '| weekly groups:', len(weeks), '(last group may be partial)')
    print('First 5 weekly totals:', weeks[:5])
    print(f'Wettest comparable week: {wet + 1}, total={comparable[wet]:.1f} mm')
    print(f'Driest comparable week: {dry + 1}, total={comparable[dry]:.1f} mm')
    if len(readings) % 7:
        print(f'Partial final group: {weeks[-1]:.1f} mm over {len(readings) % 7} day(s)')
    print('7-day moving averages:', len(averages), '| first 5:', [round(x, 2) for x in averages[:5]])
    print('Dry days:', len(dry_days), '| first 15 day numbers:', dry_days[:15])
    print('Slices: readings[7:14]=', readings[7:14])
    print('readings[-7:]=', readings[-7:])
    print('readings[::7]=', readings[::7][:8], '...')


if __name__ == '__main__':
    main()
