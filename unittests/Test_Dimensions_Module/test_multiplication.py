import pytest
from math import isnan

from unittests.Test_Dimensions_Module.dependencies import ConversionArray
from unittests.Test_Dimensions_Module.conftest import MULTIPLICATION_DATA, CONVERSION_TABLES_INIT_DATA



@pytest.mark.parametrize('dimension_name1, dimension_name2, expected_type', MULTIPLICATION_DATA)
def test_yield_correct_dimension(dimension_name1: str, dimension_name2: str, expected_type):
    conversion_table1 = ConversionArray(**CONVERSION_TABLES_INIT_DATA[dimension_name1])
    conversion_table2 = ConversionArray(**CONVERSION_TABLES_INIT_DATA[dimension_name2])
    yield_random1 = True if conversion_table1.size > 1000 else False
    yield_random2 = True if conversion_table2.size > 1000 else False
    dimension_class_1 = conversion_table1.dimension_class
    dimension_class_2 = conversion_table2.dimension_class
    for test_number1, symbol1 in conversion_table1.generate_test_values(yield_random1):
        for test_number2, symbol2 in conversion_table2.generate_test_values(yield_random2):
            quantity1 = dimension_class_1(test_number1, symbol1)
            quantity2 = dimension_class_2(test_number2, symbol2)
            multiplied_quantity = quantity1 * quantity2
            assert isinstance(multiplied_quantity, expected_type)
    return



@pytest.mark.parametrize('conversion_table_init_data', CONVERSION_TABLES_INIT_DATA.values())
def test_multiply_by_adimensional(conversion_table_init_data, supply_fuzzer):
    conversion_table = ConversionArray(**conversion_table_init_data)
    dimension_class = conversion_table.dimension_class
    yield_random = True if conversion_table.size > 1000 else False
    for test_number, symbol in conversion_table.generate_test_values(yield_random):
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
