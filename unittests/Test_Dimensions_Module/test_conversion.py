import pytest
from math import isclose
from units.dimensions import *
from units.unittests.Test_Dimensions_Module.ConversionArray import ConversionArray



CONVERSION_TABLES = \
    (
        ConversionArray(Length, length_exponent=1),
        ConversionArray(Mass, mass_exponent=1),
        ConversionArray(Time, time_exponent=1),
        ConversionArray(SubstanceAmount, substance_amount_exponent=1),
        ConversionArray(Surface, length_exponent=2),
        ConversionArray(Volume, length_exponent=3),
        ConversionArray(Speed, length_exponent=1, time_exponent=-1),
        ConversionArray(Frequency, time_exponent=-1),
        ConversionArray(Acceleration, length_exponent=1, time_exponent=-2),
        ConversionArray(Pressure, mass_exponent=1, length_exponent=-1, time_exponent=-2)
    )



@pytest.mark.parametrize('conversion_table', CONVERSION_TABLES)
def test_convert(conversion_table: ConversionArray):
    dimension_class = conversion_table.dimension_class
    yield_random = True if conversion_table.size > 200000 else False
    for test_number, source_symbol, target_symbol, expected_number in conversion_table.generate_test_data(yield_random):
        test_quantity = dimension_class(test_number, source_symbol)
        converted_quantity = test_quantity.convert(target_symbol)
        assert isclose(float(converted_quantity), expected_number, rel_tol=1e-4),\
            f"Failed to convert {dimension_class.__name__} quantity {test_quantity} in {target_symbol}."
    return
