from pathlib import Path
from datetime import datetime


def save_returns(books, log_path='returns.log'):
    with open(log_path, 'a', encoding='utf-8') as log:
        for book in books:
            log.write(book.rstrip('\n') + '\n')


def process(day_file, log_path='returns.log', error_log='errors.log'):
    try:
        with open(day_file, 'r', encoding='utf-8') as source:
            books = [line.rstrip('\n') for line in source if line.strip()]
        save_returns(books, log_path)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as exc:
        with open(error_log, 'a', encoding='utf-8') as errors:
            errors.write(f'{datetime.now().isoformat(timespec="seconds")} | {day_file} | {type(exc).__name__}: {exc}\n')
        print(f'Could not process {day_file}: {type(exc).__name__}')
        return False
    return True


def broken_save_returns(books, log_path):
    # Kept only to reproduce the assignment's original defects safely.
    log = open(log_path, 'w', encoding='utf-8')
    for book in books:
        log.write(book)
    log.close()


if __name__ == '__main__':
    base = Path(__file__).parent
    log_path = base / 'returns.log'
    error_path = base / 'errors.log'
    for old in (log_path, error_path):
        if old.exists():
            old.unlink()
    for day_file in sorted((base / 'input').glob('day*.txt')):
        process(day_file, log_path, error_path)
    process(base / 'input' / 'missing_day.txt', log_path, error_path)
    print(log_path.read_text(encoding='utf-8'))
    if error_path.exists():
        print('ERROR LOG:')
        print(error_path.read_text(encoding='utf-8'))
