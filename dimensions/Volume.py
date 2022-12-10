from units.dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit



class Volume(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=3)
    _UNITS = \
        {
            Unit('l', 'liter', 0.001): 0.001,
            Unit('gal', 'gallon(US)', 0.0002641720524): 0.0002641720524
        }
