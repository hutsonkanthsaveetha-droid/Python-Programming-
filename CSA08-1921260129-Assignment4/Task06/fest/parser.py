import csv


class InvalidRegistration(ValueError):
    pass


def normalize_reg(value):
    result = value.strip().upper()
    if not result or not result.isalnum():
        raise InvalidRegistration('invalid register number')
    return result


def valid_email(value):
    email = value.strip()
    if email.count('@') != 1 or ' ' in email:
        return False
    local, domain = email.split('@')
    return bool(local and '.' in domain and not domain.startswith('.') and not domain.endswith('.'))


def parse_line(line):
    fields = next(csv.reader([line]))
    if len(fields) != 5:
        raise InvalidRegistration(f'expected 5 fields, found {len(fields)}')
    reg, name, department, email, events_text = (field.strip() for field in fields)
    reg = normalize_reg(reg)
    if not name or not department:
        raise InvalidRegistration('name and department are required')
    if not valid_email(email):
        raise InvalidRegistration(f'invalid e-mail {email!r}')
    events = {event.strip().title() for event in events_text.split(';') if event.strip()}
    if not events:
        raise InvalidRegistration('at least one event is required')
    return {'register_number': reg, 'name': name, 'department': department,
            'emails': {email.lower()}, 'events': events}
