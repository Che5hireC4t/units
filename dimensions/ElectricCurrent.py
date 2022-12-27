from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class ElectricCurrent(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(electric_current_exponent=1)
    _UNITS = {Unit('A', 'ampere', 1.0): 1}
