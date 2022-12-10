from units.dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray



class VolumetricFlow(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=3, time_exponent=-1)
