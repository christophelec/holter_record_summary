import begin
import csv

from wave import Wave


def extract_waves(rows: csv.reader):
    return [Wave(row[0], row[1], row[2], row[3:]) for row in rows]

@begin.start
def run(input_file='record.csv'):
    """Holster Record Summary"""
    with open(input_file, 'r') as record:
        reader = csv.reader(record)
        waves = extract_waves(reader)
        for wave in waves:
            print(wave)
