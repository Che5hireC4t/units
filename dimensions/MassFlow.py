from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray


class MassFlow(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1, time_exponent=-1)
