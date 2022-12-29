import pytest
from math import isclose

from unittests.Test_Dimensions_Module.dependencies import get_conversion_data_generator
from unittests.Test_Dimensions_Module.conftest import CONVERSION_TABLES_INIT_DATA



@pytest.mark.parametrize('conversion_table_init_data', CONVERSION_TABLES_INIT_DATA.values())
def test_convert(conversion_table_init_data: dict):
    dimension_class, conversion_values_generator = get_conversion_data_generator(**conversion_table_init_data)
    for test_number, source_symbol, target_symbol, expected_number in dimension_class:
        test_quantity = dimension_class(test_number, source_symbol)
        converted_quantity = test_quantity.convert(target_symbol)
        assert isclose(float(converted_quantity), expected_number, rel_tol=1e-4),\
            f"Failed to convert {dimension_class.__name__} quantity {test_quantity} in {target_symbol}."
    return
