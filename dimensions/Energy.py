from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Energy(AbstractQuantity):
    """
    https://en.wikipedia.org/wiki/Energy
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1, length_exponent=2, time_exponent=-2)
    _UNITS = \
        {
            Unit('J', 'joule', 1.0): 1.0,                                   # https://en.wikipedia.org/wiki/Joule
            Unit('cal', 'calorie', 4.184): 4.184,                           # https://en.wikipedia.org/wiki/Calorie
            Unit('eV', 'electron-volt', 1.602176634e-19): 1.602176634e-19,  # https://en.wikipedia.org/wiki/Electronvolt
            Unit('toe', 'ton-oil-equivalent', 41.868e9): 41.868e9           # https://en.wikipedia.org/wiki/Tonne_of_
                                                                            # oil_equivalent
        }


    def _handle_particular_cases(self, unit_as_string: str) -> (str, str):
        if unit_as_string.startswith('cal'):  # Conflicts with "centi"
            return 'cal', ''
        return None, None
