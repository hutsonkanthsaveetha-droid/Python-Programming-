import string
from collections import Counter
from pathlib import Path
import csv

STOP_WORDS = {'not', 'high', 'the', 'a', 'is', 'and', 'to', 'of', 'in', 'for'}
TRANSLATION = str.maketrans({char: ' ' for char in string.punctuation})


def words_from(text):
    return text.lower().translate(TRANSLATION).split()


def frequencies_get(texts, stop):
    counts = {}
    for text in texts:
        for word in words_from(text):
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts


def frequencies_setdefault(texts, stop):
    counts = {}
    for text in texts:
        for word in words_from(text):
            if word not in stop:
                counts.setdefault(word, 0)
                counts[word] += 1
    return counts


def group_by(records, key_name):
    grouped = {}
    for record in records:
        grouped.setdefault(record[key_name], []).append(record['complaint'])
    return grouped


def top(counts, k):
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]


def list_count_method(texts, stop):
    all_words = [word for text in texts for word in words_from(text) if word not in stop]
    return {word: all_words.count(word) for word in set(all_words)}


def main():
    calls = ['seeds not received seeds delayed', 'fertiliser price high', 'seeds price high subsidy not received']
    print('required example:', top(frequencies_get(calls, {'not', 'high'}), 3))
    records = [
        {'district': 'Coimbatore', 'crop': 'paddy', 'complaint': 'Seeds not received.'},
        {'district': 'Erode', 'crop': 'banana', 'complaint': 'Fertiliser price high!'},
        {'district': 'Coimbatore', 'crop': 'paddy', 'complaint': 'Irrigation water delayed.'},
        {'district': 'Salem', 'crop': 'millet', 'complaint': 'Subsidy not received'},
    ]
    district_groups = group_by(records, 'district')
    print('district groups:', district_groups)
    print('complaints per district:', {district: len(items) for district, items in district_groups.items()})
    print('crop groups:', group_by(records, 'crop'))
    print('empty text:', frequencies_get(['', '!!!'], STOP_WORDS))
    print('case/punctuation:', frequencies_get(['SEEDS, seeds! Seeds?'], STOP_WORDS))
    print('get equals setdefault:', frequencies_get(calls, {'not', 'high'}) == frequencies_setdefault(calls, {'not', 'high'}))

    path = Path(__file__).parent / 'inputs' / 'sample_complaints.csv'
    path.parent.mkdir(exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['district', 'crop', 'complaint'])
        writer.writeheader()
        writer.writerows(records)


if __name__ == '__main__':
    main()
