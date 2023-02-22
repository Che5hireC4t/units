from .AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Power(AbstractQuantity):
    """
    https://en.wikipedia.org/wiki/Power_(physics)
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1, length_exponent=2, time_exponent=-3)
    _UNITS = {Unit('W', 'watt', 1.0): 1}  # https://en.wikipedia.org/wiki/Watt
