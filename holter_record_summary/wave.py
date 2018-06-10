import csv
from typing import List, Tuple


class Wave:
    def __init__(self, _type, onset, offset, tags=None):
        self.type = _type
        self.onset = int(onset)
        self.offset = int(offset)
        self.tags = tags

    def __str__(self):
        return 'Wave of type {} with onset {} and offset {}, tagged : {}'.format(self.type, self.onset, self.offset,
                                                                                 self.tags)


def get_premature_waves(waves: List[Wave], w_type) -> List[Wave]:
    return [wave for wave in waves if "premature" in wave.tags and wave.type == w_type]


def get_qrs(waves: List[Wave]) -> List[Wave]:
    return [wave for wave in waves if wave.type == 'QRS']


def calculate_mean_heart_rate(waves: List[Wave]) -> float:
    qrs_waves = get_qrs(waves)
    if len(qrs_waves) < 2:
        raise RuntimeError('Not enough QRS waves to calculate a heart rate')
    total_time = qrs_waves[-1].onset - qrs_waves[0].onset
    return len(qrs_waves) / (total_time / 60000)


def min_time_heart_rate(waves: List[Wave]) -> Tuple[float, int]:
    return _time_heart_rate(waves, lambda x, y: x < y)


def max_time_heart_rate(waves: List[Wave]) -> Tuple[float, int]:
    return _time_heart_rate(waves, lambda x, y: x > y)


def _time_heart_rate(waves: List[Wave], cmp_func) -> Tuple[float, int]:
    qrs_waves = get_qrs(waves)
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