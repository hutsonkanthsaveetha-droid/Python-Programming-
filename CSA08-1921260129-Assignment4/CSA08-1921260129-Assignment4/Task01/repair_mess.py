from decimal import Decimal, InvalidOperation
import csv


def process_mess_file(filename):
    total = Decimal('0.00')
    report_rows = []
    rejected = []

    with open(filename, 'r', encoding='utf-8', newline='') as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            try:
                parts = next(csv.reader([line]))
                if len(parts) != 3:
                    raise ValueError(f'expected 3 fields, found {len(parts)}')
                register_number, name, amount_text = (part.strip() for part in parts)
                if not register_number or not name:
                    raise ValueError('register number and name are required')
                amount = Decimal(amount_text)
                if not amount.is_finite() or amount < 0:
                    raise ValueError('amount must be a non-negative finite value')
            except (ValueError, InvalidOperation, csv.Error) as exc:
                rejected.append((line_number, line.rstrip('\n'), str(exc)))
                continue
            total += amount
            report_rows.append((register_number, name, amount))

    return report_rows, total, rejected


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', nargs='?', default=str(__import__('pathlib').Path(__file__).parent / 'input' / 'mess_oct.csv'))
    args = parser.parse_args()
    try:
        rows, total, rejected = process_mess_file(args.filename)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError) as exc:
        print(f'Cannot process {args.filename}: {exc}')
        return 1
    output_dir = __import__('pathlib').Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    with (output_dir / 'valid_bills.csv').open('w', encoding='utf-8', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(['register_number', 'name', 'amount'])
        writer.writerows(rows)
    with (output_dir / 'rejected_lines.csv').open('w', encoding='utf-8', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(['line_number', 'raw_line', 'reason'])
        writer.writerows(rejected)
    print('MESS BILL REPORT')
    for register_number, name, amount in rows:
        print(f'{register_number}  {name}  Rs.{amount:.2f}')
    print(f'Total: Rs.{total:.2f}')
    print(f'Rejected records: {len(rejected)}')
    for line_number, raw, reason in rejected:
        print(f'Line {line_number}: {reason} | {raw}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
