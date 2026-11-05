from pathlib import Path
from fest import process_departments


if __name__ == '__main__':
    expected = ['CSE', 'ECE', 'EEE', 'MECH', 'CIVIL']
    base = Path(__file__).parent
    records, errors, summary = process_departments(base / 'input' / 'departments', base / 'output', expected)
    print(summary)
    print('Errors:')
    for row in errors:
        print(row[:3])
    print('Output files:')
    for path in sorted((base / 'output').iterdir()):
        print(path.name)
