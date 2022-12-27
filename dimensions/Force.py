from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Force(AbstractQuantity):
    """
    https://en.wikipedia.org/wiki/Force
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1, length_exponent=1, time_exponent=-2)
    _UNITS = \
        {
            Unit('N', 'newton', 1.0): 1.0,
            Unit('gf', 'gram.force', 9.80665e-3): 9.80665e-3,  # https://fr.wikipedia.org/wiki/Kilogramme-force
            Unit('lbf', 'pound.force', 4.4482216152605): 4.4482216152605  # https://en.wikipedia.org/wiki/Pound_(force)
        }
