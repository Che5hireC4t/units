from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit



class Resistivity(AbstractQuantity):
    """
    https://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity
    """

    _DIMENSIONAL_ARRAY = DimensionalArray\
        (
            mass_exponent=1,
            length_exponent=2,
            time_exponent=-3,
            electric_current_exponent=-2
        )
    _UNITS = {Unit('Ω', 'ohm', 1.0): 1}
