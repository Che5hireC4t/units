from .AbstractQuantity import AbstractQuantity, DimensionalArray, Unit



class Volume(AbstractQuantity):
    """
    https://en.wikipedia.org/wiki/Volume
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=3)
    _UNITS = \
        {
            Unit('l', 'liter', 0.001): 0.001,
            Unit('gal', 'gallon(US)', 0.003785411784): 0.003785411784  # https://en.wikipedia.org/wiki/Gallon
        }
