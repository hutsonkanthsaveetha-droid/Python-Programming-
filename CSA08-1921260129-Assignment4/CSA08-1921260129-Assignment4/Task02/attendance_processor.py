from pathlib import Path
import csv


def process_month(input_dir, output_dir, threshold=75.0):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    counts = {}  # register -> [present, absent]
    damaged = []
    if not input_dir.is_dir():
        damaged.append((str(input_dir), 0, 'input directory is missing', ''))

    for file_path in sorted(input_dir.glob('*.csv')):
        try:
            with file_path.open('r', encoding='utf-8', newline='') as source:
                for line_number, line in enumerate(source, 1):
                    if not line.strip():
                        continue
                    try:
                        fields = next(csv.reader([line]))
                        if len(fields) != 3:
                            raise ValueError(f'expected 3 fields, found {len(fields)}')
                        reg, date_text, status = (value.strip() for value in fields)
                        if not reg or not date_text:
                            raise ValueError('register number and date are required')
                        if status not in {'P', 'A'}:
                            raise ValueError(f'invalid status {status!r}')
                    except (ValueError, csv.Error) as exc:
                        damaged.append((file_path.name, line_number, str(exc), line.rstrip('\n')))
                        continue
                    counts.setdefault(reg, [0, 0])
                    counts[reg][0 if status == 'P' else 1] += 1
        except (FileNotFoundError, PermissionError, UnicodeDecodeError) as exc:
            damaged.append((file_path.name, 0, f'{type(exc).__name__}: {exc}', ''))

    summary_path = output_dir / 'attendance_summary.csv'
    shortage_path = output_dir / 'below_75_percent.csv'
    damaged_path = output_dir / 'damaged_lines.csv'

    with summary_path.open('w', encoding='utf-8', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(['register_number', 'present', 'absent', 'valid_days', 'percentage'])
        for reg, (present, absent) in sorted(counts.items()):
            valid_days = present + absent
            percentage = (present / valid_days * 100) if valid_days else 0.0
            writer.writerow([reg, present, absent, valid_days, f'{percentage:.2f}'])

    with shortage_path.open('w', encoding='utf-8', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(['register_number', 'attendance_percentage'])
        for reg, (present, absent) in sorted(counts.items()):
            days = present + absent
            percentage = present / days * 100 if days else 0.0
            if percentage < threshold:
                writer.writerow([reg, f'{percentage:.2f}'])

    with damaged_path.open('w', encoding='utf-8', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(['file_name', 'line_number', 'reason', 'raw_line'])
        writer.writerows(damaged)

    return counts, damaged, (summary_path, shortage_path, damaged_path)


if __name__ == '__main__':
    base = Path(__file__).parent
    counts, damaged, paths = process_month(base / 'input' / 'daily', base / 'output')
    print(f'Students: {len(counts)} | damaged lines: {len(damaged)}')
    for path in paths:
        print(path)
