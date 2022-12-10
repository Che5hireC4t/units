from units.dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class SubstanceAmount(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(substance_amount_exponent=1)
    _UNITS = \
        {
            Unit('mol', 'mole', 1.0): 1.0,
            Unit('part', 'particle', 1.0/6.02214076e23): 1.0/6.02214076e23
        }


    def _handle_particular_cases(self, unit_as_string: str) -> (str, str):
        if unit_as_string.startswith('mol'):  # Conflict with "mili"
            return 'mol', ''
        if unit_as_string.startswith('part'):  # Conflict with "pico"
            return 'part', ''
        return None, None
