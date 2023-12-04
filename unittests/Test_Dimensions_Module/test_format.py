NUMBERS_FORMAT_PLAIN = \
    (
        {
            "test": 56.789,
            "precision": 5,
            "significant digits": 7,
            "expected": "56.78900",
            "expected e": "5.678900e+01",
            "expected eng": "5.678900e+01"
        },
        {
            "test": 56.789,
            "precision": 1,
            "significant digits": 3,
            "expected": "56.8",
            "expected e": "5.68e+01",
            "expected eng": "5.68e+01"
        },
        {
            "test": 56.789,
            "precision": 0,
            "significant digits": 2,
            "expected": "57",
            "expected e": "5.7e+01",
            "expected eng": "5.7e+01"
        },
        {
            "test": 56.789,
            "precision": -1,
            "significant digits": 1,
            "expected": "60",
            "expected e": "6e+01",
            "expected eng": "6e+01"
        },
        {
            "test": 123456789.123456,
            "precision": 6,
            "significant digits": 15,
            "expected": "123456789.123456",
            "expected e": "1.2345789123456e+08",
            "expected eng": "123.45789123456e+06"
        },
        {
            "test": 123456789.123456,
            "precision": 4,
            "significant digits": 13,
            "expected": "123456789.1235",
            "expected e": "1.23457891235e+08",
            "expected eng": "123.457891235e+06"
        },
        {
            "test": 123456789.123456,
            "precision": -3,
            "significant digits": 6,
            "expected": "123458000",
            "expected e": "1.23458e+08",
            "expected eng": "123.458e+06"
        },
        {
            "test": 0.0000000000000000000789,
            "precision": 22,
            "significant digits": 3,
            "expected": "0.0000000000000000000789",
            "expected e": "7.89e-20",
            "expected eng": "78.9e-21"
        },
        {
            "test": 0.0000000000000000000789,
            "precision": 24,
            "significant digits": 5,
            "expected": "0.000000000000000000078900",
            "expected e": "7.8900e-20",
            "expected eng": "78.900e-21"
        },
        {
            "test": 0.0000000000000000000789,
            "precision": 20,
            "significant digits": 1,
            "expected": "0.00000000000000000008",
            "expected e": "8e-20",
            "expected eng": "80e-21"
        },
        {
            "test": 0.0000000000000000000789,
            "precision": 19,
            "significant digits": 1,
            "expected": "0.0000000000000000001",
            "expected e": "1e-19",
            "expected eng": "100e-21"
        },
        {
            "test": 0.0000000000000000000789,
            "precision": 18,
            "significant digits": 1,
            "expected": "0.000000000000000000",
            "expected e": "0e-18",
            "expected eng": "0e-18"
        },
    )