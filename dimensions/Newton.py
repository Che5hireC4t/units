from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray



class Newton(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=3, mass_exponent=-1, time_exponent=-2)
