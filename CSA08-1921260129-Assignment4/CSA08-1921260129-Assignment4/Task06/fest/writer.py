from pathlib import Path
import csv


def write_outputs(registrations, errors, output_dir, valid_lines, duplicate_lines, files_expected):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    with (out / 'clean_master.csv').open('w', encoding='utf-8', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(['register_number', 'name', 'department', 'emails', 'events'])
        for reg, record in sorted(registrations.items()):
            writer.writerow([reg, record['name'], record['department'],
                             ';'.join(sorted(record['emails'])), ';'.join(sorted(record['events']))])

    all_events = sorted({event for record in registrations.values() for event in record['events']})
    for event in all_events:
        with (out / f'event_{event.lower().replace(" ", "_")}.csv').open('w', encoding='utf-8', newline='') as target:
            writer = csv.writer(target)
            writer.writerow(['register_number', 'name', 'department'])
            for reg, record in sorted(registrations.items()):
                if event in record['events']:
                    writer.writerow([reg, record['name'], record['department']])

    with (out / 'summary.txt').open('w', encoding='utf-8') as target:
        target.write(f'Expected department files: {files_expected}\n')
        target.write(f'Valid registration lines: {valid_lines}\n')
        target.write(f'Duplicate lines merged: {duplicate_lines}\n')
        target.write(f'Unique contacts: {len(registrations)}\n')
        target.write(f'Rejected or unavailable records: {len(errors)}\n')
        target.write(f'Events: {", ".join(all_events)}\n')

    with (out / 'error_log.csv').open('w', encoding='utf-8', newline='') as target:
        writer = csv.writer(target)
        writer.writerow(['file_name', 'line_number', 'reason', 'raw_line'])
        writer.writerows(errors)
