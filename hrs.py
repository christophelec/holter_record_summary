import csv
from typing import List

import begin

from holter_record_summary import Wave
import holter_record_summary as hrs
from datetime import datetime


def file_to_waves(input_file: str) -> List[Wave]:
    with open(input_file, 'r') as record:
        reader = csv.reader(record)
        return hrs.extract_waves(reader)


def stamp_to_date(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).isoformat()


@begin.subcommand()
def prematures():
    """Returns a list of premature P and QRS Waves"""
    # last_return is the return of function run() below
    waves = begin.context.last_return
    p_prem_waves = hrs.get_premature_waves(waves, 'P')
    qrs_prem_waves = hrs.get_premature_waves(waves, 'QRS')
    print('Premature P Waves : {}'.format(len(p_prem_waves)))
    print('Premature QRS Complexes : {}'.format(len(qrs_prem_waves)))


@begin.subcommand()
def mean_heart_rate():
    """Returns the mean heart rate of the given record"""
    # last_return is the return of function run() below
    waves = begin.context.last_return
    mean_hr = hrs.calculate_mean_heart_rate(waves)
    print('Mean heart rate : {}'.format(mean_hr))


@begin.subcommand()
def min_max_hr(start_timestamp: 'Start timestamp of the record' = '0'):
    """Returns the minimal and maximal heart rate,
    along with the time it appeared"""
    # last_return is the return of function run() below
    waves = begin.context.last_return
    min_hr, time_min = hrs.min_time_heart_rate(waves)
    max_hr, time_max = hrs.max_time_heart_rate(waves)
    _start_timestamp = int(start_timestamp)
    if _start_timestamp:
        print('Min heart rate : {} Date : {}'.format(
            min_hr, stamp_to_date(_start_timestamp + time_min)))
        print('Max heart rate : {} Date : {}'.format(
            max_hr, stamp_to_date(_start_timestamp + time_max)))
    else:
        print('Min heart rate : {} Time : {}'.format(min_hr, time_min))
        print('Max heart rate : {} Time : {}'.format(max_hr, time_max))


@begin.start
def run(input_file: 'ĆSV file containing the records'):
    return file_to_waves(input_file)
