def reports(ai_elective, iot_elective, all_students):
    both = ai_elective & iot_elective
    exactly_one = ai_elective ^ iot_elective
    neither = all_students - (ai_elective | iot_elective)
    return both, exactly_one, neither


def reports_methods(ai_elective, iot_elective, all_students):
    both = ai_elective.intersection(iot_elective)
    exactly_one = ai_elective.symmetric_difference(iot_elective)
    neither = all_students.difference(ai_elective.union(iot_elective))
    return both, exactly_one, neither


def main():
    ai_elective = {'192311001', '192311004', '192311007', '192311009', '192311004'}
    iot_elective = {'192311002', '192311004', '192311009', '192311010'}
    all_students = {f'1923110{i:02d}' for i in range(1, 11)}
    both, exactly_one, neither = reports(ai_elective, iot_elective, all_students)
    print('clash      :', sorted(both))
    print('exactly one:', sorted(exactly_one))
    print('neither    :', sorted(neither))
    print('methods agree:', (both, exactly_one, neither) == reports_methods(ai_elective, iot_elective, all_students))
    print('empty electives:', reports(set(), set(), all_students))
    print('identical electives:', reports(ai_elective, set(ai_elective), all_students))
    print('duplicates removed:', len(ai_elective), 'unique from 5 registrations')


if __name__ == '__main__':
    main()
