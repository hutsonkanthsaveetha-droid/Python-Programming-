from reader import read_records
from stats import percentage, absent_three_days
from report import write_reports
from pathlib import Path

if __name__ == '__main__':
    rows = read_records(Path(__file__).resolve().parents[1] / 'input' / 'attendance.csv')
    p = percentage(rows); a = absent_three_days(rows)
    write_reports(p, a, Path(__file__).resolve().parents[1] / 'output_three_modules')
    print(p, a)
