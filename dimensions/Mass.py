from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Mass(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1)
    _UNITS = \
        {
            Unit('g', 'gram', 1.0): 1.0,
            Unit('oz', 'ounce', 28.349523125): 28.349523125,
            Unit('lb', 'pound', 453.59237): 453.59237,
            Unit('t', 'ton', 1000000.0): 1000000.0
        }
