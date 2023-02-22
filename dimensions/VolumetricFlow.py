from .AbstractQuantity import AbstractQuantity, DimensionalArray



class VolumetricFlow(AbstractQuantity):
    """
    https://en.wikipedia.org/wiki/Volumetric_flow_rate
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(length_exponent=3, time_exponent=-1)
