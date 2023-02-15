from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Pressure(AbstractQuantity):
    """
    Supported units:

    Pascal                      Pa          Pressure(1.0, "Pa")
    Bar                         bar         Pressure(1.0, "bar")
    Normalized atmosphere       atm         Pressure(1.0, "atm")
    Technical atmosphere        at          Pressure(1.0, "at")
    Centimeter of water         cmwat       Pressure(1.0, "cmwat")
    Inch of water               inwat       Pressure(1.0, "inwat")
    Millimeter of mercury       mmHg        Pressure(1.0, "mmHg")
    Inch of mercury             inHg        Pressure(1.0, "inHg")
    Torr                        torr        Pressure(1.0, "torr")
    Barye                       ba          Pressure(1.0, "ba")
    Pieze                       pz          Pressure(1.0, "pz")
    Psi                         psi         Pressure(1.0, "psi")

    https://en.wikipedia.org/wiki/Pressure
    https://fr.wikipedia.org/wiki/Unit%C3%A9_de_pression  (French)
    """

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
