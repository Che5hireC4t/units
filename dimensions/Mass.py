from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Mass(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1)
    _UNITS = \
        {
            Unit('g', 'gram', 0.001): 0.001,
            Unit('oz', 'ounce', 0.028349523125): 0.028349523125,
            Unit('lb', 'pound', 0.45359237): 0.45359237,
            Unit('t', 'ton', 1000.0): 1000.0
        }
