from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class ElectricCurrent(AbstractQuantity):
    """
    https://en.wikipedia.org/wiki/Electric_current
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(electric_current_exponent=1)
    _UNITS = {Unit('A', 'ampere', 1.0): 1.0}  # https://en.wikipedia.org/wiki/Ampere
