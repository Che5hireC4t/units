from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit



class Dobson(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(substance_amount_exponent=1, length_exponent=-2)
    _UNITS = {Unit('DU', 'dobson', 0.00044615): 0.00044615}
