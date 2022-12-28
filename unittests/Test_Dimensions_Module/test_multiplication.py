import pytest
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
