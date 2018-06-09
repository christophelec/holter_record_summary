import csv
from typing import List

import begin

from holter_record_summary import Wave
import holter_record_summary as hrs


def file_to_waves(input_file:str) -> List[Wave]:
    with open(input_file, 'r') as record:
        reader = csv.reader(record)
        return hrs.extract_waves(reader)

@begin.subcommand
def prematures(input_file: 'CSV file containing the records'):
    """Returns a list of premature P and QRS Waves"""
    waves = file_to_waves(input_file)
    p_prem_waves = hrs.get_premature_waves(waves, 'P')
    qrs_prem_waves = hrs.get_premature_waves(waves, 'QRS')
    print('Premature P Waves : {}'.format(len(p_prem_waves)))
    print('Premature QRS Complexes : {}'.format(len(qrs_prem_waves)))


@begin.start
def run(input_file='record.csv'):
    """Holster Record Summary"""
    with open(input_file, 'r') as record:
        reader = csv.reader(record)
        waves = hrs.extract_waves(reader)
        #print(get_premature_waves(waves))
        print(hrs.calculate_mean_heart_rate(waves))
