import pytest
from math import isnan

from unittests.Test_Dimensions_Module.Test_Pickle.dependencies import get_unpickled_pickled_copy
from unittests.Test_Dimensions_Module.dependencies import get_simple_data_generator
from unittests.Test_Dimensions_Module.conftest import CONVERSION_TABLES_INIT_DATA



@pytest.mark.parametrize('conversion_table_init_data', CONVERSION_TABLES_INIT_DATA.values())
def test_properly_pickle_dump_load(conversion_table_init_data, supply_fuzzer):
    dimension_class, data_generator = get_simple_data_generator(**conversion_table_init_data)
    random_float = supply_fuzzer.logarithmic_randfloat()
    for _, symbol in data_generator:
        quantity = dimension_class(random_float, symbol)
        _ = get_unpickled_pickled_copy(quantity)
    return



@pytest.mark.parametrize('conversion_table_init_data', CONVERSION_TABLES_INIT_DATA.values())
def test_unpickled_equal_original(conversion_table_init_data, supply_fuzzer):
    dimension_class, data_generator = get_simple_data_generator(**conversion_table_init_data)
    random_float = supply_fuzzer.logarithmic_randfloat()
    for _, symbol in data_generator:
        quantity = dimension_class(random_float, symbol)
        unpickled_quantity = get_unpickled_pickled_copy(quantity)
        qty_as_fl = float(quantity)
        unpick_qty_as_fl = float(unpickled_quantity)
        assert quantity.__class__ is unpickled_quantity.__class__,\
            f"Original quantity class is {quantity.__class__}, " \
            f"but un-pickled quantity class is {unpickled_quantity.__class__}"
        assert qty_as_fl == unpick_qty_as_fl or (isnan(qty_as_fl) and isnan(unpick_qty_as_fl)),\
            f"Original value = {qty_as_fl} but un-pickled value = {unpick_qty_as_fl}"
        assert quantity.symbol == unpickled_quantity.symbol,\
            f"Original symbol = {quantity.symbol}, but un-pickled symbol = {unpickled_quantity.symbol}"
        assert quantity.unit_full_name == unpickled_quantity.unit_full_name, \
            f"Original unit name = {quantity.unit_full_name}, " \
            f"but un-pickled unit name = {unpickled_quantity.unit_full_name}"
        assert quantity.factor_from_si == unpickled_quantity.factor_from_si, \
            f"Original factor from international system unit = {quantity.factor_from_si}, " \
            f"but un-pickled factor from international system unit = {unpickled_quantity.factor_from_si}"
        assert quantity.is_si == unpickled_quantity.is_si,\
            f"Original quantity is {'' if quantity.is_si else 'not '}expressed in an international unit " \
            f"while un-pickled quantity is{'' if unpickled_quantity.is_si else ' not'}."
    return
