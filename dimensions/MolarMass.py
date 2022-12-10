from units.dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray


class MolarMass(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1, substance_amount_exponent=-1)
