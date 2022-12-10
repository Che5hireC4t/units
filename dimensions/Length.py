from units.dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Length(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=1)
    _UNITS = \
        {
            Unit('m', 'meter', 1.0): 1.0,
            Unit('in', 'inch', 0.0254): 0.0254,
            Unit('ft', 'foot', 0.3048): 0.3048,
            Unit('yd', 'yard', 0.9144): 0.9144,
            Unit('mil', 'mile', 1609.344): 1609.344,
            Unit('nmi', 'nautical mile', 1852.0): 1852.0,
            Unit('au', 'astronomical unit', 149597870700.0): 149597870700.0,
            Unit('ly', 'light year', 9460660000000000.0): 9460660000000000.0,
            Unit('ps', 'parsec', 3.0856775814913673e16): 3.0856775814913673e16
        }
