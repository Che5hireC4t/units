from units.dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Energy(AbstractQuantity):

    # https://en.wikipedia.org/wiki/Energy
    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1, length_exponent=2, time_exponent=-2)
    _UNITS = \
        {
            Unit('J', 'joule', 1.0): 1.0,
            Unit('cal', 'calorie', 4.18): 4.18,
            Unit('eV', 'electron-volt', 1.60217733e-19): 1.60217733e-19,
            Unit('toe', 'ton-oil-equivalent', 41.868e9): 41.868e9
        }


    def _handle_particular_cases(self, unit_as_string: str) -> (str, str):
        if unit_as_string.startswith('cal'):  # Conflicts with "centi"
            return 'cal', ''
        return None, None
