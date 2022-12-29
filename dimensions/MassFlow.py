from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray


class MassFlow(AbstractQuantity):
    """
    https://en.wikipedia.org/wiki/Mass_flow_rate
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(mass_exponent=1, time_exponent=-1)
