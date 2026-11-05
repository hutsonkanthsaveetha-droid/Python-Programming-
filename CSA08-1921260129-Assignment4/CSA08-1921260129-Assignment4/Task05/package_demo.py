from pathlib import Path
from attendance import read_records, percentage, absent_three_days, write_reports

if __name__ == '__main__':
    rows = read_records(Path(__file__).parent / 'input' / 'attendance.csv')
    p = percentage(rows); a = absent_three_days(rows)
    write_reports(p, a, Path(__file__).parent / 'output_package')
    print(p, a)
