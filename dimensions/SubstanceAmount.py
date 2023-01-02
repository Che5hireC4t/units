from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class SubstanceAmount(AbstractQuantity):
    """
    Supported units (From smallest to biggest):

    Particle        part      SubstanceAmount(1.0, "part")
    Mole            mol       SubstanceAmount(1.0, "mol")       https://en.wikipedia.org/wiki/Mole_(unit)

    https://en.wikipedia.org/wiki/Amount_of_substance
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(substance_amount_exponent=1)
    _UNITS = \
        {
            Unit('mol', 'mole', 1.0): 1.0,  # https://en.wikipedia.org/wiki/Mole_(unit)
            Unit('part', 'particle', 1.0/6.02214076e23): 1.0/6.02214076e23
        }


    def _handle_particular_cases(self, unit_as_string: str) -> (str, str):
        if unit_as_string.startswith('mol'):  # Conflict with "milli"
            return 'mol', ''
        if unit_as_string.startswith('part'):  # Conflict with "pico"
            return 'part', ''
        return None, None
