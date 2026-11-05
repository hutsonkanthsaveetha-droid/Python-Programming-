def percentage(records):
    counts = {}
    for row in records:
        counts.setdefault(row['register_number'], [0, 0])[0 if row['status'] == 'P' else 1] += 1
    return {reg: round(p / (p + a) * 100, 2) for reg, (p, a) in counts.items()}

def absent_three_days(records):
    by_student = {}
    for row in records:
        by_student.setdefault(row['register_number'], []).append((row['date'], row['status']))
    found = []
    for reg, values in by_student.items():
        statuses = [status for _, status in sorted(values)]
        if any(statuses[i:i+3] == ['A', 'A', 'A'] for i in range(max(0, len(statuses)-2))):
            found.append(reg)
    return sorted(found)
