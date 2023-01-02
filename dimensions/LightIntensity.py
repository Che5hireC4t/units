from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class LightIntensity(AbstractQuantity):
    """
    Supported units (From smallest to biggest):

    Candela     c       LightIntensity(1.0, "c")
    """

    _DIMENSIONAL_ARRAY = DimensionalArray(light_intensity_exponent=1)
    _UNITS = {Unit('c', 'candela', 1.0): 1.0}
