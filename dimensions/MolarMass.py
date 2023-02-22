from .AbstractQuantity import AbstractQuantity, DimensionalArray


class MolarMass(AbstractQuantity):
    """
    https://en.wikipedia.org/wiki/Molar_mass
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1, substance_amount_exponent=-1)
