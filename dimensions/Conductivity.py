from .AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class Conductivity(AbstractQuantity):
    """
    Supported units:

    Siemens     σ       Conductivity        https://en.wikipedia.org/wiki/Siemens_(unit)

    https://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity
    """

    _DIMENSIONAL_ARRAY = DimensionalArray \
        (
            mass_exponent=-1,
            length_exponent=-2,
            time_exponent=3,
            electric_current_exponent=2
        )
    _UNITS = {Unit('σ', 'sigma', 1.0): 1.0}
