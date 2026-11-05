from pathlib import Path
from .parser import parse_line, InvalidRegistration
from .writer import write_outputs


def process_departments(input_dir, output_dir, expected_departments):
    input_dir = Path(input_dir)
    registrations = {}
    errors = []
    valid_lines = 0
    duplicate_lines = 0

    for department in expected_departments:
        path = input_dir / f'{department}.csv'
        try:
            with path.open('r', encoding='utf-8', newline='') as source:
                for line_number, line in enumerate(source, 1):
                    if not line.strip():
                        continue
                    if line_number == 1 and line.strip().lower().startswith('register_number,'):
                        continue
                    try:
                        record = parse_line(line)
                    except (InvalidRegistration, ValueError) as exc:
                        errors.append((path.name, line_number, str(exc), line.rstrip('\n')))
                        continue
                    valid_lines += 1
                    reg = record['register_number']
                    if reg in registrations:
                        duplicate_lines += 1
                        registrations[reg]['emails'].update(record['emails'])
                        registrations[reg]['events'].update(record['events'])
                        if not registrations[reg]['name']:
                            registrations[reg]['name'] = record['name']
                    else:
                        registrations[reg] = record
        except FileNotFoundError as exc:
            errors.append((path.name, 0, f'missing department file: {exc}', ''))
        except (PermissionError, UnicodeDecodeError, OSError) as exc:
            errors.append((path.name, 0, f'{type(exc).__name__}: {exc}', ''))

    write_outputs(registrations, errors, output_dir, valid_lines, duplicate_lines, len(expected_departments))
    return registrations, errors, {'valid_lines': valid_lines, 'duplicate_lines': duplicate_lines,
                                   'unique_contacts': len(registrations), 'files_expected': len(expected_departments)}
