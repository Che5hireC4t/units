import pytest
from dimensions import Mass


TEST_DATA = \
    (
        {
            "number": 56.789,
            "precision": 5,
            "significant digits": 7,
            "expected": "56.78900",
            "expected e": "5.678900e+01",
            "expected eng": "56.78900e+00"
        },
        {
            "number": 56.789,
            "precision": 1,
            "significant digits": 3,
            "expected": "56.8",
            "expected e": "5.68e+01",
            "expected eng": "56.8e+00"
        },
        {
            "number": 56.789,
            "precision": 0,
            "significant digits": 2,
            "expected": "57",
            "expected e": "5.7e+01",
            "expected eng": "57e+00"
        },
        {
            "number": 56.789,
            "precision": -1,
            "significant digits": 1,
            "expected": "60",
            "expected e": "6e+01",
            "expected eng": "60e+00"
        },
        {
            "number": 56.789,
            "precision": -3,
            "significant digits": 1,
            "expected": "0",
            "expected e": "0e+03",
            "expected eng": "0e+03"
        },
        {
            "number": 123456789.123456,
            "precision": 6,
            "significant digits": 15,
            "expected": "123456789.123456",
            "expected e": "1.23456789123456e+08",
            "expected eng": "123.456789123456e+06"
        },
        {
            "number": 123456789.123456,
            "precision": 4,
            "significant digits": 13,
            "expected": "123456789.1235",
            "expected e": "1.234567891235e+08",
            "expected eng": "123.4567891235e+06"
        },
        {
            "number": 123456789.123456,
            "precision": -3,
            "significant digits": 6,
            "expected": "123457000",
            "expected e": "1.23457e+08",
            "expected eng": "123.457e+06"
        },
        {
            "number": 0.0000000000000000000789,
            "precision": 22,
            "significant digits": 3,
            "expected": "0.0000000000000000000789",
            "expected e": "7.89e-20",
            "expected eng": "78.9e-21"
        },
        {
            "number": 0.0000000000000000000789,
            "precision": 24,
            "significant digits": 5,
            "expected": "0.000000000000000000078900",
            "expected e": "7.8900e-20",
            "expected eng": "78.900e-21"
        },
        {
            "number": 0.0000000000000000000789,
            "precision": 20,
            "significant digits": 1,
            "expected": "0.00000000000000000008",
            "expected e": "8e-20",
            "expected eng": "80e-21"
        },
        {
            "number": 0.0000000000000000000789,
            "precision": 19,
            "significant digits": 1,
            "expected": "0.0000000000000000001",
            "expected e": "1e-19",
            "expected eng": "100e-21"
        },
        {
            "number": 0.0000000000000000000789,
            "precision": 18,
            "significant digits": 1,
            "expected": "0.000000000000000000",
            "expected e": "0e-18",
            "expected eng": "0e-18"
        },
        {
            "number": 1.0,
            "precision": 1,
            "significant digits": 2
        },
        {
            "number": 0.8,
            "precision": 1,
            "significant digits": 1
        },
        {
            "number": 0.31,
            "precision": 2,
            "significant digits": 2
        },
        {
            "number": 1.200,
            "precision": 3,
            "significant digits": 4
        },
        {
            "number": 0.0520,
            "precision": 4,
            "significant digits": 3
        },
        {
            "number": 400,
            "precision": -2,
            "significant digits": 1
        },
        {
            "number": 400,
            "precision": -1,
            "significant digits": 2
        },
        {
            "number": 400,
            "precision": 0,
            "significant digits": 3
        },
    )


@pytest.mark.parametrize('test_data', TEST_DATA)
def test_consistency(test_data) -> None:
    number, tested_precision, expected_significant_digits = test_data['number'], test_data['precision'], test_data['significant digits']
    expected_precision = tested_precision
    mass = Mass(number, 'g', tested_precision)
    assert mass.precision == expected_precision
    assert mass.significant_digits == expected_significant_digits
    return

