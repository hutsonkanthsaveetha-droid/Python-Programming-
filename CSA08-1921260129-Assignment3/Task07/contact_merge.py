import re


def normalise_number(value):
    digits = ''.join(ch for ch in str(value or '') if ch.isdigit())
    if len(digits) == 12 and digits.startswith('91'):
        digits = digits[2:]
    if len(digits) == 11 and digits.startswith('0'):
        digits = digits[1:]
    return digits


def normalise_name(value):
    return ' '.join(re.findall(r'[a-z0-9]+', str(value or '').casefold()))


def normalise_email(value):
    return str(value or '').strip().casefold()


def merge_contacts(sources):
    groups = {}
    number_to_key = {}
    email_to_key = {}
    for source_name, contacts in sources.items():
        for position, contact in enumerate(contacts, start=1):
            raw_numbers = contact.get('phones', [])
            if isinstance(raw_numbers, str): raw_numbers = [raw_numbers]
            numbers = {normalise_number(value) for value in raw_numbers if normalise_number(value)}
            raw_emails = contact.get('emails', [])
            if isinstance(raw_emails, str): raw_emails = [raw_emails]
            emails = {normalise_email(value) for value in raw_emails if normalise_email(value)}
            matched = {number_to_key[number] for number in numbers if number in number_to_key}
            matched.update(email_to_key[email] for email in emails if email in email_to_key)
            if matched:
                key = sorted(matched)[0]
                for old_key in sorted(matched - {key}):
                    old = groups.pop(old_key)
                    groups[key]['names'].update(old['names'])
                    groups[key]['normalised_names'].update(old['normalised_names'])
                    groups[key]['phones'].update(old['phones'])
                    groups[key]['emails'].update(old['emails'])
                    for old_number in old['phones']: number_to_key[old_number] = key
                    for old_email in old['emails']: email_to_key[old_email] = key
            elif numbers:
                key = sorted(numbers)[0]
            elif emails:
                key = 'email:' + sorted(emails)[0]
            else:
                key = f'unmatched:{source_name}:{position}'
            group = groups.setdefault(key, {'names': set(), 'normalised_names': set(), 'phones': set(), 'emails': set()})
            name = str(contact.get('name', '')).strip()
            if name:
                group['names'].add(name)
                group['normalised_names'].add(normalise_name(name))
            group['phones'].update(numbers)
            group['emails'].update(emails)
            for number in numbers: number_to_key[number] = key
            for email in emails: email_to_key[email] = key
    return sorted(groups.values(), key=lambda item: (sorted(item['phones']) or ['~'])[0])


def main():
    phone_a = [
        {'name': 'Dr. Ravi', 'phones': ['+91 98400 12345'], 'emails': ['Ravi@Example.com']},
        {'name': 'Meena', 'phones': ['+91-90000-11111'], 'emails': []},
        {'name': 'Arun', 'phones': ['9840013333'], 'emails': ['arun@example.com']},
    ]
    phone_b = [
        {'name': 'ravi kumar', 'phones': ['9840012345', '044-22223333'], 'emails': ['ravi@example.com']},
        {'name': 'Meena S', 'phones': ['9000011111'], 'emails': ['meena@example.com']},
        {'name': 'Ravi Office', 'phones': [], 'emails': ['office@example.com']},
    ]
    sim = [
        {'name': 'ARUN', 'phones': ['+91 98400 13333'], 'emails': ['ARUN@example.com']},
        {'name': 'No number contact', 'phones': [], 'emails': []},
    ]
    merged = merge_contacts({'phone_a': phone_a, 'phone_b': phone_b, 'sim': sim})
    print('merged contact groups:', len(merged))
    for item in merged:
        print('names=', sorted(item['names']), '| phones=', sorted(item['phones']), '| emails=', sorted(item['emails']))
    print('same name / different phones remain separate:', len(merge_contacts({'a':[{'name':'Ravi','phones':['9840012345'],'emails':[]},{'name':'Ravi','phones':['9840099999'],'emails':[]}]})) == 2)


if __name__ == '__main__': main()
