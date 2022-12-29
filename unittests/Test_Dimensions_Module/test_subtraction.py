import pytest
from math import isclose

from dimensions.exceptions.IncompatibleUnitError import IncompatibleUnitError
from unittests.Test_Dimensions_Module.dependencies import get_conversion_data_generator, get_simple_data_generator
from unittests.Test_Dimensions_Module.conftest import CONVERSION_TABLES_INIT_DATA



@pytest.mark.parametrize('conversion_table_init_data', CONVERSION_TABLES_INIT_DATA.values())
def test_correctly_add_same_dimension(conversion_table_init_data: dict) -> None:
    dimension_class, conversion_values_generator = get_conversion_data_generator(**conversion_table_init_data)
    for test_number_1, symbol_1, symbol_2, test_number_2 in conversion_values_generator:
        expected_number = test_number_1
        quantity_1 = dimension_class(2 * test_number_1, symbol_1)
        quantity_2 = dimension_class(test_number_2, symbol_2)
        final_quantity = quantity_1 - quantity_2
        assert isclose(float(final_quantity), expected_number, rel_tol=1e-4),\
            f"Addition gave an unexpected value: {quantity_1} - {quantity_2} --> {final_quantity}"
        assert set(final_quantity.symbol.split(' ')) == set(symbol_1.split(' ')),\
            f"Addition of 2 quantities with different units should give a quantity with same symbol that first member."\
            f"\nHowever, symbol_1 = {symbol_1} and final symbol = {final_quantity.symbol}"
    return


@pytest.mark.parametrize('conversion_table_init_data1', CONVERSION_TABLES_INIT_DATA.values())
@pytest.mark.parametrize('conversion_table_init_data2', CONVERSION_TABLES_INIT_DATA.values())
def test_properly_raise_if_incompatible(conversion_table_init_data1: dict, conversion_table_init_data2: dict) -> None:
    if conversion_table_init_data1['test_dimension'] == conversion_table_init_data2['test_dimension']:
        return
    dimension_class_1, data_generator_1 = get_simple_data_generator(**conversion_table_init_data1)
    dimension_class_2, data_generator_2 = get_simple_data_generator(**conversion_table_init_data2)
    for test_number_1, symbol_1 in data_generator_1:
        for test_number_2, symbol_2 in data_generator_2:
            test_quantity_1 = dimension_class_1(test_number_1, symbol_1)
            test_quantity_2 = dimension_class_2(test_number_2, symbol_2)
            with pytest.raises(IncompatibleUnitError):
                _ = test_quantity_1 - test_quantity_2
    return
