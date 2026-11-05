from pathlib import Path
import csv


def read_records(path):
    with open(path, encoding='utf-8', newline='') as source:
        return list(csv.DictReader(source))


def percentage(records):
    counts = {}
    for row in records:
        item = counts.setdefault(row['register_number'], [0, 0])
        item[0 if row['status'] == 'P' else 1] += 1
    return {reg: round(p / (p + a) * 100, 2) for reg, (p, a) in counts.items()}


def absent_three_days(records):
    by_student = {}
    for row in records:
        by_student.setdefault(row['register_number'], []).append((row['date'], row['status']))
    result = []
    for reg, days in by_student.items():
        statuses = [status for _, status in sorted(days)]
        if any(statuses[i:i+3] == ['A', 'A', 'A'] for i in range(max(0, len(statuses)-2))):
            result.append(reg)
    return sorted(result)


def write_reports(records, output_dir):
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / 'attendance_percentages.txt').write_text(str(percentage(records)), encoding='utf-8')
    (output_dir / 'absent_three_days.txt').write_text('\n'.join(absent_three_days(records)), encoding='utf-8')


if __name__ == '__main__':
    sample = Path(__file__).parent / 'input' / 'attendance.csv'
    records = read_records(sample)
    write_reports(records, Path(__file__).parent / 'output_single')
    print(percentage(records))
    print(absent_three_days(records))
