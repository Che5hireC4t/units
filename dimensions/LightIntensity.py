from dimensions.AbstractQuantity import AbstractQuantity, DimensionalArray, Unit


class LightIntensity(AbstractQuantity):

    _DIMENSIONAL_ARRAY = DimensionalArray(light_intensity_exponent=1)
    _UNITS = {Unit('c', 'candela', 1.0): 1.0}
