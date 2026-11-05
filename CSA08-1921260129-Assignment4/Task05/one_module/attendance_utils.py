import csv
from pathlib import Path


def read_records(path):
    with open(path, encoding='utf-8', newline='') as source:
        return list(csv.DictReader(source))


def percentage(records):
    counts = {}
    for row in records:
        counts.setdefault(row['register_number'], [0, 0])[0 if row['status'] == 'P' else 1] += 1
    return {reg: round(p / (p + a) * 100, 2) for reg, (p, a) in counts.items()}


def absent_three_days(records):
    by_student = {}
    for row in records:
        by_student.setdefault(row['register_number'], []).append((row['date'], row['status']))
    return sorted(reg for reg, days in by_student.items() if any(
        [s for _, s in sorted(days)][i:i+3] == ['A', 'A', 'A']
        for i in range(max(0, len(days)-2))))


def write_reports(records, output_dir):
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    (out / 'attendance_percentages.txt').write_text(str(percentage(records)), encoding='utf-8')
    (out / 'absent_three_days.txt').write_text('\n'.join(absent_three_days(records)), encoding='utf-8')
