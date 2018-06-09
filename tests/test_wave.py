import pytest

import holter_record_summary.wave
from holter_record_summary.wave import Wave


class TestWave:
    @pytest.mark.parametrize('input_rows, expected', [([], []),
                                                      ([['P', '32', '33', 'test', 'premature'],
                                                        ['QRS', '37', '38'], ], [
                                                           'Wave of type P with onset 32 and offset 33, tagged : [\'test\', \'premature\']',
                                                           'Wave of type QRS with onset 37 and offset 38, tagged : []'])],
                             ids=['empty', 'simple'])
    def test_wave_creation(self, input_rows, expected):
        waves = holter_record_summary.wave.extract_waves(input_rows)
        assert [str(w) for w in waves] == expected

    def test_wave_creation_fail(self):
        with pytest.raises(RuntimeError):
            holter_record_summary.wave.extract_waves([['P']])

    @pytest.mark.parametrize('input_waves, wave_type, expected', [([], 'P', 0),
                                                       ([Wave('P', '32', '33', ['premature'])], 'P', 1),
                                                       ([Wave('QRS', '32', '33', ['premature'])], 'QRS', 1),
                                                       ([Wave('W', '32', '33', ['premature'])], 'P', 0),
                                                       ([Wave('P', '32', '33', ['non_premature'])], 'P', 0),
                                                       ([Wave('P', '32', '33', ['non_premature']),
                                                         Wave('P', '32', '33', ['premature']),
                                                         Wave('P', '35', '33', ['premature']),
                                                         Wave('QRS', '32', '33', ['premature'])], 'P', 2)],
                             ids=['empty', 'single_p', 'single_qrs', 'single_w', 'invalid_p', 'multi'])
    def test_get_premature_waves(self, input_waves, wave_type, expected):
        waves = holter_record_summary.wave.get_premature_waves(input_waves, wave_type)
        assert len(waves) == expected

    def test_mean_heart_rate(self):
        qrs_waves = [Wave('QRS', '0', '59000'),
                     Wave('QRS', '60000', '60001')]
        expected = 2.0
        assert holter_record_summary.wave.calculate_mean_heart_rate(qrs_waves) == expected

    def test_mean_heart_rate_fails(self):
        qrs_waves = [Wave('QRS', '0', '59000')]
        with pytest.raises(RuntimeError):
            holter_record_summary.wave.calculate_mean_heart_rate(qrs_waves)

    def test_min_heart_rate(self):
        qrs_waves = [Wave('QRS', '0', '59000'),
                     Wave('QRS', '60000', '60001'),
                     Wave('QRS', '60001', '60002')]
        assert holter_record_summary.wave.min_time_heart_rate(qrs_waves) == (2.0, 60000)

    def test_max_heart_rate(self):
        qrs_waves = [Wave('QRS', '0', '59000'),
                     Wave('QRS', '60000', '60001'),
                     Wave('QRS', '60001', '60002')]
        assert holter_record_summary.wave.max_time_heart_rate(qrs_waves) == (120000.0, 60001)

    def test_fail_min_heart_rate(self):
        qrs_waves = []
        with pytest.raises(RuntimeError):
            holter_record_summary.wave.max_time_heart_rate(qrs_waves)
