from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray



class Newton(AbstractQuantity):
    """
    This is the dimension of the gravitational constant G:
    https://en.wikipedia.org/wiki/Gravitational_constant
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=3, mass_exponent=-1, time_exponent=-2)
