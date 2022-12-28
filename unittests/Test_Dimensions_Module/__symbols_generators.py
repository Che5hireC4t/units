from __syntax.Prefix import Prefix
from dimensions import *
PREFIX_INSTANCES = \
    [
        Prefix(full_name, symbol, ten_exponent)
        for full_name, symbol, ten_exponent in getattr(Prefix, f"_{Prefix.__name__}__PREFIXES")
    ]
from dimensions._MetaQuantity import _MetaQuantity




def generate_symbols() -> tuple:
    for unit_symbol, dimension_class in __generate_native_units():
        yield unit_symbol, dimension_class
    for unit_symbol in __generate_double_symbol(Mass, 1, Length, -3):
        yield unit_symbol, Density
    for unit_symbol in __generate_double_symbol(SubstanceAmount, 1, Length, -2):
        yield unit_symbol, Dobson
    for unit_symbol in __generate_double_symbol(Length, 1, Time, -1):
        yield unit_symbol, Speed
    for unit_symbol in __generate_double_symbol(Mass, 1, Time, -1):
        yield unit_symbol, MassFlow
    for unit_symbol in __generate_double_symbol(Mass, 1, SubstanceAmount, -1):
        yield unit_symbol, MolarMass
    for unit_symbol in __generate_double_symbol(Force, 1, Length, -2):
        yield unit_symbol, Pressure
    for unit_symbol in __generate_double_symbol(SubstanceAmount, 1, Time, -1):
        yield unit_symbol, SubstanceFlow
    for unit_symbol in __generate_double_symbol(Length, 3, Time, -1):
        yield unit_symbol, VolumetricFlow




def __generate_native_units() -> tuple:
    all_dimensions = getattr(_MetaQuantity, f"{_MetaQuantity.__name__}__instances")
    try:
        all_dimensions.pop((0, 0, 0, 0, 0, 0, 0))
        all_dimensions.pop((127, 127, 127, 127, 127, 127, 127))
    except KeyError:
        pass
    for dimension_class in all_dimensions.values():
        for unit in dimension_class.UNITS:
            for prefix in PREFIX_INSTANCES:
                yield f"{prefix.symbol}{unit.symbol}", dimension_class,



def __generate_double_symbol(dimension_class_1, exponent1: int, dimension_class_2, exponent2: int):
    if exponent1 == 1:
        exponent1_str = ''
    else:
        exponent1_str = str(exponent1)
    if exponent2 == 1:
        exponent2_str = ''
    else:
        exponent2_str = str(exponent2)
    for unit1 in dimension_class_1.UNITS:
        for unit2 in dimension_class_2.UNITS:
            for prefix1 in PREFIX_INSTANCES:
                for prefix2 in PREFIX_INSTANCES:
                    yield f"{prefix1.symbol}{unit1.symbol}{exponent1_str} {prefix2.symbol}{unit2.symbol}{exponent2_str}"
