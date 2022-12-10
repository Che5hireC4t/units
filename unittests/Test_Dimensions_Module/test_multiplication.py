import pytest
from units.dimensions import *


MULTIPLICATION_DATA = \
    {
        (Length, Length): Surface,
        (Length, Surface): Volume,
        (ElectricCurrent, Time): ElectricCharge,
        (Length, Frequency): Speed
    }


def test_double_multiplication(multiplier_1: tuple, multiplier_2: tuple, expected_type):
    number_1, symbol_1, dim_class_1 = multiplier_1
    number_2, symbol_2, dim_class_2 = multiplier_2
    quantity_1 = dim_class_1(number_1, symbol_1)
    quantity_2 = dim_class_2(number_2, symbol_2)
    final_result = quantity_1 * quantity_2
