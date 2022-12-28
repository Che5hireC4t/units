import pytest
from math import isclose

from unittests.Test_Dimensions_Module.dependencies import ConversionArray
from unittests.Test_Dimensions_Module.conftest import CONVERSION_TABLES_INIT_DATA



@pytest.mark.parametrize('conversion_table_init_data', CONVERSION_TABLES_INIT_DATA.values())
def test_convert(conversion_table_init_data: dict):
    conversion_table = ConversionArray(**conversion_table_init_data)
    dimension_class = conversion_table.dimension_class
    yield_random = True if conversion_table.size > 1000 else False
    for test_number, source_symbol, target_symbol, expected_number in conversion_table.generate_test_data(yield_random):
        test_quantity = dimension_class(test_number, source_symbol)
        converted_quantity = test_quantity.convert(target_symbol)
        assert isclose(float(converted_quantity), expected_number, rel_tol=1e-4),\
            f"Failed to convert {dimension_class.__name__} quantity {test_quantity} in {target_symbol}."
    return
