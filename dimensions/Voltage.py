from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Voltage(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray\
        (
            mass_exponent=1,
            length_exponent=2,
            time_exponent=-3,
            electric_current_exponent=-1
        )
    _UNITS = {Unit('V', 'volt', 1.0): 1.0}
