import pytest
from dimensions import Mass


TESTS = \
    (
        (Mass(1, 'g', None), Mass(1, 'g', None), False),
        (Mass(1, 'g', 3), Mass(1, 'g', None), False),
        (Mass(1, 'g', 3), Mass(1, 'g', 1), True),
        (Mass(1, 'g', 3), Mass(1, 'g', 3), False),
        (Mass(1, 'g', 3), Mass(2, 'g', 3), True),
    )


@pytest.mark.parametrize('test_data', TESTS)
def test_ne(test_data) -> None:
    value1, value2, expected_result = test_data
    real_result = value1 != value2
    assert real_result == expected_result
    return