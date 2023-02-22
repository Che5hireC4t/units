from .AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Voltage(AbstractQuantity):
    """
    https://en.wikipedia.org/wiki/Voltage
    """

    _DIMENSIONAL_ARRAY = DimensionalArray\
        (
            mass_exponent=1,
            length_exponent=2,
            time_exponent=-3,
            electric_current_exponent=-1
        )
    _UNITS = {Unit('V', 'volt', 1.0): 1.0}  # https://en.wikipedia.org/wiki/Volt
