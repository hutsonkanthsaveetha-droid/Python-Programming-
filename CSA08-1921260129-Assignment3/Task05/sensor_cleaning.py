def valid(value):
    return -50 <= value <= 50


def clean_loop(readings):
    result = []
    for celsius in readings:
        if valid(celsius):
            result.append((celsius, celsius * 9 / 5 + 32))
    return result


def clean_comprehension(readings):
    return [(c, c * 9 / 5 + 32) for c in readings if -50 <= c <= 50]


def clean_map_filter(readings):
    return list(map(lambda c: (c, c * 9 / 5 + 32), filter(lambda c: -50 <= c <= 50, readings)))


def alarm_minutes(readings):
    return [minute for minute, c in enumerate(readings, start=1) if valid(c) and not 2 <= c <= 8]


def main():
    readings = [4.0, 2.5, 8.5, 51.0, -52.0, 6.0, 1.5, 7.0, 12.0]
    a = clean_loop(readings)
    b = clean_comprehension(readings)
    c = clean_map_filter(readings)
    print('loop:', a)
    print('comprehension:', b)
    print('map/filter:', c)
    print('all equal:', a == b == c)
    print('alarm minutes (1-based):', alarm_minutes(readings))
    print('dictionary comprehension:', {i: value for i, value in enumerate(readings, start=1) if valid(value)})
    print('set comprehension:', {round(value) for value in readings if valid(value)})
    print('all invalid:', clean_comprehension([100, -100, 51, -51]))
    print('all valid count:', len(clean_comprehension([3, 4, 5, 6])))


if __name__ == '__main__':
    main()
