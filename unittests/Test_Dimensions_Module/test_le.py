import pytest
from dimensions import Mass


TESTS = \
    (
        (Mass(1, 'g', None), Mass(1, 'g', None), True),
        (Mass(1, 'g', 3), Mass(1, 'g', None), True),
        (Mass(1, 'g', 3), Mass(1, 'g', 1), False),
        (Mass(1, 'g', 3), Mass(1, 'g', 3), True),
        (Mass(1, 'g', 3), Mass(2, 'g', 3), True),
        (Mass(56, 'g', 0), Mass(56.789, 'g', 3), False)
    )


@pytest.mark.parametrize('test_data', TESTS)
def test_le(test_data) -> None:
    value1, value2, expected_result = test_data
    real_result = value1 <= value2
    assert real_result == expected_result
    return
