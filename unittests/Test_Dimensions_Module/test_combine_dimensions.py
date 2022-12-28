import pytest
from dimensions import *


MULTIPLICATION_DATA = \
    {
        (Length, Length): Surface,
        (Length, Surface): Volume,
        (ElectricCurrent, Time): ElectricCharge,
        (Length, Frequency): Speed
    }

DIVISION_DATA = \
    {
        (Mass, Volume): Density,
        (Mass, Time): MassFlow,
        (SubstanceAmount, Time): SubstanceFlow,
        (Volume, Time): VolumetricFlow,
        (SubstanceAmount, Surface): Dobson,
        (Force, Surface): Pressure,
        (Energy, Volume): Pressure,
        (Length, Time): Speed
    }

POWER_DATA = \
    {
        (Time, -1): Frequency,
        (Length, 2): Surface,
        (Length, 3): Volume
    }



@pytest.mark.parametrize\
        (
            'right, left, expected_result_class',
            [(*operands, result) for operands, result in MULTIPLICATION_DATA.items()]
        )
def test_multiply_dimensions(right, left, expected_result_class):
    result_class = right * left
    assert result_class is expected_result_class
    return


@pytest.mark.parametrize\
        (
            'right, left, expected_result_class',
            [(*operands, result) for operands, result in DIVISION_DATA.items()]
        )
def test_divide_dimensions(right, left, expected_result_class):
    result_class = right / left
    assert result_class is expected_result_class
    return


@pytest.mark.parametrize\
        (
            'right, exponent, expected_result_class',
            [(*operands, result) for operands, result in POWER_DATA.items()]
        )
def test_power_dimensions(right, exponent: int, expected_result_class):
    result_class = pow(right, exponent)
    assert result_class is expected_result_class
    return
