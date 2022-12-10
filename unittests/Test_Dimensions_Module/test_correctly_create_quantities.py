import pytest
from math import isnan
from units.unittests.Fuzzer import Fuzzer
from units.unittests.Test_Dimensions_Module.__symbols_generators import generate_symbols


@pytest.mark.parametrize\
        (
            'symbol, dimension_class',
            (symbol_class_tuple for symbol_class_tuple in generate_symbols())
        )
def test_symbols(symbol: str, dimension_class):
    quantity = dimension_class(1.0, symbol)
    assert isinstance(quantity, dimension_class)
    return


fuzzer = Fuzzer()
@pytest.mark.parametrize\
        (
            'symbol, dimension_class, random_integer',
            ([*symbol_class_tuple, fuzzer.logarithmic_randint()] for symbol_class_tuple in generate_symbols())
        )
def test_instantiate_by_int(symbol: str, dimension_class, random_integer: int):
    quantity = dimension_class(random_integer, symbol)
    assert isinstance(quantity, dimension_class)
    assert float(quantity) == float(random_integer)
    return


@pytest.mark.parametrize\
        (
            'symbol, dimension_class, random_float',
            ([*symbol_class_tuple, fuzzer.logarithmic_randfloat()] for symbol_class_tuple in generate_symbols())
        )
def test_instantiate_by_float(symbol: str, dimension_class, random_float: float):
    quantity = dimension_class(random_float, symbol)
    assert isinstance(quantity, dimension_class)
    assert float(quantity) == random_float or (isnan(float(quantity)) and isnan(random_float))
    return
