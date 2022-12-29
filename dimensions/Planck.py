from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray



class Planck(AbstractQuantity):
    """
    This is the dimension of the Planck constant:
    https://en.wikipedia.org/wiki/Planck_constant
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=2, mass_exponent=1, time_exponent=-1)
