from units.dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray


class Density(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1, length_exponent=-3)


VolumetricMass = Density
