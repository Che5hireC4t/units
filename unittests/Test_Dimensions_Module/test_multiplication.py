import pytest
from math import isnan

from unittests.Test_Dimensions_Module.dependencies import get_simple_data_generator
from unittests.Test_Dimensions_Module.conftest import MULTIPLICATION_DATA, CONVERSION_TABLES_INIT_DATA



@pytest.mark.parametrize('dimension_name1, dimension_name2, expected_type', MULTIPLICATION_DATA)
def test_yield_correct_dimension(dimension_name1: str, dimension_name2: str, expected_type):
    dimension_class_1, data_generator1 = get_simple_data_generator(**CONVERSION_TABLES_INIT_DATA[dimension_name1])
    dimension_class_2, data_generator2 = get_simple_data_generator(**CONVERSION_TABLES_INIT_DATA[dimension_name2])
    for test_number1, symbol1 in data_generator1:
        for test_number2, symbol2 in data_generator2:
            quantity1 = dimension_class_1(test_number1, symbol1)
            quantity2 = dimension_class_2(test_number2, symbol2)
            multiplied_quantity = quantity1 * quantity2
            assert isinstance(multiplied_quantity, expected_type)
    return



@pytest.mark.parametrize('conversion_table_init_data', CONVERSION_TABLES_INIT_DATA.values())
def test_multiply_by_adimensional(conversion_table_init_data, supply_fuzzer):
    dimension_class, data_generator = get_simple_data_generator(**conversion_table_init_data)
    for test_number, symbol in data_generator:
        test_quantity = dimension_class(test_number, symbol)
        if bool(supply_fuzzer.randint(0, 1)):
            random_number = supply_fuzzer.logarithmic_randint()
        else:
            random_number = supply_fuzzer.logarithmic_randfloat()
        expected_number = test_number * random_number
        final_quantity = test_quantity * random_number
        assert float(final_quantity) == expected_number or (isnan(float(final_quantity)) and isnan(expected_number)),\
            f"Multiplication by adimensional number gave an unexpected result.\n" \
            f"{repr(test_quantity)} x {random_number} --> {repr(test_quantity)}"
        assert isinstance(final_quantity, dimension_class),\
            f"Multiplication by adimensional number has changed the dimension:\n" \
            f"{type(test_quantity)} x {random_number} --> {type(test_quantity)}"
    return
