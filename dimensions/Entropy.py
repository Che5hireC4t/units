from .AbstractQuantity import AbstractQuantity, DimensionalArray


class Entropy(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1, length_exponent=2, time_exponent=-2, temperature_exponent=-1)
