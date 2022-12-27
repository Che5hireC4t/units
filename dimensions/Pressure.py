from units.dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Pressure(AbstractQuantity):

    # https://fr.wikipedia.org/wiki/Unit%C3%A9_de_pression
    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1, length_exponent=-1, time_exponent=-2)
    _UNITS = \
        {
            Unit('Pa', 'pascal', 1.0): 1.0,
            Unit('bar', 'bar', 100000.0): 100000.0,
            Unit('atm', 'norm.atmosphere', 101325.0): 101325.0,
            Unit('at', 'tech.atmosphere', 98066.5): 98066.5,
            Unit('cmwat', 'water-cm', 98.0638): 98.0638,
            Unit('inwat', 'water-inch', 249.08890833333): 249.08890833333,
            Unit('mmHg', 'mercury-mm', 133.322): 133.322,
            Unit('torr', 'torr', 133.322): 133.322,
            Unit('inHg', 'mercury-inch', 3386.389): 3386.389,
            Unit('ba', 'barye', 0.1): 0.1,
            Unit('pz', 'pieze', 1000.0): 1000.0,
            Unit('psi', 'psi', 6894.76): 6894.76
        }
