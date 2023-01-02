from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Acceleration(AbstractQuantity):
    """
    https://en.wikipedia.org/wiki/Acceleration

    Supported units (From smallest to biggest):

    gravity      g       Acceleration(1.0, "g")     https://en.wikipedia.org/wiki/G-force
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=1, time_exponent=-2)
    _UNITS = {Unit('g', 'gravity', 9.80665): 9.80665}
