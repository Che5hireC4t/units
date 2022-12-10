from units.dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray



class Planck(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=2, mass_exponent=1, time_exponent=-1)
