from typing import List, Generator, Tuple

import begin
import csv

from holter_record_summary.wave import Wave


def get_premature_waves(waves: List[Wave]) -> List[Wave]:
    return [wave for wave in waves if "premature" in wave.tags and wave.type in ['P', 'QRS']]


def get_qrs(waves: List[Wave]) -> List[Wave]:
    return [wave for wave in waves if wave.type == 'QRS']


def calculate_mean_heart_rate(qrs_waves: List[Wave]) -> float:
    if len(qrs_waves) < 2:
        raise RuntimeError('Not enough QRS waves to calculate a heart rate')
    total_time = qrs_waves[-1].onset - qrs_waves[0].onset
    return len(qrs_waves) / (total_time / 60000)


def min_time_heart_rate(qrs_waves: List[Wave]) -> Tuple[float, int]:
    return _time_heart_rate(qrs_waves, lambda x, y: x < y)


def max_time_heart_rate(qrs_waves: List[Wave]) -> Tuple[float, int]:
    return _time_heart_rate(qrs_waves, lambda x, y: x > y)


def _time_heart_rate(qrs_waves: List[Wave], cmp_func) -> Tuple[float, int]:
    if len(qrs_waves) < 2:
        raise RuntimeError('Not enough QRS waves to calculate a heart rate')
    kept_hr = None
    onset_time = None
    for i in range(1, len(qrs_waves)):
        hr = calculate_mean_heart_rate(qrs_waves[i-1:i+1])
        if kept_hr is None or cmp_func(hr, kept_hr):
            kept_hr = hr
            onset_time = qrs_waves[i].onset
    return kept_hr, onset_time


def extract_waves(rows: csv.reader) -> List[Wave]:
    try:
        return [Wave(row[0], row[1], row[2], row[3:]) for row in rows]
    except IndexError as e:
        raise RuntimeError('Poorly formatted row') from e


@begin.start
def run(input_file='record.csv'):
    """Holster Record Summary"""
    with open(input_file, 'r') as record:
        reader = csv.reader(record)
        waves = extract_waves(reader)
        #print(get_premature_waves(waves))
        print(calculate_mean_heart_rate(waves))
