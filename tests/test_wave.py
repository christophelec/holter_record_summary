import pytest

import hrs
from holter_record_summary.wave import Wave


class TestWave:
    @pytest.mark.parametrize('input_rows, expected', [([], []),
                                                      ([['P', '32', '33', 'test', 'premature'],
                                                        ['QRS', '37', '38'], ], [
                                                           'Wave of type P with onset 32 and offset 33, tagged : [\'test\', \'premature\']',
                                                           'Wave of type QRS with onset 37 and offset 38, tagged : []'])],
                             ids=['empty', 'simple'])
    def test_wave_creation(self, input_rows, expected):
        waves = hrs.extract_waves(input_rows)
        assert [str(w) for w in waves] == expected

    @pytest.mark.parametrize('input_waves, expected', [([], 0),
                                                       ([Wave('P', '32', '33', ['premature'])], 1),
                                                       ([Wave('QRS', '32', '33', ['premature'])], 1),
                                                       ([Wave('W', '32', '33', ['premature'])], 0),
                                                       ([Wave('P', '32', '33', ['non_premature'])], 0),
                                                       ([Wave('P', '32', '33', ['non_premature']),
                                                         Wave('P', '32', '33', ['premature']),
                                                         Wave('QRS', '32', '33', ['premature'])], 2)],
                             ids=['empty', 'single_p', 'single_qrs', 'single_w', 'invalid_p', 'multi'])
    def test_get_premature_waves(self, input_waves, expected):
        waves = hrs.get_premature_waves(input_waves)
        assert len(waves) == expected