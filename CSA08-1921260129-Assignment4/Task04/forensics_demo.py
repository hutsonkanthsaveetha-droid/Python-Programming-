from pathlib import Path


def broken_save_returns(books, log_path):
    log = open(log_path, 'w', encoding='utf-8')
    for book in books:
        log.write(book)
    log.close()


def main():
    base = Path(__file__).parent
    broken_log = base / 'broken_returns.log'
    for day in sorted((base / 'input').glob('day*.txt')):
        books = day.read_text(encoding='utf-8').splitlines()
        broken_save_returns(books, broken_log)
    print('Broken log after three days:')
    print(repr(broken_log.read_text(encoding='utf-8')))

    handle = open(base / 'write_failure.log', 'w', encoding='utf-8')
    try:
        handle.write(123)
    except TypeError as exc:
        print(type(exc).__name__, '| file closed?', handle.closed)
    finally:
        handle.close()


if __name__ == '__main__':
    main()
