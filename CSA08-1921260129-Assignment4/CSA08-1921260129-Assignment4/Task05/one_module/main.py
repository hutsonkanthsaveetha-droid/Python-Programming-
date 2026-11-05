from pathlib import Path
from attendance_utils import read_records, write_reports, percentage, absent_three_days

if __name__ == '__main__':
    rows = read_records(Path(__file__).resolve().parents[1] / 'input' / 'attendance.csv')
    write_reports(rows, Path(__file__).resolve().parents[1] / 'output_one_module')
    print(percentage(rows), absent_three_days(rows))
