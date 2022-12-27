from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray



class _NullDimension(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray()

    def __new__(cls, value: int | float | str, unit=None):
        return float(value)
