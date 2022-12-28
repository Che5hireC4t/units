import pytest
from math import isnan

from unittests.Test_Dimensions_Module.dependencies import ConversionArray
from unittests.Test_Dimensions_Module.conftest import CONVERSION_TABLES_INIT_DATA


@pytest.mark.parametrize('conversion_table_init_data', CONVERSION_TABLES_INIT_DATA)
def test_symbols(conversion_table_init_data):
    conversion_table = ConversionArray(**conversion_table_init_data)
    dimension_class = conversion_table.dimension_class
    yield_random = True if conversion_table.size > 1000 else False
    for _, symbol, _, _ in conversion_table.generate_test_data(yield_random):
        quantity = dimension_class(1.0, symbol)
        assert isinstance(quantity, dimension_class)
    return



@pytest.mark.parametrize('conversion_table_init_data', CONVERSION_TABLES_INIT_DATA)
def test_instantiate_by_int(conversion_table_init_data, supply_fuzzer):
    conversion_table = ConversionArray(**conversion_table_init_data)
    dimension_class = conversion_table.dimension_class
    yield_random = True if conversion_table.size > 1000 else False
    random_integer = supply_fuzzer.logarithmic_randint()
    for _, symbol, _, _ in conversion_table.generate_test_data(yield_random):
        quantity = dimension_class(random_integer, symbol)
        assert isinstance(quantity, dimension_class)
        assert float(quantity) == float(random_integer)
    return



@pytest.mark.parametrize('conversion_table_init_data', CONVERSION_TABLES_INIT_DATA)
def test_instantiate_by_float(conversion_table_init_data, supply_fuzzer):
    conversion_table = ConversionArray(**conversion_table_init_data)
    dimension_class = conversion_table.dimension_class
    yield_random = True if conversion_table.size > 1000 else False
    random_float = supply_fuzzer.logarithmic_randfloat()
    for _, symbol, _, _ in conversion_table.generate_test_data(yield_random):
        quantity = dimension_class(random_float, symbol)
        assert isinstance(quantity, dimension_class)
        assert float(quantity) == random_float or (isnan(float(quantity)) and isnan(random_float))
    return
