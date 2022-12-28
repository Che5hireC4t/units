import pytest
from math import isnan

from unittests.Test_Dimensions_Module.dependencies import ConversionArray, get_simple_data_generator
from unittests.Test_Dimensions_Module.conftest import CONVERSION_TABLES_INIT_DATA


@pytest.mark.parametrize('conversion_table_init_data', CONVERSION_TABLES_INIT_DATA.values())
def test_symbols(conversion_table_init_data):
    dimension_class, data_generator = get_simple_data_generator(**conversion_table_init_data)
    for _, symbol in data_generator:
        quantity = dimension_class(1.0, symbol)
        assert isinstance(quantity, dimension_class)
    return



@pytest.mark.parametrize('conversion_table_init_data', CONVERSION_TABLES_INIT_DATA.values())
def test_instantiate_by_int(conversion_table_init_data, supply_fuzzer):
    dimension_class, data_generator = get_simple_data_generator(**conversion_table_init_data)
    random_integer = supply_fuzzer.logarithmic_randint()
    for _, symbol in data_generator:
        quantity = dimension_class(random_integer, symbol)
        assert isinstance(quantity, dimension_class)
        assert float(quantity) == float(random_integer)
    return



@pytest.mark.parametrize('conversion_table_init_data', CONVERSION_TABLES_INIT_DATA.values())
def test_instantiate_by_float(conversion_table_init_data, supply_fuzzer):
    dimension_class, data_generator = get_simple_data_generator(**conversion_table_init_data)
    random_float = supply_fuzzer.logarithmic_randfloat()
    for _, symbol in data_generator:
        quantity = dimension_class(random_float, symbol)
        assert isinstance(quantity, dimension_class)
        assert float(quantity) == random_float or (isnan(float(quantity)) and isnan(random_float))
    return
