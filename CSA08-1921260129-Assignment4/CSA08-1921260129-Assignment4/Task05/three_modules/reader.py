import csv

def read_records(path):
    with open(path, encoding='utf-8', newline='') as source:
        return list(csv.DictReader(source))
