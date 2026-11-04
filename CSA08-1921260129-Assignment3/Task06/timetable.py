from datetime import time

TIMETABLE = {
    '12601': {'name': 'Chennai Mail', 'stops': [('Chennai', '06:00', '06:15'), ('Katpadi', '08:10', '08:12'), ('Jolarpettai', '09:35', '09:40'), ('Bengaluru', '12:00', '12:10')], 'days': {'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'}},
    '12602': {'name': 'Bengaluru Express', 'stops': [('Chennai', '07:00', '07:10'), ('Arakkonam', '08:00', '08:02'), ('Katpadi', '09:10', '09:12'), ('Bengaluru', '11:30', '11:40')], 'days': {'Mon', 'Wed', 'Fri', 'Sun'}},
    '12603': {'name': 'Kaveri Express', 'stops': [('Chennai', '05:30', '05:45'), ('Villupuram', '07:25', '07:27'), ('Trichy', '10:10', '10:15'), ('Madurai', '12:30', '12:35')], 'days': {'Tue', 'Thu', 'Sat'}},
    '12604': {'name': 'Coastal Link', 'stops': [('Chennai', '09:00', '09:05'), ('Tambaram', '09:35', '09:37'), ('Chengalpattu', '10:15', '10:17'), ('Villupuram', '12:00', '12:05')], 'days': {'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'}},
    '12605': {'name': 'Hill City Express', 'stops': [('Chennai', '20:00', '20:15'), ('Katpadi', '22:20', '22:22'), ('Salem', '02:30', '02:35'), ('Coimbatore', '05:30', '05:40')], 'days': {'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'}},
}


def find_trains(timetable, station, day):
    matches = []
    for number, train in timetable.items():
        if day in train['days']:
            for stop, arrival, departure in train['stops']:
                if stop.casefold() == station.casefold():
                    matches.append((number, train['name'], departure))
                    break
    return sorted(matches, key=lambda item: item[2])


def build_station_index(timetable):
    index = {}
    for number, train in timetable.items():
        for station, arrival, departure in train['stops']:
            index.setdefault(station.casefold(), []).append((number, train['name'], departure, train['days']))
    return index


def query_index(index, station, day):
    matches = [(number, name, departure) for number, name, departure, days in index.get(station.casefold(), []) if day in days]
    return sorted(matches, key=lambda item: item[2])


def main():
    index = build_station_index(TIMETABLE)
    print('Tuesday arrivals/departures at Katpadi:')
    for number, name, departure in find_trains(TIMETABLE, 'Katpadi', 'Tue'):
        print(f'{number} {name:20} depart={departure}')
    print('index result same:', find_trains(TIMETABLE, 'Katpadi', 'Tue') == query_index(index, 'Katpadi', 'Tue'))
    print('unknown station:', find_trains(TIMETABLE, 'Unknown', 'Tue'))
    print('train not running that day at Trichy on Monday:', find_trains(TIMETABLE, 'Trichy', 'Mon'))
    print('third station departure for 12601:', TIMETABLE['12601']['stops'][2][2])
    print('full timetable:')
    for number, train in TIMETABLE.items():
        print(number, train['name'], '|', ', '.join(f'{s} {a}-{d}' for s, a, d in train['stops']), '|', ','.join(sorted(train['days'])))


if __name__ == '__main__':
    main()
