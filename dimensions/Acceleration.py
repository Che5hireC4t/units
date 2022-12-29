from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Acceleration(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=1, time_exponent=-2)
    _UNITS = {Unit('g', 'gravity', 9.80665): 9.80665}
