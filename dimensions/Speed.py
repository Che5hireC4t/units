from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray



class Speed(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=1, time_exponent=-1)
