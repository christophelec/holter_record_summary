from typing import List, Generator

import begin
import csv

from holter_record_summary.wave import Wave


def get_premature_waves(waves: List[Wave]) -> List[Wave]:
    return [wave for wave in waves if "premature" in wave.tags and wave.type in ['P', 'QRS']]


def get_qrs(waves: List[Wave]) -> List[Wave]:
    return [wave for wave in waves if wave.type == 'QRS']


def extract_waves(rows: csv.reader) -> List[Wave]:
    return [Wave(row[0], row[1], row[2], row[3:]) for row in rows]

@begin.start
def run(input_file='record.csv'):
    """Holster Record Summary"""
    with open(input_file, 'r') as record:
        reader = csv.reader(record)
        waves = extract_waves(reader)
        #print(get_premature_waves(waves))
        print(calculate_mean_heart_rate(waves))
