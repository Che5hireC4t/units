from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit



class Frequency(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(time_exponent=-1)
    _UNITS = {Unit('Hz', 'hertz', 1.0): 1.0}


    def _handle_particular_cases(self, unit_as_string: str) -> (str, str):
        if unit_as_string.startswith('Hz'):  # Conflicts with "hecto"
            return 'Hz', ''
        return None, None
