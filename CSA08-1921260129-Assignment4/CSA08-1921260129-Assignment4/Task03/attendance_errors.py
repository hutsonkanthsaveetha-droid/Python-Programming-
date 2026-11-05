from pathlib import Path
import argparse


class InvalidRecord(Exception):
    pass


class AttendanceFileError(Exception):
    pass


def parse_line(line):
    parts = line.strip().split(',')
    if len(parts) != 3:
        raise InvalidRecord(f'expected 3 fields, found {len(parts)}')
    register_number, date_text, status = (part.strip() for part in parts)
    if not register_number or not date_text:
        raise InvalidRecord('register number and date are required')
    if status not in {'P', 'A'}:
        raise InvalidRecord(f'invalid status {status!r}')
    return register_number, date_text, status


def summarise(path):
    present, absent, errors = 0, 0, []
    try:
        with open(path, 'r', encoding='utf-8') as source:
            for line_number, line in enumerate(source, start=1):
                if not line.strip():
                    continue
                try:
                    record = parse_line(line)
                except InvalidRecord as exc:
                    errors.append((line_number, str(exc)))
                else:
                    if record[2] == 'P':
                        present += 1
                    else:
                        absent += 1
    except FileNotFoundError as exc:
        raise AttendanceFileError(f'file not found: {path}') from exc
    except PermissionError as exc:
        raise AttendanceFileError(f'permission denied: {path}') from exc
    except UnicodeDecodeError as exc:
        raise AttendanceFileError(f'cannot decode file: {path}') from exc
    finally:
        # The with statement closes the file on success and on every exception.
        pass
    return present, absent, errors


def run_with_audit(path, audit_path):
    try:
        result = summarise(path)
    except AttendanceFileError as exc:
        print(exc)
        if exc.__cause__ is not None:
            print(f'Original cause: {type(exc.__cause__).__name__}')
        raise
    else:
        return result
    finally:
        with open(audit_path, 'a', encoding='utf-8') as audit:
            audit.write(f'Finished attempt: {path}\n')


def main():
    base = Path(__file__).parent
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='?', default=str(base / 'input' / 'sample_attendance.csv'))
    args = parser.parse_args()
    try:
        print(run_with_audit(args.path, base / 'processing_audit.log'))
    except AttendanceFileError:
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
